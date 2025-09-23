"""Performance monitoring and metrics commands."""
from __future__ import annotations

import asyncio
from typing import List, Optional

import typer
from rich.console import Console
from rich.table import Table

from ..config import get_settings
from ..http import client

app = typer.Typer(help="Performance Monitoring & Metrics")
console = Console()

def _run(action):
    asyncio.run(action())

@app.command()
def summary(
    service: Optional[str] = typer.Option(None, "--service", "-s", help="Specific service"),
    period: str = typer.Option("1h", "--period", "-p", help="Time period: 5m|15m|1h|6h|24h"),
) -> None:
    """Show performance summary."""
    settings = get_settings()

    async def _action():
        if service:
            # Service-specific summary
            params = {"period": period}
            async with client() as c:
                resp = await c.get(
                    f"{settings.performance_api}/v1/services/{service}/summary",
                    params=params
                )
                resp.raise_for_status()
                data = resp.json()
                
                console.print(f"📊 Performance Summary: {service} ({period})")
                
                # Key metrics
                metrics = data.get("metrics", {})
                console.print(f"Average Response Time: {metrics.get('avg_response_time', 0)}ms")
                console.print(f"Request Count: {metrics.get('request_count', 0)}")
                console.print(f"Error Rate: {metrics.get('error_rate', 0):.2f}%")
                console.print(f"Memory Usage: {metrics.get('memory_usage', 0)}MB")
                console.print(f"CPU Usage: {metrics.get('cpu_usage', 0):.1f}%")
                
                # Performance grade
                grade = data.get("performance_grade", "Unknown")
                console.print(f"Performance Grade: {grade}")
                
                # Recommendations
                if data.get("recommendations"):
                    console.print("\n💡 Recommendations:")
                    for rec in data.get("recommendations", []):
                        console.print(f"  • {rec}")
        else:
            # Overall system summary
            params = {"period": period}
            async with client() as c:
                resp = await c.get(f"{settings.performance_api}/v1/metrics", params=params)
                resp.raise_for_status()
                data = resp.json()
                
                console.print(f"📊 System Performance Summary ({period})")
                
                table = Table(title="Service Performance")
                table.add_column("Service")
                table.add_column("Avg Response")
                table.add_column("Requests")
                table.add_column("Errors")
                table.add_column("Memory")
                table.add_column("Grade")
                
                for service_data in data.get("services", []):
                    metrics = service_data.get("metrics", {})
                    table.add_row(
                        service_data.get("name", ""),
                        f"{metrics.get('avg_response_time', 0)}ms",
                        str(metrics.get('request_count', 0)),
                        f"{metrics.get('error_rate', 0):.1f}%",
                        f"{metrics.get('memory_usage', 0)}MB",
                        service_data.get("grade", ""),
                    )
                
                console.print(table)

    _run(_action)

@app.command()
def metrics(
    service: str = typer.Argument(..., help="Service name"),
    metric: Optional[str] = typer.Option(None, "--metric", "-m", help="Specific metric"),
    period: str = typer.Option("1h", "--period", "-p", help="Time period"),
    granularity: str = typer.Option("5m", "--granularity", "-g", help="Data granularity"),
) -> None:
    """Record and view service metrics."""
    settings = get_settings()

    async def _action():
        payload = {
            "service": service,
            "period": period,
            "granularity": granularity
        }
        if metric:
            payload["metric"] = metric
            
        async with client() as c:
            resp = await c.post(f"{settings.performance_api}/v1/metrics", json=payload)
            resp.raise_for_status()
            data = resp.json()
            
            console.print(f"📈 Metrics: {service}")
            
            if metric:
                # Single metric view
                metric_data = data.get("metric_data", [])
                
                table = Table(title=f"{metric} over {period}")
                table.add_column("Time")
                table.add_column("Value")
                table.add_column("Change")
                
                for point in metric_data:
                    change_str = ""
                    if point.get("change"):
                        change = point.get("change", 0)
                        change_str = f"+{change:.1f}" if change > 0 else f"{change:.1f}"
                    
                    table.add_row(
                        point.get("timestamp", ""),
                        str(point.get("value", 0)),
                        change_str,
                    )
                
                console.print(table)
            else:
                # All metrics overview
                table = Table(title="Current Metrics")
                table.add_column("Metric")
                table.add_column("Current")
                table.add_column("Average")
                table.add_column("Peak")
                table.add_column("Trend")
                
                for metric_info in data.get("metrics", []):
                    trend = metric_info.get("trend", "stable")
                    trend_icon = "📈" if trend == "up" else "📉" if trend == "down" else "➡️"
                    
                    table.add_row(
                        metric_info.get("name", ""),
                        str(metric_info.get("current", 0)),
                        str(metric_info.get("average", 0)),
                        str(metric_info.get("peak", 0)),
                        f"{trend_icon} {trend}",
                    )
                
                console.print(table)

    _run(_action)

@app.command()
def alerts(
    action: Optional[str] = typer.Argument(None, help="Action: list|create|update|delete"),
    alert_id: Optional[int] = typer.Option(None, "--id", help="Alert ID"),
    service: Optional[str] = typer.Option(None, "--service", "-s", help="Service name"),
    metric: Optional[str] = typer.Option(None, "--metric", "-m", help="Metric name"),
    threshold: Optional[float] = typer.Option(None, "--threshold", "-t", help="Alert threshold"),
    condition: Optional[str] = typer.Option(None, "--condition", "-c", help="Condition: gt|lt|eq"),
) -> None:
    """Manage performance alerts."""
    settings = get_settings()

    async def _action():
        if not action or action == "list":
            # List alerts
            params = {}
            if service:
                params["service"] = service
                
            async with client() as c:
                resp = await c.get(f"{settings.performance_api}/v1/alerts", params=params)
                resp.raise_for_status()
                data = resp.json()
                
                table = Table(title="Performance Alerts")
                table.add_column("ID")
                table.add_column("Service")
                table.add_column("Metric")
                table.add_column("Condition")
                table.add_column("Threshold")
                table.add_column("Status")
                
                for alert in data.get("alerts", []):
                    condition_str = f"{alert.get('condition', '')} {alert.get('threshold', '')}"
                    status_icon = "🔴" if alert.get("triggered", False) else "🟢"
                    
                    table.add_row(
                        str(alert.get("id", "")),
                        alert.get("service", ""),
                        alert.get("metric", ""),
                        condition_str,
                        str(alert.get("threshold", "")),
                        f"{status_icon} {alert.get('status', '')}",
                    )
                
                console.print(table)
                
        elif action == "create":
            # Create new alert
            if not all([service, metric, threshold, condition]):
                console.print("❌ Required: --service, --metric, --threshold, --condition")
                return
                
            payload = {
                "service": service,
                "metric": metric,
                "threshold": threshold,
                "condition": condition
            }
            
            async with client() as c:
                resp = await c.post(f"{settings.performance_api}/v1/alerts", json=payload)
                resp.raise_for_status()
                data = resp.json()
                
                console.print("✅ Alert created")
                console.print(f"ID: {data.get('id')}")
                console.print(f"Condition: {metric} {condition} {threshold}")
                
        elif action == "delete":
            # Delete alert
            if not alert_id:
                console.print("❌ Alert ID required for delete action")
                return
                
            async with client() as c:
                resp = await c.delete(f"{settings.performance_api}/v1/alerts/{alert_id}")
                resp.raise_for_status()
                console.print(f"🗑️  Alert {alert_id} deleted")

    _run(_action)

@app.command()
def system(
    component: Optional[str] = typer.Option(None, "--component", "-c", help="System component"),
    realtime: bool = typer.Option(False, "--realtime", "-r", help="Real-time monitoring"),
    duration: int = typer.Option(30, "--duration", "-d", help="Monitoring duration (seconds)"),
) -> None:
    """Monitor system-level metrics."""
    settings = get_settings()

    async def _action():
        if realtime:
            console.print(f"🔄 Real-time monitoring for {duration}s...")
            console.print("Press Ctrl+C to stop")
            
            try:
                import time
                start_time = time.time()
                
                while time.time() - start_time < duration:
                    params = {}
                    if component:
                        params["component"] = component
                        
                    async with client() as c:
                        resp = await c.get(f"{settings.performance_api}/v1/system/metrics", params=params)
                        resp.raise_for_status()
                        data = resp.json()
                        
                        # Clear screen and show current metrics
                        console.clear()
                        console.print(f"🖥️  System Metrics (Real-time)")
                        console.print(f"Time: {data.get('timestamp', '')}")
                        
                        metrics = data.get("metrics", {})
                        console.print(f"CPU: {metrics.get('cpu_percent', 0):.1f}%")
                        console.print(f"Memory: {metrics.get('memory_percent', 0):.1f}%")
                        console.print(f"Disk: {metrics.get('disk_percent', 0):.1f}%")
                        console.print(f"Network In: {metrics.get('network_in', 0)} MB/s")
                        console.print(f"Network Out: {metrics.get('network_out', 0)} MB/s")
                        
                        if metrics.get("services"):
                            console.print("\n🔧 Service Status:")
                            for svc in metrics.get("services", []):
                                status_icon = "🟢" if svc.get("healthy", False) else "🔴"
                                console.print(f"  {status_icon} {svc.get('name', '')}")
                    
                    await asyncio.sleep(2)  # Update every 2 seconds
                    
            except KeyboardInterrupt:
                console.print("\n⏹️  Monitoring stopped")
        else:
            # Single snapshot
            params = {}
            if component:
                params["component"] = component
                
            async with client() as c:
                resp = await c.get(f"{settings.performance_api}/v1/system/metrics", params=params)
                resp.raise_for_status()
                data = resp.json()
                
                console.print("🖥️  System Metrics Snapshot")
                
                metrics = data.get("metrics", {})
                
                table = Table(title="System Resources")
                table.add_column("Resource")
                table.add_column("Usage")
                table.add_column("Available")
                table.add_column("Total")
                
                table.add_row(
                    "CPU",
                    f"{metrics.get('cpu_percent', 0):.1f}%",
                    f"{100 - metrics.get('cpu_percent', 0):.1f}%",
                    f"{metrics.get('cpu_count', 0)} cores"
                )
                
                table.add_row(
                    "Memory",
                    f"{metrics.get('memory_used', 0)}MB",
                    f"{metrics.get('memory_available', 0)}MB",
                    f"{metrics.get('memory_total', 0)}MB"
                )
                
                table.add_row(
                    "Disk",
                    f"{metrics.get('disk_used', 0)}GB",
                    f"{metrics.get('disk_free', 0)}GB",
                    f"{metrics.get('disk_total', 0)}GB"
                )
                
                console.print(table)

    _run(_action)

@app.command()
def analyze(
    service: str = typer.Argument(..., help="Service name"),
    period: str = typer.Option("24h", "--period", "-p", help="Analysis period"),
    focus: Optional[str] = typer.Option(None, "--focus", "-f", help="Focus area: memory|cpu|response_time"),
) -> None:
    """Analyze service performance patterns."""
    settings = get_settings()

    async def _action():
        payload = {
            "service": service,
            "period": period
        }
        if focus:
            payload["focus"] = focus
            
        async with client() as c:
            resp = await c.post(f"{settings.performance_api}/v1/analyze", json=payload)
            resp.raise_for_status()
            data = resp.json()
            
            console.print(f"🔍 Performance Analysis: {service} ({period})")
            
            # Analysis summary
            analysis = data.get("analysis", {})
            console.print(f"Overall Health: {analysis.get('health_score', 0)}/100")
            console.print(f"Performance Grade: {analysis.get('grade', 'Unknown')}")
            
            # Key findings
            if analysis.get("findings"):
                console.print("\n🔎 Key Findings:")
                for finding in analysis.get("findings", []):
                    severity = finding.get("severity", "info")
                    icon = "🔴" if severity == "critical" else "🟡" if severity == "warning" else "ℹ️"
                    console.print(f"  {icon} {finding.get('message', '')}")
            
            # Recommendations
            if analysis.get("recommendations"):
                console.print("\n💡 Recommendations:")
                for rec in analysis.get("recommendations", []):
                    impact = rec.get("impact", "medium")
                    effort = rec.get("effort", "medium")
                    console.print(f"  • {rec.get('description', '')} (Impact: {impact}, Effort: {effort})")
            
            # Trend analysis
            if analysis.get("trends"):
                table = Table(title="Performance Trends")
                table.add_column("Metric")
                table.add_column("Trend")
                table.add_column("Change")
                table.add_column("Prediction")
                
                for trend in analysis.get("trends", []):
                    direction = trend.get("direction", "stable")
                    trend_icon = "📈" if direction == "improving" else "📉" if direction == "degrading" else "➡️"
                    
                    table.add_row(
                        trend.get("metric", ""),
                        f"{trend_icon} {direction}",
                        f"{trend.get('change_percent', 0):+.1f}%",
                        trend.get("prediction", ""),
                    )
                
                console.print(table)

    _run(_action)

@app.command()
def benchmark(
    service: str = typer.Argument(..., help="Service name"),
    duration: int = typer.Option(60, "--duration", "-d", help="Benchmark duration (seconds)"),
    concurrency: int = typer.Option(10, "--concurrency", "-c", help="Concurrent requests"),
    endpoint: Optional[str] = typer.Option(None, "--endpoint", "-e", help="Specific endpoint"),
) -> None:
    """Run performance benchmark."""
    settings = get_settings()

    async def _action():
        payload = {
            "service": service,
            "duration": duration,
            "concurrency": concurrency
        }
        if endpoint:
            payload["endpoint"] = endpoint
            
        console.print(f"🏃 Running benchmark: {service}")
        console.print(f"Duration: {duration}s, Concurrency: {concurrency}")
        
        async with client() as c:
            resp = await c.post(f"{settings.performance_api}/v1/benchmark", json=payload)
            resp.raise_for_status()
            data = resp.json()
            
            console.print("✅ Benchmark completed")
            
            results = data.get("results", {})
            console.print(f"Total Requests: {results.get('total_requests', 0)}")
            console.print(f"Successful: {results.get('successful_requests', 0)}")
            console.print(f"Failed: {results.get('failed_requests', 0)}")
            console.print(f"Requests/sec: {results.get('requests_per_second', 0):.1f}")
            
            # Response time statistics
            response_times = results.get("response_times", {})
            
            table = Table(title="Response Time Statistics")
            table.add_column("Percentile")
            table.add_column("Time (ms)")
            
            for percentile, time_ms in response_times.items():
                table.add_row(f"P{percentile}", f"{time_ms:.1f}")
            
            console.print(table)

    _run(_action)

@app.command()
def export(
    output_file: typer.FileText = typer.Argument(..., help="Output file"),
    service: Optional[str] = typer.Option(None, "--service", "-s", help="Specific service"),
    period: str = typer.Option("24h", "--period", "-p", help="Time period"),
    format: str = typer.Option("json", "--format", "-f", help="Export format: json|csv"),
) -> None:
    """Export performance data."""
    settings = get_settings()

    async def _action():
        params = {
            "period": period,
            "format": format
        }
        if service:
            params["service"] = service
            
        async with client() as c:
            resp = await c.get(f"{settings.performance_api}/v1/export", params=params)
            resp.raise_for_status()
            
            if format == "json":
                data = resp.json()
                import json
                json.dump(data, output_file, indent=2)
            else:
                # CSV format
                output_file.write(resp.text)
            
            console.print(f"✅ Performance data exported ({format.upper()})")
            console.print(f"Records: {resp.headers.get('X-Record-Count', 'Unknown')}")

    _run(_action)

@app.command()
def health() -> None:
    """Check performance monitoring service health."""
    settings = get_settings()

    async def _action():
        async with client() as c:
            resp = await c.get(f"{settings.performance_api}/healthz")
            resp.raise_for_status()
            data = resp.json()
            
            console.print("🏥 Performance Monitoring Health")
            console.print_json(data=data)

    _run(_action)
