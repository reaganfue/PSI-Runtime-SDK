"""
Enterprise Configuration Management for PSI Runtime SDK

This module provides centralized configuration management with:
- Environment-based configuration
- Validation and type checking
- Security-aware handling of secrets
- Monitoring and logging configuration
"""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class SecurityConfig(BaseSettings):
    """Security-related configuration."""
    
    # JWT Settings
    jwt_secret_key: str = Field(default="", env="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", env="JWT_ALGORITHM")
    jwt_expiration_hours: int = Field(default=24, env="JWT_EXPIRATION_HOURS")
    
    # API Security
    api_key_header: str = Field(default="X-API-Key", env="API_KEY_HEADER")
    rate_limit_per_minute: int = Field(default=60, env="RATE_LIMIT_PER_MINUTE")
    
    # CORS Settings
    cors_origins: List[str] = Field(default=["*"], env="CORS_ORIGINS")
    cors_methods: List[str] = Field(default=["GET", "POST"], env="CORS_METHODS")
    
    model_config = SettingsConfigDict(env_prefix="SECURITY_")


class DatabaseConfig(BaseSettings):
    """Database configuration."""
    
    # Connection settings
    url: str = Field(default="sqlite:///psi_runtime.db", env="DATABASE_URL")
    pool_size: int = Field(default=5, env="DATABASE_POOL_SIZE")
    max_overflow: int = Field(default=10, env="DATABASE_MAX_OVERFLOW")
    pool_timeout: int = Field(default=30, env="DATABASE_POOL_TIMEOUT")
    
    # Security
    ssl_mode: str = Field(default="prefer", env="DATABASE_SSL_MODE")
    
    model_config = SettingsConfigDict(env_prefix="DATABASE_")


class LoggingConfig(BaseSettings):
    """Logging and monitoring configuration."""
    
    # Log levels
    level: str = Field(default="INFO", env="LOG_LEVEL")
    format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        env="LOG_FORMAT"
    )
    
    # File logging
    file_enabled: bool = Field(default=True, env="LOG_FILE_ENABLED")
    file_path: str = Field(default="logs/psi_runtime.log", env="LOG_FILE_PATH")
    file_max_size: int = Field(default=10485760, env="LOG_FILE_MAX_SIZE")  # 10MB
    file_backup_count: int = Field(default=5, env="LOG_FILE_BACKUP_COUNT")
    
    # Structured logging
    structured: bool = Field(default=True, env="LOG_STRUCTURED")
    
    # External logging services
    sentry_dsn: Optional[str] = Field(default=None, env="SENTRY_DSN")
    
    model_config = SettingsConfigDict(env_prefix="LOGGING_")


class MonitoringConfig(BaseSettings):
    """Monitoring and metrics configuration."""
    
    # Prometheus metrics
    metrics_enabled: bool = Field(default=True, env="METRICS_ENABLED")
    metrics_port: int = Field(default=8000, env="METRICS_PORT")
    metrics_path: str = Field(default="/metrics", env="METRICS_PATH")
    
    # Health checks
    health_check_interval: int = Field(default=30, env="HEALTH_CHECK_INTERVAL")
    
    # Performance monitoring
    performance_tracking: bool = Field(default=True, env="PERFORMANCE_TRACKING")
    slow_query_threshold: float = Field(default=1.0, env="SLOW_QUERY_THRESHOLD")
    
    model_config = SettingsConfigDict(env_prefix="MONITORING_")


class APIConfig(BaseSettings):
    """API server configuration."""
    
    # Server settings
    host: str = Field(default="0.0.0.0", env="API_HOST")
    port: int = Field(default=5000, env="API_PORT")
    workers: int = Field(default=4, env="API_WORKERS")
    
    # Request handling
    max_request_size: int = Field(default=16777216, env="API_MAX_REQUEST_SIZE")  # 16MB
    request_timeout: int = Field(default=30, env="API_REQUEST_TIMEOUT")
    
    # Documentation
    docs_enabled: bool = Field(default=True, env="API_DOCS_ENABLED")
    docs_url: str = Field(default="/docs", env="API_DOCS_URL")
    
    model_config = SettingsConfigDict(env_prefix="API_")


class ModelConfig(BaseSettings):
    """AI Model configuration."""
    
    # Model paths and settings
    model_path: str = Field(default="models/", env="MODEL_PATH")
    cache_enabled: bool = Field(default=True, env="MODEL_CACHE_ENABLED")
    cache_size: int = Field(default=1000, env="MODEL_CACHE_SIZE")
    
    # Performance settings
    batch_size: int = Field(default=32, env="MODEL_BATCH_SIZE")
    max_sequence_length: int = Field(default=512, env="MODEL_MAX_SEQUENCE_LENGTH")
    
    # Quantum engine settings
    quantum_simulation_depth: int = Field(default=10, env="QUANTUM_SIMULATION_DEPTH")
    semantic_field_dimensions: int = Field(default=768, env="SEMANTIC_FIELD_DIMENSIONS")
    
    model_config = SettingsConfigDict(env_prefix="MODEL_")


class EnterpriseConfig(BaseSettings):
    """Main enterprise configuration class."""
    
    # Environment
    environment: str = Field(default="development", env="ENVIRONMENT")
    debug: bool = Field(default=False, env="DEBUG")
    version: str = Field(default="0.1.0", env="VERSION")
    
    # Sub-configurations
    security: SecurityConfig = Field(default_factory=SecurityConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    monitoring: MonitoringConfig = Field(default_factory=MonitoringConfig)
    api: APIConfig = Field(default_factory=APIConfig)
    model: ModelConfig = Field(default_factory=ModelConfig)
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    @validator("environment")
    def validate_environment(cls, v):
        """Validate environment setting."""
        allowed = ["development", "testing", "staging", "production"]
        if v not in allowed:
            raise ValueError(f"Environment must be one of: {allowed}")
        return v
    
    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.environment == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.environment == "development"
    
    def get_log_config(self) -> Dict[str, Any]:
        """Get logging configuration dictionary."""
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": self.logging.format,
                },
                "json": {
                    "()": "structlog.stdlib.ProcessorFormatter",
                    "processor": "structlog.dev.ConsoleRenderer",
                },
            },
            "handlers": {
                "default": {
                    "formatter": "json" if self.logging.structured else "default",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                },
                "file": {
                    "formatter": "json" if self.logging.structured else "default",
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": self.logging.file_path,
                    "maxBytes": self.logging.file_max_size,
                    "backupCount": self.logging.file_backup_count,
                },
            },
            "loggers": {
                "": {
                    "level": self.logging.level,
                    "handlers": ["default"] + (["file"] if self.logging.file_enabled else []),
                },
            },
        }


# Global configuration instance
config = EnterpriseConfig()


def get_config() -> EnterpriseConfig:
    """Get the global configuration instance."""
    return config


def load_config_from_file(file_path: str) -> EnterpriseConfig:
    """Load configuration from a specific file."""
    return EnterpriseConfig(_env_file=file_path)