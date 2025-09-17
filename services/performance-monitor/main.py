"""
Performance Monitoring Service

Monitors API response times, memory usage, and system performance metrics.
Provides alerts and optimization recommendations.
"""

from fastapi import FastAPI, BackgroundTasks, Request, Response
from fastapi.middleware.base import BaseHTTPMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import time
import psutil
import asyncio
import aioredis
import json
import logging
import os
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
import numpy as np
from enum import Enum
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Performance Monitor Service", version="1.0.0")

class AlertLevel(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

class MetricType(str, Enum):
    RESPONSE_TIME = "response_time"
    MEMORY_USAGE = "memory_usage"
    CPU_USAGE = "cpu_usage"
    ERROR_RATE = "error_rate"
    THROUGHPUT = "throughput"
    DATABASE_LATENCY = "database_latency"

@dataclass
class PerformanceMetric:
    """Individual performance metric"""
    id: str
    timestamp: datetime
    metric_type: MetricType
    value: float
    service_name: str
    endpoint: Optional[str] = None
    user_id: Optional[str] = None
    request_id: Optional[str] = None
    metadata: Dict[str, Any] = None

@dataclass
class PerformanceAlert:
    """Performance alert"""
    id: str
    timestamp: datetime
    level: AlertLevel
    metric_type: MetricType
    message: str
    threshold_value: float
    actual_value: float
    service_name: str
    endpoint: Optional[str] = None
    resolved: bool = False
    resolved_at: Optional[datetime] = None

class PerformanceAnalyzer:
    """Analyzes performance metrics and generates insights"""
    
    def __init__(self):
        self.thresholds = {
            MetricType.RESPONSE_TIME: {
                AlertLevel.WARNING: 500,  # 500ms
                AlertLevel.CRITICAL: 2000  # 2 seconds
            },
            MetricType.MEMORY_USAGE: {
                AlertLevel.WARNING: 80,  # 80% memory usage
                AlertLevel.CRITICAL: 95  # 95% memory usage
            },
            MetricType.CPU_USAGE: {
                AlertLevel.WARNING: 70,  # 70% CPU usage
                AlertLevel.CRITICAL: 90  # 90% CPU usage
            },
            MetricType.ERROR_RATE: {
                AlertLevel.WARNING: 5,   # 5% error rate
                AlertLevel.CRITICAL: 15  # 15% error rate
            }
        }
    
    def analyze_response_time_trend(self, metrics: List[PerformanceMetric]) -> Dict[str, Any]:
        """Analyze response time trends"""
        if not metrics:
            return {"trend": "no_data", "recommendation": "Need more data points"}
        
        response_times = [m.value for m in metrics if m.metric_type == MetricType.RESPONSE_TIME]
        if len(response_times) < 5:
            return {"trend": "insufficient_data", "recommendation": "Collect more data points"}
        
        # Calculate trend
        x = np.arange(len(response_times))
        slope = np.polyfit(x, response_times, 1)[0]
        
        avg_response_time = np.mean(response_times)
        p95_response_time = np.percentile(response_times, 95)
        
        analysis = {
            "trend": "improving" if slope < -10 else "degrading" if slope > 10 else "stable",
            "slope": slope,
            "average_ms": avg_response_time,
            "p95_ms": p95_response_time,
            "min_ms": min(response_times),
            "max_ms": max(response_times),
            "recommendation": self._get_response_time_recommendation(avg_response_time, p95_response_time, slope)
        }
        
        return analysis
    
    def _get_response_time_recommendation(self, avg: float, p95: float, slope: float) -> str:
        """Generate response time optimization recommendations"""
        recommendations = []
        
        if avg > 1000:
            recommendations.append("Consider implementing API response caching")
        if p95 > 2000:
            recommendations.append("Investigate slow queries and optimize database operations")
        if slope > 10:
            recommendations.append("Response times are degrading - check for memory leaks or increased load")
        if avg > 500:
            recommendations.append("Implement background processing for heavy operations")
        
        return "; ".join(recommendations) if recommendations else "Performance is within acceptable range"
    
    def analyze_memory_pattern(self, metrics: List[PerformanceMetric]) -> Dict[str, Any]:
        """Analyze memory usage patterns"""
        memory_metrics = [m for m in metrics if m.metric_type == MetricType.MEMORY_USAGE]
        if not memory_metrics:
            return {"status": "no_data"}
        
        memory_values = [m.value for m in memory_metrics]
        
        # Check for memory leak pattern (steadily increasing memory)
        if len(memory_values) >= 10:
            recent_trend = np.polyfit(range(len(memory_values[-10:])), memory_values[-10:], 1)[0]
            if recent_trend > 1:  # Memory increasing by more than 1% per measurement
                return {
                    "status": "memory_leak_suspected",
                    "trend": recent_trend,
                    "recommendation": "Investigate potential memory leaks, check for unreleased resources"
                }
        
        avg_memory = np.mean(memory_values)
        max_memory = max(memory_values)
        
        return {
            "status": "normal" if max_memory < 80 else "high_usage",
            "average_percent": avg_memory,
            "peak_percent": max_memory,
            "recommendation": self._get_memory_recommendation(avg_memory, max_memory)
        }
    
    def _get_memory_recommendation(self, avg: float, peak: float) -> str:
        """Generate memory optimization recommendations"""
        if peak > 90:
            return "Critical: Increase available memory or optimize memory usage"
        elif peak > 80:
            return "Consider memory optimization or scaling up resources"
        elif avg > 60:
            return "Monitor closely - approaching high memory usage"
        else:
            return "Memory usage is within normal range"

class PerformanceMonitor:
    """Main performance monitoring service"""
    
    def __init__(self):
        self.redis = None
        self.metrics_buffer = deque(maxlen=10000)  # Keep last 10k metrics in memory
        self.alerts_buffer = deque(maxlen=1000)   # Keep last 1k alerts in memory
        self.analyzer = PerformanceAnalyzer()
        self.service_metrics = defaultdict(lambda: defaultdict(list))  # service -> metric_type -> values
        self.alert_cooldowns = {}  # Prevent alert spam
        
    async def initialize_redis(self):
        """Initialize Redis connection"""
        try:
            self.redis = await aioredis.from_url("redis://localhost:6379")
            logger.info("Connected to Redis for performance monitoring")
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}")
    
    async def record_metric(self, metric: PerformanceMetric):
        """Record a performance metric"""
        # Add to buffer
        self.metrics_buffer.append(metric)
        
        # Add to service-specific tracking
        self.service_metrics[metric.service_name][metric.metric_type].append(metric)
        
        # Keep only recent metrics (last 1000 per service/type)
        if len(self.service_metrics[metric.service_name][metric.metric_type]) > 1000:
            self.service_metrics[metric.service_name][metric.metric_type] = \
                self.service_metrics[metric.service_name][metric.metric_type][-1000:]
        
        # Store in Redis if available
        if self.redis:
            try:
                await self.redis.lpush(
                    f"metrics:{metric.service_name}:{metric.metric_type}",
                    json.dumps(asdict(metric), default=str)
                )
                # Keep only last 1000 metrics per service/type in Redis
                await self.redis.ltrim(f"metrics:{metric.service_name}:{metric.metric_type}", 0, 999)
            except Exception as e:
                logger.warning(f"Failed to store metric in Redis: {e}")
        
        # Check for alerts
        await self._check_alert_conditions(metric)
    
    async def _check_alert_conditions(self, metric: PerformanceMetric):
        """Check if metric triggers any alerts"""
        thresholds = self.analyzer.thresholds.get(metric.metric_type)
        if not thresholds:
            return
        
        # Check cooldown to prevent alert spam
        cooldown_key = f"{metric.service_name}:{metric.metric_type}"
        if cooldown_key in self.alert_cooldowns:
            if datetime.now() - self.alert_cooldowns[cooldown_key] < timedelta(minutes=5):
                return
        
        alert_level = None
        threshold_value = None
        
        if metric.value >= thresholds[AlertLevel.CRITICAL]:
            alert_level = AlertLevel.CRITICAL
            threshold_value = thresholds[AlertLevel.CRITICAL]
        elif metric.value >= thresholds[AlertLevel.WARNING]:
            alert_level = AlertLevel.WARNING
            threshold_value = thresholds[AlertLevel.WARNING]
        
        if alert_level:
            alert = PerformanceAlert(
                id=str(uuid.uuid4()),
                timestamp=datetime.now(),
                level=alert_level,
                metric_type=metric.metric_type,
                message=self._generate_alert_message(metric, alert_level),
                threshold_value=threshold_value,
                actual_value=metric.value,
                service_name=metric.service_name,
                endpoint=metric.endpoint
            )
            
            await self._send_alert(alert)
            self.alert_cooldowns[cooldown_key] = datetime.now()
    
    def _generate_alert_message(self, metric: PerformanceMetric, level: AlertLevel) -> str:
        """Generate human-readable alert message"""
        messages = {
            MetricType.RESPONSE_TIME: f"{level.value.title()}: High response time ({metric.value:.0f}ms) detected on {metric.service_name}",
            MetricType.MEMORY_USAGE: f"{level.value.title()}: High memory usage ({metric.value:.1f}%) on {metric.service_name}",
            MetricType.CPU_USAGE: f"{level.value.title()}: High CPU usage ({metric.value:.1f}%) on {metric.service_name}",
            MetricType.ERROR_RATE: f"{level.value.title()}: High error rate ({metric.value:.1f}%) on {metric.service_name}"
        }
        
        base_message = messages.get(metric.metric_type, f"{level.value.title()}: Performance issue on {metric.service_name}")
        
        if metric.endpoint:
            base_message += f" (endpoint: {metric.endpoint})"
        
        return base_message
    
    async def _send_alert(self, alert: PerformanceAlert):
        """Send performance alert"""
        self.alerts_buffer.append(alert)
        
        # Store in Redis
        if self.redis:
            try:
                await self.redis.lpush("alerts:performance", json.dumps(asdict(alert), default=str))
                await self.redis.ltrim("alerts:performance", 0, 999)
            except Exception as e:
                logger.warning(f"Failed to store alert in Redis: {e}")
        
        # Log alert
        logger.warning(f"Performance Alert [{alert.level}]: {alert.message}")
        
        # TODO: Send to external alerting system (Slack, PagerDuty, etc.)
    
    async def get_service_summary(self, service_name: str, hours: int = 24) -> Dict[str, Any]:
        """Get performance summary for a service"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        service_metrics = []
        for metric_type, metrics in self.service_metrics[service_name].items():
            recent_metrics = [m for m in metrics if m.timestamp >= cutoff_time]
            service_metrics.extend(recent_metrics)
        
        if not service_metrics:
            return {"service_name": service_name, "status": "no_data"}
        
        # Analyze different metric types
        response_time_analysis = self.analyzer.analyze_response_time_trend(
            [m for m in service_metrics if m.metric_type == MetricType.RESPONSE_TIME]
        )
        
        memory_analysis = self.analyzer.analyze_memory_pattern(
            [m for m in service_metrics if m.metric_type == MetricType.MEMORY_USAGE]
        )
        
        # Calculate error rate
        total_requests = len([m for m in service_metrics if m.metric_type == MetricType.RESPONSE_TIME])
        error_requests = len([m for m in service_metrics if m.metric_type == MetricType.ERROR_RATE])
        error_rate = (error_requests / total_requests * 100) if total_requests > 0 else 0
        
        return {
            "service_name": service_name,
            "time_range_hours": hours,
            "response_time": response_time_analysis,
            "memory": memory_analysis,
            "error_rate_percent": error_rate,
            "total_requests": total_requests,
            "recommendations": self._generate_service_recommendations(response_time_analysis, memory_analysis, error_rate)
        }
    
    def _generate_service_recommendations(self, response_analysis: Dict, memory_analysis: Dict, error_rate: float) -> List[str]:
        """Generate optimization recommendations for a service"""
        recommendations = []
        
        # Response time recommendations
        if response_analysis.get("average_ms", 0) > 500:
            recommendations.append("Implement API response caching to reduce response times")
        
        if response_analysis.get("p95_ms", 0) > 1000:
            recommendations.append("Optimize slow database queries and add appropriate indexes")
        
        # Memory recommendations
        if memory_analysis.get("status") == "memory_leak_suspected":
            recommendations.append("Investigate potential memory leaks in application code")
        
        if memory_analysis.get("peak_percent", 0) > 80:
            recommendations.append("Consider scaling up memory resources or optimizing memory usage")
        
        # Error rate recommendations
        if error_rate > 5:
            recommendations.append("High error rate detected - review application logs and fix recurring errors")
        
        # General recommendations
        if not recommendations:
            recommendations.append("Performance is within acceptable range - continue monitoring")
        
        return recommendations

# Performance monitoring middleware
class PerformanceMiddleware(BaseHTTPMiddleware):
    """Middleware to automatically track API performance metrics"""
    
    def __init__(self, app, monitor: PerformanceMonitor):
        super().__init__(app)
        self.monitor = monitor
    
    async def dispatch(self, request: Request, call_next):
        # Start timing
        start_time = time.time()
        request_id = str(uuid.uuid4())
        
        # Get user ID from request (if available)
        user_id = request.headers.get("X-User-ID")
        
        # Process request
        try:
            response = await call_next(request)
            
            # Record response time metric
            response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            await self.monitor.record_metric(PerformanceMetric(
                id=str(uuid.uuid4()),
                timestamp=datetime.now(),
                metric_type=MetricType.RESPONSE_TIME,
                value=response_time,
                service_name=os.getenv("SERVICE_NAME", "unknown"),
                endpoint=f"{request.method} {request.url.path}",
                user_id=user_id,
                request_id=request_id,
                metadata={
                    "status_code": response.status_code,
                    "user_agent": request.headers.get("user-agent"),
                    "request_size": len(await request.body()) if hasattr(request, "body") else 0
                }
            ))
            
            # Record error rate if applicable
            if response.status_code >= 400:
                await self.monitor.record_metric(PerformanceMetric(
                    id=str(uuid.uuid4()),
                    timestamp=datetime.now(),
                    metric_type=MetricType.ERROR_RATE,
                    value=1.0,  # Binary - either error or not
                    service_name=os.getenv("SERVICE_NAME", "unknown"),
                    endpoint=f"{request.method} {request.url.path}",
                    user_id=user_id,
                    request_id=request_id,
                    metadata={"status_code": response.status_code}
                ))
            
            return response
            
        except Exception as e:
            # Record error
            response_time = (time.time() - start_time) * 1000
            
            await self.monitor.record_metric(PerformanceMetric(
                id=str(uuid.uuid4()),
                timestamp=datetime.now(),
                metric_type=MetricType.ERROR_RATE,
                value=1.0,
                service_name=os.getenv("SERVICE_NAME", "unknown"),
                endpoint=f"{request.method} {request.url.path}",
                user_id=user_id,
                request_id=request_id,
                metadata={"error": str(e), "response_time_ms": response_time}
            ))
            
            raise e

# System metrics collector
class SystemMetricsCollector:
    """Collects system-level performance metrics"""
    
    def __init__(self, monitor: PerformanceMonitor):
        self.monitor = monitor
        self.service_name = os.getenv("SERVICE_NAME", "system")
        self.collection_interval = 30  # seconds
    
    async def start_collection(self):
        """Start collecting system metrics periodically"""
        while True:
            try:
                await self._collect_metrics()
                await asyncio.sleep(self.collection_interval)
            except Exception as e:
                logger.error(f"Error collecting system metrics: {e}")
                await asyncio.sleep(self.collection_interval)
    
    async def _collect_metrics(self):
        """Collect and record system metrics"""
        timestamp = datetime.now()
        
        # Memory usage
        memory = psutil.virtual_memory()
        await self.monitor.record_metric(PerformanceMetric(
            id=str(uuid.uuid4()),
            timestamp=timestamp,
            metric_type=MetricType.MEMORY_USAGE,
            value=memory.percent,
            service_name=self.service_name,
            metadata={
                "total_gb": round(memory.total / (1024**3), 2),
                "available_gb": round(memory.available / (1024**3), 2),
                "used_gb": round(memory.used / (1024**3), 2)
            }
        ))
        
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        await self.monitor.record_metric(PerformanceMetric(
            id=str(uuid.uuid4()),
            timestamp=timestamp,
            metric_type=MetricType.CPU_USAGE,
            value=cpu_percent,
            service_name=self.service_name,
            metadata={
                "cpu_count": psutil.cpu_count(),
                "load_average": os.getloadavg() if hasattr(os, 'getloadavg') else None
            }
        ))
        
        # Disk usage (for main partition)
        disk = psutil.disk_usage('/')
        await self.monitor.record_metric(PerformanceMetric(
            id=str(uuid.uuid4()),
            timestamp=timestamp,
            metric_type=MetricType.MEMORY_USAGE,  # Reusing this type for disk
            value=(disk.used / disk.total) * 100,
            service_name=f"{self.service_name}_disk",
            metadata={
                "total_gb": round(disk.total / (1024**3), 2),
                "used_gb": round(disk.used / (1024**3), 2),
                "free_gb": round(disk.free / (1024**3), 2)
            }
        ))

# Initialize services
monitor = PerformanceMonitor()
system_collector = SystemMetricsCollector(monitor)

# Pydantic models for API
class MetricRequest(BaseModel):
    metric_type: MetricType
    value: float
    service_name: str
    endpoint: Optional[str] = None
    user_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class ServiceSummaryResponse(BaseModel):
    service_name: str
    time_range_hours: int
    response_time: Dict[str, Any]
    memory: Dict[str, Any]
    error_rate_percent: float
    total_requests: int
    recommendations: List[str]

@app.on_event("startup")
async def startup_event():
    await monitor.initialize_redis()
    # Start system metrics collection in background
    asyncio.create_task(system_collector.start_collection())

# Add performance monitoring middleware
app.add_middleware(PerformanceMiddleware, monitor=monitor)

# API Endpoints
@app.post("/metrics")
async def record_metric(metric_request: MetricRequest):
    """Record a custom performance metric"""
    metric = PerformanceMetric(
        id=str(uuid.uuid4()),
        timestamp=datetime.now(),
        metric_type=metric_request.metric_type,
        value=metric_request.value,
        service_name=metric_request.service_name,
        endpoint=metric_request.endpoint,
        user_id=metric_request.user_id,
        metadata=metric_request.metadata
    )
    
    await monitor.record_metric(metric)
    return {"message": "Metric recorded successfully", "metric_id": metric.id}

@app.get("/metrics/{service_name}/summary", response_model=ServiceSummaryResponse)
async def get_service_summary(service_name: str, hours: int = 24):
    """Get performance summary for a service"""
    summary = await monitor.get_service_summary(service_name, hours)
    return summary

@app.get("/alerts")
async def get_recent_alerts(limit: int = 50):
    """Get recent performance alerts"""
    recent_alerts = list(monitor.alerts_buffer)[-limit:]
    return [asdict(alert) for alert in reversed(recent_alerts)]

@app.get("/metrics/{service_name}/{metric_type}")
async def get_metrics(service_name: str, metric_type: MetricType, limit: int = 100):
    """Get recent metrics for a service and metric type"""
    metrics = monitor.service_metrics[service_name][metric_type][-limit:]
    return [asdict(metric) for metric in metrics]

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "service": "performance-monitor",
        "metrics_in_buffer": len(monitor.metrics_buffer),
        "alerts_in_buffer": len(monitor.alerts_buffer)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)
