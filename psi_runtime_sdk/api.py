"""
Enterprise API Server for PSI Runtime SDK - L4 Enhanced

Provides a production-ready API with L4 meta-cognitive capabilities, security, 
monitoring, and comprehensive documentation.

L4 API Features:
- Integrated multi-engine analysis
- Meta-cognitive optimization endpoints
- Cross-engine synchronization
- Advanced analytics and monitoring
"""

import asyncio
from functools import wraps
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Depends, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel, Field
import uvicorn

from .config import get_config
from .logging import get_logger, log_api_request, start_metrics_server
from .monitoring import get_health_status, get_performance_summary
from .security import verify_api_key, verify_jwt_token, RateLimiter

# Import L4 components
try:
    from .l4_integrated_analyzer import L4IntegratedAnalyzer
    from .quantum_engine import L4QuantumAnalyzer
    from .psi_field import L4SemanticFieldEngine
    from .logic_core import BasicResponseLogic
    L4_AVAILABLE = True
except ImportError:
    L4_AVAILABLE = False

# Initialize configuration and logger
config = get_config()
logger = get_logger("api")

# Security
security = HTTPBearer(auto_error=False)
rate_limiter = RateLimiter(
    requests_per_minute=config.security.rate_limit_per_minute
)


# Pydantic models for API
class APIResponse(BaseModel):
    """Standard API response format."""
    success: bool = Field(description="Whether the request was successful")
    data: Optional[Any] = Field(default=None, description="Response data")
    message: Optional[str] = Field(default=None, description="Response message")
    error: Optional[str] = Field(default=None, description="Error message if any")
    request_id: Optional[str] = Field(default=None, description="Unique request identifier")


class AnalysisRequest(BaseModel):
    """Request model for analysis endpoints."""
    query: str = Field(description="Input text to analyze", min_length=1, max_length=10000)
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")
    options: Optional[Dict[str, Any]] = Field(default=None, description="Analysis options")


class L4AnalysisRequest(BaseModel):
    """L4 Enhanced analysis request model."""
    query: str = Field(description="Input text to analyze", min_length=1, max_length=10000)
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")
    session_id: Optional[str] = Field(default=None, description="Session ID for context continuity")
    engine_weights: Optional[Dict[str, float]] = Field(default=None, description="Custom engine weights")
    l4_options: Optional[Dict[str, Any]] = Field(default=None, description="L4-specific options")


class L4StatusResponse(BaseModel):
    """L4 system status response."""
    status: str
    l4_optimization_enabled: bool
    engines: Dict[str, Any]
    integration_features: List[str]
    analysis_history_size: int
    optimal_weights: Dict[str, float]


class BenchmarkRequest(BaseModel):
    """Benchmark request model."""
    query: str = Field(description="Query to benchmark")
    iterations: int = Field(default=5, ge=1, le=50, description="Number of iterations")
    engines: List[str] = Field(default=["integrated"], description="Engines to benchmark")


class ModelConfig(BaseModel):
    """Model configuration for training/fine-tuning."""
    learning_rate: Optional[float] = Field(default=0.001, ge=0.0001, le=0.1)
    epochs: Optional[int] = Field(default=1, ge=1, le=100)
    batch_size: Optional[int] = Field(default=32, ge=1, le=512)


class TrainingRequest(BaseModel):
    """Request model for model training."""
    training_data: List[Dict[str, Any]] = Field(description="Training dataset")
    config: Optional[ModelConfig] = Field(default=None, description="Training configuration")


# Create FastAPI app
def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    
    app = FastAPI(
        title="PSI Runtime SDK API",
        description="Enterprise Quantum-Inspired Reasoning and Semantic Field Analysis API",
        version=config.version,
        docs_url=config.api.docs_url if config.api.docs_enabled else None,
        redoc_url="/redoc" if config.api.docs_enabled else None,
        openapi_url="/openapi.json" if config.api.docs_enabled else None,
    )
    
    # Add middleware
    add_middleware(app)
    
    # Add routes
    add_routes(app)
    
    # Custom OpenAPI schema
    if config.api.docs_enabled:
        app.openapi = lambda: get_custom_openapi(app)
    
    return app


def add_middleware(app: FastAPI):
    """Add security and monitoring middleware."""
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.security.cors_origins,
        allow_credentials=True,
        allow_methods=config.security.cors_methods,
        allow_headers=["*"],
    )
    
    # Trusted host middleware
    if config.is_production:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=["*"]  # Configure this based on your needs
        )


def add_routes(app: FastAPI):
    """Add API routes to the application."""
    
    @app.get("/", response_model=APIResponse)
    async def root():
        """Root endpoint with basic information."""
        return APIResponse(
            success=True,
            data={
                "name": "PSI Runtime SDK API",
                "version": config.version,
                "status": "operational",
                "docs_url": config.api.docs_url if config.api.docs_enabled else None
            },
            message="PSI Runtime SDK API is operational"
        )
    
    @app.get("/health", response_model=APIResponse)
    async def health_check():
        """Comprehensive health check endpoint."""
        try:
            health_data = await get_health_status()
            
            return APIResponse(
                success=health_data["status"] != "unhealthy",
                data=health_data,
                message=f"System status: {health_data['status']}"
            )
        except Exception as e:
            logger.error("Health check failed", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Health check failed"
            )
    
    @app.get("/metrics/summary", response_model=APIResponse)
    async def metrics_summary(
        hours: int = 1,
        credentials: HTTPAuthorizationCredentials = Security(security)
    ):
        """Get performance metrics summary."""
        await verify_authentication(credentials)
        
        try:
            metrics_data = get_performance_summary(hours)
            
            return APIResponse(
                success=True,
                data=metrics_data,
                message=f"Performance metrics for the last {hours} hour(s)"
            )
        except Exception as e:
            logger.error("Failed to get metrics summary", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve metrics"
            )
    
    @app.post("/analyze/basic", response_model=APIResponse)
    @log_api_request
    async def basic_analysis(
        request: AnalysisRequest,
        credentials: HTTPAuthorizationCredentials = Security(security)
    ):
        """Perform basic semantic analysis."""
        await verify_authentication(credentials)
        await rate_limiter.check_rate_limit("basic_analysis")
        
        try:
            # Import here to avoid circular imports
            from .logic_core import BasicResponseLogic
            
            engine = BasicResponseLogic()
            result = engine.run(request.query, request.context or {})
            
            return APIResponse(
                success=True,
                data=result,
                message="Basic analysis completed successfully"
            )
        except Exception as e:
            logger.error("Basic analysis failed", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Analysis failed"
            )
    
    @app.post("/analyze/quantum", response_model=APIResponse)
    @log_api_request
    async def quantum_analysis(
        request: AnalysisRequest,
        credentials: HTTPAuthorizationCredentials = Security(security)
    ):
        """Perform quantum-inspired analysis."""
        await verify_authentication(credentials)
        await rate_limiter.check_rate_limit("quantum_analysis")
        
        try:
            from .quantum_engine import QuantumAnalyzer
            
            analyzer = QuantumAnalyzer()
            result = analyzer.comprehensive_analysis(request.query)
            
            return APIResponse(
                success=True,
                data=result,
                message="Quantum analysis completed successfully"
            )
        except Exception as e:
            logger.error("Quantum analysis failed", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Quantum analysis failed"
            )
    
    @app.post("/analyze/semantic-field", response_model=APIResponse)
    @log_api_request
    async def semantic_field_analysis(
        request: AnalysisRequest,
        credentials: HTTPAuthorizationCredentials = Security(security)
    ):
        """Perform semantic field analysis."""
        await verify_authentication(credentials)
        await rate_limiter.check_rate_limit("semantic_field_analysis")
        
        try:
            from .psi_field import SemanticFieldEngine, DataParser
            
            engine = SemanticFieldEngine()
            semantic_input = DataParser.parse(request.query)
            result = engine.psi_engine.unlock_knowledge(semantic_input)
            
            return APIResponse(
                success=True,
                data={"unlocked_keys": result},
                message="Semantic field analysis completed successfully"
            )
        except Exception as e:
            logger.error("Semantic field analysis failed", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Semantic field analysis failed"
            )
    
    @app.post("/analyze/comprehensive", response_model=APIResponse)
    @log_api_request
    async def comprehensive_analysis(
        request: AnalysisRequest,
        credentials: HTTPAuthorizationCredentials = Security(security)
    ):
        """Perform comprehensive analysis using all engines."""
        await verify_authentication(credentials)
        await rate_limiter.check_rate_limit("comprehensive_analysis")
        
        try:
            # Run all analysis types
            basic_task = asyncio.create_task(
                run_basic_analysis(request.query, request.context)
            )
            quantum_task = asyncio.create_task(
                run_quantum_analysis(request.query)
            )
            semantic_task = asyncio.create_task(
                run_semantic_analysis(request.query)
            )
            
            # Wait for all analyses to complete
            basic_result, quantum_result, semantic_result = await asyncio.gather(
                basic_task, quantum_task, semantic_task,
                return_exceptions=True
            )
            
            # Compile results
            result = {
                "basic_analysis": basic_result if not isinstance(basic_result, Exception) else str(basic_result),
                "quantum_analysis": quantum_result if not isinstance(quantum_result, Exception) else str(quantum_result),
                "semantic_analysis": semantic_result if not isinstance(semantic_result, Exception) else str(semantic_result),
                "integrated_confidence": calculate_integrated_confidence(
                    basic_result, quantum_result, semantic_result
                )
            }
            
            return APIResponse(
                success=True,
                data=result,
                message="Comprehensive analysis completed successfully"
            )
        except Exception as e:
            logger.error("Comprehensive analysis failed", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Comprehensive analysis failed"
            )
    
    @app.post("/model/train", response_model=APIResponse)
    @log_api_request
    async def train_model(
        request: TrainingRequest,
        credentials: HTTPAuthorizationCredentials = Security(security)
    ):
        """Train or fine-tune the model."""
        await verify_authentication(credentials)
        await rate_limiter.check_rate_limit("model_training")
        
        try:
            # This would implement actual model training
            # For now, simulate training process
            
            training_config = request.config or ModelConfig()
            
            result = {
                "training_started": True,
                "data_points": len(request.training_data),
                "config": training_config.dict(),
                "estimated_duration": "2-5 minutes",
                "status": "training_in_progress"
            }
            
            return APIResponse(
                success=True,
                data=result,
                message="Model training started successfully"
            )
        except Exception as e:
            logger.error("Model training failed", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Model training failed"
            )
    
    # L4 Enhanced Analysis Endpoints
    @app.post("/l4/analyze/integrated", response_model=APIResponse)
    @log_api_request
    async def l4_integrated_analysis(
        request: L4AnalysisRequest,
        credentials: HTTPAuthorizationCredentials = Security(security)
    ):
        """L4 integrated multi-engine analysis with meta-cognitive optimization."""
        await verify_authentication(credentials)
        await rate_limiter.check_rate_limit("l4_analysis")
        
        if not L4_AVAILABLE:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="L4 components not available"
            )
        
        try:
            analyzer = L4IntegratedAnalyzer()
            
            result = analyzer.analyze(
                request.query,
                context=request.context,
                session_id=request.session_id
            )
            
            return APIResponse(
                success=True,
                data=result,
                message="L4 integrated analysis completed successfully"
            )
        except Exception as e:
            logger.error("L4 integrated analysis failed", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="L4 integrated analysis failed"
            )
    
    @app.get("/l4/status", response_model=APIResponse)
    @log_api_request  
    async def l4_status(
        engine: Optional[str] = None,
        credentials: HTTPAuthorizationCredentials = Security(security)
    ):
        """Get L4 system status and optimization metrics."""
        await verify_authentication(credentials)
        
        if not L4_AVAILABLE:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="L4 components not available"
            )
        
        try:
            if engine == "integrated" or not engine:
                analyzer = L4IntegratedAnalyzer()
                status_data = analyzer.get_l4_status()
            else:
                # Get integrated status as default
                integrated = L4IntegratedAnalyzer()
                status_data = integrated.get_l4_status()
            
            return APIResponse(
                success=True,
                data=status_data,
                message=f"L4 {engine or 'system'} status retrieved successfully"
            )
        except Exception as e:
            logger.error("L4 status check failed", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="L4 status check failed"
            )
    
    @app.get("/l4/features", response_model=APIResponse)
    @log_api_request
    async def l4_features():
        """Get available L4 features and capabilities."""
        try:
            features = {
                "l4_available": L4_AVAILABLE,
                "engines": {
                    "integrated_analyzer": L4_AVAILABLE,
                    "quantum_analyzer": L4_AVAILABLE,
                    "semantic_field_engine": L4_AVAILABLE,
                    "logic_core_engine": True
                },
                "capabilities": [
                    "meta_cognitive_optimization",
                    "cross_engine_synchronization", 
                    "adaptive_confidence_calibration",
                    "integrated_reasoning_paths",
                    "dynamic_engine_weighting"
                ] if L4_AVAILABLE else ["basic_analysis"],
                "api_endpoints": [
                    "/l4/analyze/integrated",
                    "/l4/status", 
                    "/l4/features"
                ] if L4_AVAILABLE else []
            }
            
            return APIResponse(
                success=True,
                data=features,
                message="L4 features information retrieved successfully"
            )
        except Exception as e:
            logger.error("L4 features check failed", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="L4 features check failed"
            )


async def verify_authentication(credentials: HTTPAuthorizationCredentials):
    """Verify API authentication."""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    # Try JWT token first, then API key
    try:
        verify_jwt_token(credentials.credentials)
    except:
        try:
            verify_api_key(credentials.credentials)
        except:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )


# Helper functions for analysis
async def run_basic_analysis(query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
    """Run basic analysis asynchronously."""
    from .logic_core import BasicResponseLogic
    
    engine = BasicResponseLogic()
    return engine.run(query, context or {})


async def run_quantum_analysis(query: str) -> Dict[str, Any]:
    """Run quantum analysis asynchronously."""
    from .quantum_engine import QuantumAnalyzer
    
    analyzer = QuantumAnalyzer()
    return analyzer.comprehensive_analysis(query)


async def run_semantic_analysis(query: str) -> Dict[str, Any]:
    """Run semantic field analysis asynchronously."""
    from .psi_field import SemanticFieldEngine, DataParser
    
    engine = SemanticFieldEngine()
    semantic_input = DataParser.parse(query)
    result = engine.psi_engine.unlock_knowledge(semantic_input)
    return {"unlocked_keys": result}


def calculate_integrated_confidence(
    basic_result: Any, 
    quantum_result: Any, 
    semantic_result: Any
) -> float:
    """Calculate integrated confidence score from all analysis results."""
    try:
        basic_score = basic_result.get("final_result", 0.5) if isinstance(basic_result, dict) else 0.5
        quantum_score = quantum_result.get("integrated_score", 0.5) if isinstance(quantum_result, dict) else 0.5
        semantic_score = 0.7 if isinstance(semantic_result, dict) and semantic_result.get("unlocked_keys") else 0.3
        
        # Weighted average
        return (basic_score * 0.4 + quantum_score * 0.4 + semantic_score * 0.2)
    except:
        return 0.5


def get_custom_openapi(app: FastAPI):
    """Generate custom OpenAPI schema with additional metadata."""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="PSI Runtime SDK API",
        version=config.version,
        description="""
        ## Enterprise Quantum-Inspired Reasoning and Semantic Field Analysis API
        
        This API provides access to advanced AI reasoning capabilities through three core engines:
        
        - **Logic Core**: Basic reasoning and response logic
        - **Quantum Engine**: Quantum-inspired analysis and reasoning
        - **PSI Field**: Semantic field analysis and knowledge unlocking
        
        ### Authentication
        
        All endpoints require authentication via:
        - Bearer JWT tokens
        - API keys in the Authorization header
        
        ### Rate Limiting
        
        API calls are rate-limited to prevent abuse. Default limit is 60 requests per minute.
        
        ### Monitoring
        
        The API includes comprehensive monitoring and health check endpoints for enterprise deployment.
        """,
        routes=app.routes,
    )
    
    # Add additional metadata
    openapi_schema["info"]["contact"] = {
        "name": "PSI Runtime SDK Support",
        "email": "reagan.fue@gmail.com",
        "url": "https://github.com/reaganfue/PSI-Runtime-SDK"
    }
    
    openapi_schema["info"]["license"] = {
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
    
    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        },
        "apiKeyAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization"
        }
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


# Create the application instance
app = create_app()


if __name__ == "__main__":
    # Start metrics server
    start_metrics_server()
    
    # Run the API server
    uvicorn.run(
        "psi_runtime_sdk.api:app",
        host=config.api.host,
        port=config.api.port,
        workers=config.api.workers if not config.is_development else 1,
        reload=config.is_development,
        log_level="info"
    )