"""
Performance Monitor v1 router for metrics collection, analysis, and alerting.
Provides comprehensive performance monitoring with real-time alerts and recommendations.
"""

import asyncio
import json
import os
import time
import uuid
from collections import defaultdict, deque
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List

import numpy as np
import psutil
from fastapi import APIRouter, HTTPException, Query, BackgroundTasks, status
from pydantic import BaseModel

# Import shared standards
import sys
from pathlib import Path
SERVICE_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = SERVICE_DIR.parent.parent
for p in (SERVICE_DIR, REPO_ROOT):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

try:
    from _shared.api_standards.error_schemas import raise_http_error
    from _shared.api_standards.pagination import PaginatedResponse
except ImportError:
    # Fallback for legacy compatibility
    def raise_http_error(code: str, message: str, details: Optional[Dict] = None):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                          detail={"error": {"code": code, "message": message, "details": details or {}}})
    
    class PaginatedResponse(BaseModel):
        items: list
        total: int
        page: int = 1
        size: int = 10

# Import models
from ..models import (
    AlertLevel,
    MetricType,
    PerformanceMetric,
    PerformanceAlert,
    MetricRequest,
    MetricRecordResponse,
    ServiceSummaryResponse,
    AlertsResponse,
    MetricsResponse,
    SystemMetrics,
    OverallSystemHealth,
    PerformanceReport,
    ResponseTimeAnalysis,
    MemoryAnalysis
)

router = APIRouter(tags=["Performance Monitor"], prefix="/v1")


class PerformanceAnalyzer:
    """Analyzes performance metrics and generates insights."""
    
    def __init__(self):
        self.thresholds = {
            MetricType.RESPONSE_TIME: {
                AlertLevel.WARNING: 500,
                AlertLevel.CRITICAL: 2000
            },
            MetricType.MEMORY_USAGE: {
                AlertLevel.WARNING: 80,
                AlertLevel.CRITICAL: 95
            },
            MetricType.CPU_USAGE: {
                AlertLevel.WARNING: 70,
                AlertLevel.CRITICAL: 90
            },
            MetricType.ERROR_RATE: {
                AlertLevel.WARNING: 5,
                AlertLevel.CRITICAL: 15
            }
        }
    
    def analyze_response_time_trend(self, metrics: List[PerformanceMetric]) -> ResponseTimeAnalysis:
        """Analyze response time trends."""
        if not metrics:
            return ResponseTimeAnalysis(
                trend="no_data",
                recommendation="Need more data points"
            )
        
        response_times = [m.value for m in metrics if m.metric_type == MetricType.RESPONSE_TIME]
        if len(response_times) < 5:
            return ResponseTimeAnalysis(
                trend="insufficient_data",
                recommendation="Collect more data points"
            )
        
        # Calculate trend
        x = np.arange(len(response_times))
        slope = np.polyfit(x, response_times, 1)[0]
        
        avg_response_time = np.mean(response_times)
        p95_response_time = np.percentile(response_times, 95)
        
        trend = "improving" if slope < -10 else "degrading" if slope > 10 else "stable"
        
        return ResponseTimeAnalysis(
            trend=trend,
            slope=slope,
            average_ms=avg_response_time,
            p95_ms=p95_response_time,
            min_ms=min(response_times),
            max_ms=max(response_times),
            recommendation=self._get_response_time_recommendation(avg_response_time, p95_response_time, slope)
        )
    
    def _get_response_time_recommendation(self, avg: float, p95: float, slope: float) -> str:
        """Generate response time optimization recommendations."""
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
    
    def analyze_memory_pattern(self, metrics: List[PerformanceMetric]) -> MemoryAnalysis:
        """Analyze memory usage patterns."""
        memory_metrics = [m for m in metrics if m.metric_type == MetricType.MEMORY_USAGE]
        if not memory_metrics:
            return MemoryAnalysis(status="no_data", recommendation="No memory data available")
        
        memory_values = [m.value for m in memory_metrics]
        
        # Check for memory leak pattern
        if len(memory_values) >= 10:
            recent_trend = np.polyfit(range(len(memory_values[-10:])), memory_values[-10:], 1)[0]
            if recent_trend > 1:
                return MemoryAnalysis(
                    status="memory_leak_suspected",
                    trend=recent_trend,
                    average_percent=np.mean(memory_values),
                    peak_percent=max(memory_values),
                    recommendation="Investigate potential memory leaks, check for unreleased resources"
                )
        
        avg_memory = np.mean(memory_values)
        max_memory = max(memory_values)
        
        status = "normal" if max_memory < 80 else "high_usage"
        
        return MemoryAnalysis(
            status=status,
            average_percent=avg_memory,
            peak_percent=max_memory,
            recommendation=self._get_memory_recommendation(avg_memory, max_memory)
        )
    
    def _get_memory_recommendation(self, avg: float, peak: float) -> str:
        """Generate memory optimization recommendations."""
        if peak > 90:
            return "Critical: Increase available memory or optimize memory usage"
        elif peak > 80:
            return "Consider memory optimization or scaling up resources"
        elif avg > 60:
            return "Monitor closely - approaching high memory usage"
        else:
            return "Memory usage is within normal range"


class PerformanceMonitor:
    """Main performance monitoring service."""
    
    def __init__(self):
        self.redis = None
        self.metrics_buffer = deque(maxlen=10000)
        self.alerts_buffer = deque(maxlen=1000)
        self.analyzer = PerformanceAnalyzer()
        self.service_metrics = defaultdict(lambda: defaultdict(list))
        self.alert_cooldowns = {}
        
    async def initialize_redis(self):
        """Initialize Redis connection."""
        try:
            import aioredis
            self.redis = await aioredis.from_url("redis://localhost:6379")
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Redis connection failed: {e}")
    
    async def record_metric(self, metric: PerformanceMetric):
        """Record a performance metric."""
        self.metrics_buffer.append(metric)
        self.service_metrics[metric.service_name][metric.metric_type].append(metric)
        
        # Keep only recent metrics
        if len(self.service_metrics[metric.service_name][metric.metric_type]) > 1000:
            self.service_metrics[metric.service_name][metric.metric_type] = \
                self.service_metrics[metric.service_name][metric.metric_type][-1000:]
        
        # Store in Redis if available
        if self.redis:
            try:
                await self.redis.lpush(
                    f"metrics:{metric.service_name}:{metric.metric_type}",
                    json.dumps(metric.dict(), default=str)
                )
                await self.redis.ltrim(f"metrics:{metric.service_name}:{metric.metric_type}", 0, 999)
            except Exception:
                pass
        
        await self._check_alert_conditions(metric)
    
    async def _check_alert_conditions(self, metric: PerformanceMetric):
        """Check if metric triggers any alerts."""
        thresholds = self.analyzer.thresholds.get(metric.metric_type)
        if not thresholds:
            return
        
        # Check cooldown
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
        """Generate alert message."""
        messages = {
            MetricType.RESPONSE_TIME: f"{level.value.title()}: High response time ({metric.value:.0f}ms) on {metric.service_name}",
            MetricType.MEMORY_USAGE: f"{level.value.title()}: High memory usage ({metric.value:.1f}%) on {metric.service_name}",
            MetricType.CPU_USAGE: f"{level.value.title()}: High CPU usage ({metric.value:.1f}%) on {metric.service_name}",
            MetricType.ERROR_RATE: f"{level.value.title()}: High error rate ({metric.value:.1f}%) on {metric.service_name}"
        }
        
        base_message = messages.get(metric.metric_type, f"{level.value.title()}: Performance issue on {metric.service_name}")
        
        if metric.endpoint:
            base_message += f" (endpoint: {metric.endpoint})"
        
        return base_message
    
    async def _send_alert(self, alert: PerformanceAlert):
        """Send performance alert."""
        self.alerts_buffer.append(alert)
        
        if self.redis:
            try:
                await self.redis.lpush("alerts:performance", json.dumps(alert.dict(), default=str))
                await self.redis.ltrim("alerts:performance", 0, 999)
            except Exception:
                pass
    
    async def get_service_summary(self, service_name: str, hours: int = 24) -> ServiceSummaryResponse:
        """Get performance summary for a service."""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        service_metrics = []
        for metric_type, metrics in self.service_metrics[service_name].items():
            recent_metrics = [m for m in metrics if m.timestamp >= cutoff_time]
            service_metrics.extend(recent_metrics)
        
        if not service_metrics:
            return ServiceSummaryResponse(
                service_name=service_name,
                time_range_hours=hours,
                response_time=ResponseTimeAnalysis(trend="no_data", recommendation="No data available"),
                memory=MemoryAnalysis(status="no_data", recommendation="No data available"),
                error_rate_percent=0,
                total_requests=0,
                recommendations=["No data available for analysis"]
            )
        
        # Analyze metrics
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
        
        return ServiceSummaryResponse(
            service_name=service_name,
            time_range_hours=hours,
            response_time=response_time_analysis,
            memory=memory_analysis,
            error_rate_percent=error_rate,
            total_requests=total_requests,
            recommendations=self._generate_service_recommendations(response_time_analysis, memory_analysis, error_rate)
        )
    
    def _generate_service_recommendations(self, response_analysis: ResponseTimeAnalysis, memory_analysis: MemoryAnalysis, error_rate: float) -> List[str]:
        """Generate service recommendations."""
        recommendations = []
        
        if response_analysis.average_ms and response_analysis.average_ms > 500:
            recommendations.append("Implement API response caching to reduce response times")
        
        if response_analysis.p95_ms and response_analysis.p95_ms > 1000:
            recommendations.append("Optimize slow database queries and add appropriate indexes")
        
        if memory_analysis.status == "memory_leak_suspected":
            recommendations.append("Investigate potential memory leaks in application code")
        
        if memory_analysis.peak_percent and memory_analysis.peak_percent > 80:
            recommendations.append("Consider scaling up memory resources or optimizing memory usage")
        
        if error_rate > 5:
            recommendations.append("High error rate detected - review application logs and fix recurring errors")
        
        if not recommendations:
            recommendations.append("Performance is within acceptable range - continue monitoring")
        
        return recommendations


# Global monitor instance
monitor = PerformanceMonitor()

# API Endpoints
@router.post("/metrics", response_model=MetricRecordResponse)
async def record_metric(metric_request: MetricRequest):
    """
    Record a custom performance metric.
    
    Allows services to submit custom performance metrics for monitoring.
    """
    try:
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
        
        return MetricRecordResponse(
            message="Metric recorded successfully",
            metric_id=metric.id
        )
        
    except Exception as e:
        raise_http_error("METRIC_RECORDING_FAILED", f"Failed to record metric: {str(e)}")


@router.get("/services/{service_name}/summary", response_model=ServiceSummaryResponse)
async def get_service_summary(
    service_name: str,
    hours: int = Query(24, description="Time range in hours", ge=1, le=168)
):
    """
    Get performance summary for a service.
    
    Returns comprehensive analysis including trends and recommendations.
    """
    try:
        summary = await monitor.get_service_summary(service_name, hours)
        return summary
        
    except Exception as e:
        raise_http_error("SERVICE_SUMMARY_FAILED", f"Failed to get service summary: {str(e)}")


@router.get("/alerts", response_model=AlertsResponse)
async def get_recent_alerts(limit: int = Query(50, description="Maximum number of alerts", ge=1, le=1000)):
    """
    Get recent performance alerts.
    
    Returns latest performance alerts across all services.
    """
    try:
        recent_alerts = list(monitor.alerts_buffer)[-limit:]
        alerts_list = [alert for alert in reversed(recent_alerts)]
        
        return AlertsResponse(
            alerts=alerts_list,
            total=len(alerts_list)
        )
        
    except Exception as e:
        raise_http_error("ALERTS_RETRIEVAL_FAILED", f"Failed to retrieve alerts: {str(e)}")


@router.get("/services/{service_name}/metrics/{metric_type}", response_model=MetricsResponse)
async def get_service_metrics(
    service_name: str,
    metric_type: MetricType,
    limit: int = Query(100, description="Maximum number of metrics", ge=1, le=1000)
):
    """
    Get recent metrics for a service and metric type.
    
    Returns time-series data for specific metric types.
    """
    try:
        metrics = monitor.service_metrics[service_name][metric_type][-limit:]
        
        return MetricsResponse(
            metrics=metrics,
            total=len(metrics),
            service_name=service_name,
            metric_type=metric_type
        )
        
    except Exception as e:
        raise_http_error("METRICS_RETRIEVAL_FAILED", f"Failed to retrieve metrics: {str(e)}")


@router.get("/system/metrics", response_model=SystemMetrics)
async def get_system_metrics():
    """
    Get current system performance metrics.
    
    Returns real-time system resource usage.
    """
    try:
        # Get system metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Get load average if available
        load_avg = None
        if hasattr(os, 'getloadavg'):
            load_avg = list(os.getloadavg())
        
        # Calculate uptime
        uptime_seconds = time.time() - psutil.boot_time()
        uptime_hours = uptime_seconds / 3600
        
        return SystemMetrics(
            cpu_usage_percent=cpu_percent,
            memory_usage_percent=memory.percent,
            disk_usage_percent=round((disk.used / disk.total) * 100, 2),
            load_average=load_avg,
            uptime_hours=round(uptime_hours, 2)
        )
        
    except Exception as e:
        raise_http_error("SYSTEM_METRICS_FAILED", f"Failed to get system metrics: {str(e)}")


@router.get("/services", response_model=PaginatedResponse)
async def list_monitored_services(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size")
):
    """
    List all monitored services.
    
    Returns paginated list of services with metrics.
    """
    try:
        services = list(monitor.service_metrics.keys())
        total = len(services)
        
        # Apply pagination
        start = (page - 1) * size
        end = start + size
        paginated_services = services[start:end]
        
        # Build service info
        service_info = []
        for service_name in paginated_services:
            metrics_count = sum(len(metrics) for metrics in monitor.service_metrics[service_name].values())
            metric_types = list(monitor.service_metrics[service_name].keys())
            
            service_info.append({
                "service_name": service_name,
                "total_metrics": metrics_count,
                "metric_types": metric_types,
                "last_seen": max(
                    (max(metrics, key=lambda m: m.timestamp).timestamp 
                     for metrics in monitor.service_metrics[service_name].values() if metrics),
                    default=None
                )
            })
        
        return PaginatedResponse(
            items=service_info,
            total=total,
            page=page,
            size=size
        )
        
    except Exception as e:
        raise_http_error("SERVICES_LIST_FAILED", f"Failed to list services: {str(e)}")


@router.get("/health/status")
async def get_monitor_health():
    """
    Get performance monitor health status.
    
    Returns health information about the monitoring service itself.
    """
    try:
        return {
            "status": "healthy",
            "service": "performance-monitor",
            "metrics_in_buffer": len(monitor.metrics_buffer),
            "alerts_in_buffer": len(monitor.alerts_buffer),
            "monitored_services": len(monitor.service_metrics),
            "redis_connected": monitor.redis is not None,
            "uptime_hours": round((time.time() - psutil.boot_time()) / 3600, 2)
        }
        
    except Exception as e:
        raise_http_error("HEALTH_CHECK_FAILED", f"Health check failed: {str(e)}")


# Initialize monitor on startup
async def initialize_monitor():
    """Initialize the performance monitor."""
    await monitor.initialize_redis()
