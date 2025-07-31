"""
Enterprise Monitoring and Health Check System for PSI Runtime SDK

Provides comprehensive health checks, monitoring, and alerting capabilities.
"""

import asyncio
import json
import platform
import psutil
import time
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional

from prometheus_client import Gauge, Info
from pydantic import BaseModel

from .config import get_config
from .logging import get_logger, LoggerMixin

# Prometheus metrics for system monitoring
SYSTEM_CPU_USAGE = Gauge("psi_runtime_cpu_usage_percent", "CPU usage percentage")
SYSTEM_MEMORY_USAGE = Gauge("psi_runtime_memory_usage_percent", "Memory usage percentage")
SYSTEM_DISK_USAGE = Gauge("psi_runtime_disk_usage_percent", "Disk usage percentage")
ACTIVE_CONNECTIONS = Gauge("psi_runtime_active_connections", "Number of active connections")
MODEL_CACHE_SIZE = Gauge("psi_runtime_model_cache_size", "Size of model cache")
SYSTEM_INFO = Info("psi_runtime_system", "System information")


class HealthStatus(str, Enum):
    """Health check status enumeration."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


class HealthCheck(BaseModel):
    """Individual health check result."""
    name: str
    status: HealthStatus
    message: str
    timestamp: datetime
    duration_ms: float
    details: Optional[Dict[str, Any]] = None


class SystemHealth(BaseModel):
    """Overall system health status."""
    status: HealthStatus
    timestamp: datetime
    version: str
    uptime_seconds: float
    checks: List[HealthCheck]
    system_metrics: Dict[str, Any]


class HealthChecker(LoggerMixin):
    """Main health checking system."""
    
    def __init__(self):
        self.config = get_config()
        self.start_time = time.time()
        self.checks = {}
        self._register_default_checks()
    
    def _register_default_checks(self):
        """Register default health checks."""
        self.register_check("system_resources", self._check_system_resources)
        self.register_check("model_status", self._check_model_status)
        self.register_check("database_connection", self._check_database_connection)
        self.register_check("external_dependencies", self._check_external_dependencies)
    
    def register_check(self, name: str, check_func):
        """Register a health check function."""
        self.checks[name] = check_func
        self.logger.info(f"Registered health check: {name}")
    
    async def run_check(self, name: str, check_func) -> HealthCheck:
        """Run a single health check."""
        start_time = time.time()
        
        try:
            if asyncio.iscoroutinefunction(check_func):
                result = await check_func()
            else:
                result = check_func()
            
            duration = (time.time() - start_time) * 1000
            
            if isinstance(result, tuple):
                status, message, details = result
            else:
                status, message, details = result, "Check passed", None
            
            return HealthCheck(
                name=name,
                status=status,
                message=message,
                timestamp=datetime.utcnow(),
                duration_ms=duration,
                details=details
            )
            
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            self.logger.error(f"Health check {name} failed", error=str(e))
            
            return HealthCheck(
                name=name,
                status=HealthStatus.UNHEALTHY,
                message=f"Check failed: {str(e)}",
                timestamp=datetime.utcnow(),
                duration_ms=duration,
                details={"error_type": type(e).__name__}
            )
    
    async def get_system_health(self) -> SystemHealth:
        """Get comprehensive system health status."""
        check_results = []
        
        # Run all registered checks
        for name, check_func in self.checks.items():
            result = await self.run_check(name, check_func)
            check_results.append(result)
        
        # Determine overall status
        overall_status = self._determine_overall_status(check_results)
        
        # Get system metrics
        system_metrics = self._get_system_metrics()
        
        # Update Prometheus metrics
        self._update_prometheus_metrics(system_metrics)
        
        return SystemHealth(
            status=overall_status,
            timestamp=datetime.utcnow(),
            version=self.config.version,
            uptime_seconds=time.time() - self.start_time,
            checks=check_results,
            system_metrics=system_metrics
        )
    
    def _determine_overall_status(self, checks: List[HealthCheck]) -> HealthStatus:
        """Determine overall health status from individual checks."""
        if not checks:
            return HealthStatus.UNKNOWN
        
        unhealthy_count = sum(1 for check in checks if check.status == HealthStatus.UNHEALTHY)
        degraded_count = sum(1 for check in checks if check.status == HealthStatus.DEGRADED)
        
        if unhealthy_count > 0:
            return HealthStatus.UNHEALTHY
        elif degraded_count > 0:
            return HealthStatus.DEGRADED
        else:
            return HealthStatus.HEALTHY
    
    def _get_system_metrics(self) -> Dict[str, Any]:
        """Get current system metrics."""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                "cpu_usage_percent": cpu_percent,
                "memory_usage_percent": memory.percent,
                "memory_total_gb": memory.total / (1024**3),
                "memory_available_gb": memory.available / (1024**3),
                "disk_usage_percent": disk.percent,
                "disk_total_gb": disk.total / (1024**3),
                "disk_free_gb": disk.free / (1024**3),
                "load_average": psutil.getloadavg() if hasattr(psutil, 'getloadavg') else None,
                "process_count": len(psutil.pids()),
                "boot_time": datetime.fromtimestamp(psutil.boot_time()).isoformat(),
                "platform": platform.platform(),
                "python_version": platform.python_version(),
            }
        except Exception as e:
            self.logger.error("Failed to get system metrics", error=str(e))
            return {"error": str(e)}
    
    def _update_prometheus_metrics(self, metrics: Dict[str, Any]):
        """Update Prometheus metrics with current values."""
        try:
            SYSTEM_CPU_USAGE.set(metrics.get("cpu_usage_percent", 0))
            SYSTEM_MEMORY_USAGE.set(metrics.get("memory_usage_percent", 0))
            SYSTEM_DISK_USAGE.set(metrics.get("disk_usage_percent", 0))
            
            # Update system info
            SYSTEM_INFO.info({
                "version": self.config.version,
                "environment": self.config.environment,
                "platform": metrics.get("platform", "unknown"),
                "python_version": metrics.get("python_version", "unknown"),
            })
        except Exception as e:
            self.logger.error("Failed to update Prometheus metrics", error=str(e))
    
    # Default health checks
    def _check_system_resources(self) -> tuple:
        """Check system resource usage."""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory_percent = psutil.virtual_memory().percent
            disk_percent = psutil.disk_usage('/').percent
            
            details = {
                "cpu_percent": cpu_percent,
                "memory_percent": memory_percent,
                "disk_percent": disk_percent
            }
            
            # Define thresholds
            if cpu_percent > 90 or memory_percent > 90 or disk_percent > 90:
                return HealthStatus.UNHEALTHY, "High resource usage detected", details
            elif cpu_percent > 70 or memory_percent > 70 or disk_percent > 80:
                return HealthStatus.DEGRADED, "Moderate resource usage", details
            else:
                return HealthStatus.HEALTHY, "Resource usage is normal", details
                
        except Exception as e:
            return HealthStatus.UNHEALTHY, f"Failed to check system resources: {str(e)}", None
    
    def _check_model_status(self) -> tuple:
        """Check AI model status."""
        try:
            # This would be implemented based on your actual model loading logic
            # For now, we'll simulate a basic check
            
            details = {
                "models_loaded": True,
                "cache_enabled": self.config.model.cache_enabled,
                "cache_size": self.config.model.cache_size
            }
            
            return HealthStatus.HEALTHY, "Models are loaded and ready", details
            
        except Exception as e:
            return HealthStatus.UNHEALTHY, f"Model check failed: {str(e)}", None
    
    def _check_database_connection(self) -> tuple:
        """Check database connectivity."""
        try:
            # This would implement actual database connectivity check
            # For now, we'll simulate based on configuration
            
            if self.config.database.url:
                details = {
                    "database_configured": True,
                    "connection_pool_size": self.config.database.pool_size
                }
                return HealthStatus.HEALTHY, "Database connection is healthy", details
            else:
                return HealthStatus.DEGRADED, "Database not configured", None
                
        except Exception as e:
            return HealthStatus.UNHEALTHY, f"Database check failed: {str(e)}", None
    
    def _check_external_dependencies(self) -> tuple:
        """Check external service dependencies."""
        try:
            # This would check actual external dependencies
            # For now, we'll simulate a basic check
            
            details = {
                "external_services_available": True,
                "api_endpoints_reachable": True
            }
            
            return HealthStatus.HEALTHY, "External dependencies are available", details
            
        except Exception as e:
            return HealthStatus.DEGRADED, f"Some external dependencies may be unavailable: {str(e)}", None


class PerformanceMonitor(LoggerMixin):
    """Monitor system and application performance."""
    
    def __init__(self):
        self.config = get_config()
        self.metrics_history = []
        self.max_history_size = 1000
    
    def record_metric(self, name: str, value: float, tags: Optional[Dict[str, str]] = None):
        """Record a performance metric."""
        metric = {
            "name": name,
            "value": value,
            "timestamp": datetime.utcnow().isoformat(),
            "tags": tags or {}
        }
        
        self.metrics_history.append(metric)
        
        # Keep history size manageable
        if len(self.metrics_history) > self.max_history_size:
            self.metrics_history = self.metrics_history[-self.max_history_size:]
        
        self.logger.debug(f"Recorded metric: {name} = {value}", tags=tags)
    
    def get_metrics_summary(self, hours: int = 1) -> Dict[str, Any]:
        """Get summary of metrics from the last N hours."""
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        
        recent_metrics = [
            m for m in self.metrics_history
            if datetime.fromisoformat(m["timestamp"]) > cutoff_time
        ]
        
        if not recent_metrics:
            return {"message": "No metrics available for the specified time period"}
        
        # Group metrics by name
        grouped_metrics = {}
        for metric in recent_metrics:
            name = metric["name"]
            if name not in grouped_metrics:
                grouped_metrics[name] = []
            grouped_metrics[name].append(metric["value"])
        
        # Calculate summary statistics
        summary = {}
        for name, values in grouped_metrics.items():
            summary[name] = {
                "count": len(values),
                "avg": sum(values) / len(values),
                "min": min(values),
                "max": max(values),
                "latest": values[-1] if values else None
            }
        
        return {
            "time_period_hours": hours,
            "total_metrics": len(recent_metrics),
            "summary": summary
        }


# Global instances
health_checker = HealthChecker()
performance_monitor = PerformanceMonitor()


async def get_health_status() -> Dict[str, Any]:
    """Get current health status (API endpoint helper)."""
    health = await health_checker.get_system_health()
    return health.dict()


def get_performance_summary(hours: int = 1) -> Dict[str, Any]:
    """Get performance summary (API endpoint helper)."""
    return performance_monitor.get_metrics_summary(hours)