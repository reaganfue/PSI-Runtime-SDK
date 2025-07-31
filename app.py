#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Enterprise Application Entry Point - PSI Runtime SDK

Production-ready application with comprehensive monitoring, security, and logging.
"""

import os
import sys
import asyncio
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Enterprise imports
from psi_runtime_sdk.config import get_config
from psi_runtime_sdk.logging import setup_logging, get_logger, start_metrics_server
from psi_runtime_sdk.monitoring import health_checker
from psi_runtime_sdk.api import app

# Legacy Flask app for backward compatibility
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize enterprise configuration
config = get_config()

# Set up enterprise logging
setup_logging()
logger = get_logger("main")

# Legacy Flask app setup for backward compatibility
flask_app = Flask(__name__)

try:
    # Import legacy modules with error handling
    try:
        from psi_field import PsiFieldModel
        from logic_core import LogicCore
        legacy_modules_available = True
        logger.info("Legacy modules loaded successfully")
    except ImportError as e:
        logger.warning(f"Legacy modules not available: {e}")
        legacy_modules_available = False
        
        # Use new module structure
        from psi_runtime_sdk.psi_field import PsiFieldModel
        from psi_runtime_sdk.logic_core import LogicCore
        logger.info("Using new enterprise module structure")

    # Initialize models
    if legacy_modules_available:
        psi_field_model = PsiFieldModel()
        logic_core = LogicCore()
        logger.info("Legacy models initialized successfully")
    else:
        # Initialize with enterprise modules
        psi_field_model = PsiFieldModel()
        logic_core = LogicCore()
        logger.info("Enterprise models initialized successfully")

except Exception as e:
    logger.error(f"Model initialization failed: {str(e)}")
    # Continue without models for health checks and monitoring
    psi_field_model = None
    logic_core = None


# Legacy Flask routes for backward compatibility
@flask_app.route('/')
def index():
    """Main page - redirect to API documentation"""
    if config.api.docs_enabled:
        return jsonify({
            "message": "PSI Runtime SDK Enterprise API",
            "version": config.version,
            "documentation": f"http://localhost:{config.api.port}{config.api.docs_url}",
            "api_endpoint": f"http://localhost:{config.api.port}/",
            "health_check": f"http://localhost:{config.api.port}/health"
        })
    else:
        return jsonify({
            "message": "PSI Runtime SDK Enterprise API", 
            "version": config.version,
            "status": "operational"
        })


@flask_app.route('/api/process', methods=['POST'])
def process_input():
    """Legacy processing endpoint"""
    try:
        data = request.json
        if not data or 'input' not in data:
            return jsonify({'error': 'Missing input data'}), 400
        
        input_text = data['input']
        context = data.get('context', {})
        
        if not psi_field_model or not logic_core:
            return jsonify({'error': 'Models not available'}), 503
        
        # Use models with error handling
        psi_result = psi_field_model.process(input_text, context)
        result = logic_core.analyze(psi_result)
        
        return jsonify({
            'status': 'success',
            'result': result,
            'psi_field_data': psi_result.to_dict() if hasattr(psi_result, 'to_dict') else psi_result,
            'note': 'Legacy endpoint - consider migrating to /analyze/comprehensive'
        })
    except Exception as e:
        logger.error(f"Legacy processing failed: {str(e)}")
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500


@flask_app.route('/api/model/status', methods=['GET'])
def model_status():
    """Legacy model status endpoint"""
    try:
        status_data = {
            'status': 'online' if psi_field_model and logic_core else 'degraded',
            'version': config.version,
            'enterprise_features': True,
            'monitoring_enabled': config.monitoring.metrics_enabled,
            'security_enabled': True,
        }
        
        if psi_field_model:
            status_data['psi_field'] = 'available'
        if logic_core:
            status_data['logic_core'] = 'available'
            
        return jsonify(status_data)
    except Exception as e:
        logger.error(f"Status check failed: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


@flask_app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found',
        'suggestion': f'Try the enterprise API at http://localhost:{config.api.port}/'
    }), 404


@flask_app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    logger.error(f"Server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500


async def start_enterprise_services():
    """Start enterprise services"""
    try:
        # Start metrics server
        start_metrics_server()
        logger.info("Metrics server started")
        
        # Run initial health check
        health_status = await health_checker.get_system_health()
        logger.info(f"Initial health check: {health_status.status}")
        
        return True
    except Exception as e:
        logger.error(f"Failed to start enterprise services: {e}")
        return False


def run_enterprise_api():
    """Run the enterprise FastAPI server"""
    import uvicorn
    
    logger.info("Starting PSI Runtime SDK Enterprise API")
    logger.info(f"Environment: {config.environment}")
    logger.info(f"Debug mode: {config.debug}")
    logger.info(f"API documentation: {'enabled' if config.api.docs_enabled else 'disabled'}")
    
    uvicorn.run(
        "psi_runtime_sdk.api:app",
        host=config.api.host,
        port=config.api.port,
        workers=config.api.workers if config.is_production else 1,
        reload=config.is_development,
        log_level="info",
        access_log=True
    )


def run_legacy_flask():
    """Run the legacy Flask server"""
    logger.info("Starting PSI Runtime SDK Legacy Flask Server")
    logger.warning("Legacy mode - consider migrating to enterprise API")
    
    port = int(os.environ.get('PORT', 5001))  # Use different port
    debug = config.is_development
    
    flask_app.run(
        host='0.0.0.0',
        port=port,
        debug=debug,
        threaded=True
    )


async def main():
    """Main application entry point"""
    logger.info("=" * 60)
    logger.info("PSI Runtime SDK Enterprise Edition")
    logger.info(f"Version: {config.version}")
    logger.info(f"Environment: {config.environment}")
    logger.info("=" * 60)
    
    # Start enterprise services
    services_started = await start_enterprise_services()
    
    if not services_started:
        logger.error("Failed to start enterprise services")
        sys.exit(1)
    
    # Determine which server to run
    run_mode = os.environ.get('RUN_MODE', 'enterprise').lower()
    
    if run_mode == 'legacy':
        logger.info("Running in legacy Flask mode")
        run_legacy_flask()
    elif run_mode == 'both':
        logger.info("Running both enterprise and legacy servers")
        # This would require running in separate processes
        logger.warning("Both mode not implemented - running enterprise API only")
        run_enterprise_api()
    else:
        logger.info("Running in enterprise FastAPI mode")
        run_enterprise_api()


if __name__ == '__main__':
    try:
        # Check if we're running in an event loop already
        try:
            loop = asyncio.get_running_loop()
            # If we're in an async context, run the startup directly
            asyncio.create_task(start_enterprise_services())
            run_enterprise_api()
        except RuntimeError:
            # No event loop running, start normally
            asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.error(f"Application startup failed: {e}")
        sys.exit(1)
