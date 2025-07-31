# PSI Runtime SDK - Enterprise Deployment Guide

## Overview

This guide covers enterprise deployment of the PSI Runtime SDK, including containerization, monitoring, security, and scalability considerations.

## Quick Start

### Development Environment

```bash
# Clone the repository
git clone https://github.com/reaganfue/PSI-Runtime-SDK.git
cd PSI-Runtime-SDK

# Start development environment
docker-compose -f docker-compose.dev.yml up

# Access the API
curl http://localhost:5000/health

# Access monitoring
open http://localhost:9090  # Prometheus
```

### Production Deployment

```bash
# Set environment variables
export JWT_SECRET_KEY="your-super-secret-jwt-key"
export API_KEYS="prod-key-1,prod-key-2"
export POSTGRES_PASSWORD="secure-db-password"
export SENTRY_DSN="your-sentry-dsn"
export ENCRYPTION_KEY="your-encryption-key"

# Deploy full stack
docker-compose up -d

# Check status
curl http://localhost/health
```

## Architecture

### Service Components

1. **API Server** (`psi-runtime-api`)
   - FastAPI-based REST API
   - Authentication and authorization
   - Rate limiting and security
   - Health checks and monitoring

2. **Metrics Server** (`psi-runtime-metrics`)
   - Prometheus metrics endpoint
   - Performance monitoring
   - Custom business metrics

3. **Database** (`postgres`)
   - PostgreSQL for persistent data
   - Connection pooling
   - SSL/TLS encryption

4. **Cache** (`redis`)
   - Redis for caching
   - Session storage
   - Rate limiting data

5. **Monitoring Stack**
   - **Prometheus**: Metrics collection
   - **Grafana**: Visualization and dashboards
   - **ELK Stack**: Log aggregation and analysis

6. **Reverse Proxy** (`nginx`)
   - SSL termination
   - Load balancing
   - Security headers

## Configuration

### Environment Files

The SDK supports multiple environments through configuration files:

- `.env.development` - Development settings
- `.env.production` - Production settings
- `.env` - Local overrides (gitignored)

### Key Configuration Sections

#### Security Configuration
```bash
JWT_SECRET_KEY=your-jwt-secret
API_KEYS=api-key-1,api-key-2
ENCRYPTION_KEY=your-encryption-key
RATE_LIMIT_PER_MINUTE=100
```

#### Database Configuration
```bash
DATABASE_URL=postgresql://user:pass@host:5432/db
DATABASE_POOL_SIZE=20
DATABASE_SSL_MODE=require
```

#### Monitoring Configuration
```bash
METRICS_ENABLED=true
SENTRY_DSN=your-sentry-dsn
LOG_LEVEL=INFO
PERFORMANCE_TRACKING=true
```

## Security

### Authentication

The SDK supports multiple authentication methods:

1. **JWT Tokens**
   ```bash
   # Generate a token
   python -m psi_runtime_sdk.cli security generate-token --user-id user123
   
   # Use in API calls
   curl -H "Authorization: Bearer your-jwt-token" http://localhost:5000/analyze/basic
   ```

2. **API Keys**
   ```bash
   # Generate an API key
   python -m psi_runtime_sdk.cli security generate-key --description "Production API"
   
   # Use in API calls
   curl -H "Authorization: your-api-key" http://localhost:5000/analyze/basic
   ```

### Rate Limiting

Built-in rate limiting protects against abuse:
- Default: 60 requests per minute per IP
- Configurable per endpoint
- Redis-backed for distributed deployments

### Security Headers

Production deployments include security headers:
- HTTPS enforcement
- CORS protection
- XSS protection
- Content type validation

## Monitoring and Observability

### Health Checks

```bash
# System health
curl http://localhost:5000/health

# CLI health check
python -m psi_runtime_sdk.cli health check
```

### Metrics

Access Prometheus metrics at `http://localhost:8000/metrics`:

```bash
# Custom business metrics
psi_runtime_requests_total
psi_runtime_model_inferences_total
psi_runtime_errors_total

# System metrics
psi_runtime_cpu_usage_percent
psi_runtime_memory_usage_percent
```

### Dashboards

Grafana dashboards are available at `http://localhost:3000`:
- System overview
- API performance
- Business metrics
- Error tracking

### Logging

Structured logging with multiple outputs:
- Console output (development)
- File logging (configurable)
- Sentry integration (errors)
- ELK stack (production)

## API Documentation

### Interactive Documentation

Access OpenAPI documentation:
- Development: `http://localhost:5000/docs`
- Production: Configure `API_DOCS_ENABLED=true`

### Key Endpoints

#### Analysis Endpoints
```bash
# Basic analysis
POST /analyze/basic
{
  "query": "Your text to analyze",
  "context": {},
  "options": {}
}

# Quantum analysis
POST /analyze/quantum
{
  "query": "Your text to analyze"
}

# Comprehensive analysis
POST /analyze/comprehensive
{
  "query": "Your text to analyze"
}
```

#### Management Endpoints
```bash
# Health check
GET /health

# Metrics summary
GET /metrics/summary?hours=24

# Model training
POST /model/train
{
  "training_data": [...],
  "config": {
    "learning_rate": 0.001,
    "epochs": 10
  }
}
```

## Performance Tuning

### Scaling Recommendations

1. **Horizontal Scaling**
   ```yaml
   # docker-compose.yml
   psi-runtime-api:
     deploy:
       replicas: 3
   ```

2. **Database Optimization**
   ```bash
   DATABASE_POOL_SIZE=20
   DATABASE_MAX_OVERFLOW=30
   ```

3. **Caching Strategy**
   ```bash
   MODEL_CACHE_ENABLED=true
   MODEL_CACHE_SIZE=1000
   ```

### Resource Requirements

#### Minimum Requirements
- CPU: 2 cores
- RAM: 4GB
- Storage: 20GB
- Network: 1Gbps

#### Recommended Production
- CPU: 8 cores
- RAM: 16GB
- Storage: 100GB SSD
- Network: 10Gbps

## Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Check package installation
   pip install -e .
   
   # Verify imports
   python -c "from psi_runtime_sdk import BasicResponseLogic"
   ```

2. **Database Connection Issues**
   ```bash
   # Check connection
   python -c "from psi_runtime_sdk.config import get_config; print(get_config().database.url)"
   
   # Test connection
   docker-compose exec postgres psql -U psi_user -d psi_runtime
   ```

3. **Memory Issues**
   ```bash
   # Monitor memory usage
   docker stats
   
   # Adjust model cache size
   MODEL_CACHE_SIZE=500
   ```

### Log Analysis

```bash
# View application logs
docker-compose logs psi-runtime-api

# Follow logs in real-time
docker-compose logs -f psi-runtime-api

# Structured log search in Kibana
# Access: http://localhost:5601
```

## Backup and Recovery

### Database Backup
```bash
# Create backup
docker-compose exec postgres pg_dump -U psi_user psi_runtime > backup.sql

# Restore backup
docker-compose exec -T postgres psql -U psi_user psi_runtime < backup.sql
```

### Configuration Backup
```bash
# Backup configurations
tar czf config-backup.tar.gz .env.* docker-compose.yml monitoring/
```

## Maintenance

### Updates
```bash
# Update to latest version
git pull origin main
docker-compose pull
docker-compose up -d

# Check health after update
python -m psi_runtime_sdk.cli health check
```

### Log Rotation
```bash
# Configure log rotation in production
# See monitoring/logstash/logstash.conf
```

## Support

### CLI Tools
```bash
# Show configuration
python -m psi_runtime_sdk.cli config show

# Generate API key
python -m psi_runtime_sdk.cli security generate-key

# Run analysis
python -m psi_runtime_sdk.cli analysis run "test query"
```

### Documentation
- API Documentation: `/docs` endpoint
- Configuration Reference: `psi_runtime_sdk/config.py`
- Code Examples: `examples/` directory

For additional support, see the GitHub repository issues or contact the development team.