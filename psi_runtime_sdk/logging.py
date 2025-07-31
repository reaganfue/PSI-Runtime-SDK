"""
Enterprise Logging System for PSI Runtime SDK

Provides structured logging, monitoring, and observability features.
"""

import logging
import logging.config
import sys
import time
from contextlib import contextmanager
from functools import wraps
from typing import Any, Dict, Optional

import structlog
from prometheus_client import Counter, Histogram, start_http_server

from .config import get_config

# Metrics
REQUEST_COUNT = Counter(
    "psi_runtime_requests_total", 
    "Total number of requests", 
    ["method", "endpoint", "status"]
)

REQUEST_DURATION = Histogram(
    "psi_runtime_request_duration_seconds",
    "Request duration in seconds",
    ["method", "endpoint"]
)

ERROR_COUNT = Counter(
    "psi_runtime_errors_total",
    "Total number of errors",
    ["error_type", "component"]
)

MODEL_INFERENCE_COUNT = Counter(
    "psi_runtime_model_inferences_total",
    "Total number of model inferences",
    ["model_type", "status"]
)

MODEL_INFERENCE_DURATION = Histogram(
    "psi_runtime_model_inference_duration_seconds",
    "Model inference duration in seconds",
    ["model_type"]
)


def setup_logging(config_dict: Optional[Dict[str, Any]] = None) -> None:
    """Set up enterprise logging with structured logging support."""
    config = get_config()
    
    if config_dict is None:
        config_dict = config.get_log_config()
    
    # Configure standard logging
    logging.config.dictConfig(config_dict)
    
    # Configure structured logging
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="ISO"),
            structlog.dev.ConsoleRenderer() if config.is_development else structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(config.logging.level),
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
    
    # Set up Sentry if configured
    if config.logging.sentry_dsn:
        try:
            import sentry_sdk
            from sentry_sdk.integrations.logging import LoggingIntegration
            
            sentry_logging = LoggingIntegration(
                level=logging.INFO,
                event_level=logging.ERROR
            )
            
            sentry_sdk.init(
                dsn=config.logging.sentry_dsn,
                integrations=[sentry_logging],
                environment=config.environment,
                release=config.version,
            )
        except ImportError:
            logging.warning("Sentry SDK not installed, skipping Sentry setup")


def get_logger(name: str) -> structlog.BoundLogger:
    """Get a structured logger instance."""
    return structlog.get_logger(name)


class LoggerMixin:
    """Mixin class to add logging capabilities to any class."""
    
    @property
    def logger(self) -> structlog.BoundLogger:
        """Get a logger instance for this class."""
        return get_logger(self.__class__.__name__)


def log_function_call(
    include_args: bool = False,
    include_result: bool = False,
    log_level: str = "INFO"
) -> Any:
    """Decorator to log function calls."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = get_logger(func.__module__)
            
            log_data = {
                "function": func.__name__,
                "module": func.__module__,
            }
            
            if include_args:
                log_data["args"] = args
                log_data["kwargs"] = kwargs
            
            logger.info("Function call started", **log_data)
            
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                
                duration = time.time() - start_time
                log_data["duration"] = duration
                log_data["status"] = "success"
                
                if include_result:
                    log_data["result"] = result
                
                getattr(logger, log_level.lower())("Function call completed", **log_data)
                return result
                
            except Exception as e:
                duration = time.time() - start_time
                log_data["duration"] = duration
                log_data["status"] = "error"
                log_data["error"] = str(e)
                log_data["error_type"] = type(e).__name__
                
                logger.error("Function call failed", **log_data)
                
                # Record error metrics
                ERROR_COUNT.labels(
                    error_type=type(e).__name__,
                    component=func.__module__
                ).inc()
                
                raise
        
        return wrapper
    return decorator


@contextmanager
def log_context(**kwargs):
    """Context manager to add structured context to logs."""
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(**kwargs)
    try:
        yield
    finally:
        structlog.contextvars.clear_contextvars()


def log_model_inference(model_type: str):
    """Decorator to log and monitor model inference calls."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = get_logger("model_inference")
            
            with log_context(model_type=model_type, function=func.__name__):
                logger.info("Model inference started")
                
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    
                    duration = time.time() - start_time
                    
                    # Record metrics
                    MODEL_INFERENCE_COUNT.labels(
                        model_type=model_type,
                        status="success"
                    ).inc()
                    
                    MODEL_INFERENCE_DURATION.labels(
                        model_type=model_type
                    ).observe(duration)
                    
                    logger.info(
                        "Model inference completed",
                        duration=duration,
                        status="success"
                    )
                    
                    return result
                    
                except Exception as e:
                    duration = time.time() - start_time
                    
                    # Record error metrics
                    MODEL_INFERENCE_COUNT.labels(
                        model_type=model_type,
                        status="error"
                    ).inc()
                    
                    ERROR_COUNT.labels(
                        error_type=type(e).__name__,
                        component="model_inference"
                    ).inc()
                    
                    logger.error(
                        "Model inference failed",
                        duration=duration,
                        error=str(e),
                        error_type=type(e).__name__
                    )
                    
                    raise
        
        return wrapper
    return decorator


def log_api_request(func):
    """Decorator to log API requests with metrics."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        from flask import request
        
        logger = get_logger("api")
        
        with log_context(
            method=request.method,
            path=request.path,
            remote_addr=request.remote_addr,
            user_agent=request.headers.get("User-Agent", "")
        ):
            logger.info("API request started")
            
            start_time = time.time()
            try:
                response = func(*args, **kwargs)
                
                duration = time.time() - start_time
                status_code = getattr(response, 'status_code', 200)
                
                # Record metrics
                REQUEST_COUNT.labels(
                    method=request.method,
                    endpoint=request.endpoint or "unknown",
                    status=status_code
                ).inc()
                
                REQUEST_DURATION.labels(
                    method=request.method,
                    endpoint=request.endpoint or "unknown"
                ).observe(duration)
                
                logger.info(
                    "API request completed",
                    status_code=status_code,
                    duration=duration
                )
                
                return response
                
            except Exception as e:
                duration = time.time() - start_time
                
                # Record error metrics
                ERROR_COUNT.labels(
                    error_type=type(e).__name__,
                    component="api"
                ).inc()
                
                logger.error(
                    "API request failed",
                    duration=duration,
                    error=str(e),
                    error_type=type(e).__name__
                )
                
                raise
    
    return wrapper


def start_metrics_server():
    """Start the Prometheus metrics server."""
    config = get_config()
    
    if config.monitoring.metrics_enabled:
        try:
            start_http_server(config.monitoring.metrics_port)
            logger = get_logger("metrics")
            logger.info(
                "Metrics server started",
                port=config.monitoring.metrics_port,
                path=config.monitoring.metrics_path
            )
        except Exception as e:
            logger = get_logger("metrics")
            logger.error(
                "Failed to start metrics server",
                error=str(e),
                error_type=type(e).__name__
            )


class SecurityLogger:
    """Security-focused logging utilities."""
    
    def __init__(self):
        self.logger = get_logger("security")
    
    def log_authentication_attempt(self, username: str, success: bool, ip_address: str = None):
        """Log authentication attempts."""
        self.logger.info(
            "Authentication attempt",
            username=username,
            success=success,
            ip_address=ip_address,
            event_type="authentication"
        )
    
    def log_authorization_failure(self, username: str, resource: str, ip_address: str = None):
        """Log authorization failures."""
        self.logger.warning(
            "Authorization failed",
            username=username,
            resource=resource,
            ip_address=ip_address,
            event_type="authorization_failure"
        )
    
    def log_security_event(self, event_type: str, severity: str = "info", **kwargs):
        """Log general security events."""
        log_method = getattr(self.logger, severity.lower(), self.logger.info)
        log_method(
            "Security event",
            event_type=event_type,
            severity=severity,
            **kwargs
        )


# Global security logger instance
security_logger = SecurityLogger()