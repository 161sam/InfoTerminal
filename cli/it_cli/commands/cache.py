"""Cache management and operations commands."""
from __future__ import annotations

import asyncio
from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console
from rich.table import Table

from ..config import get_settings
from ..http import client

app = typer.Typer(help="Cache Management & Operations")
console = Console()

def _run(action):
    asyncio.run(action())

@app.command()
def get(
    key: str = typer.Argument(..., help="Cache key"),
    decode: bool = typer.Option(False, "--decode", "-d", help="Decode value as JSON"),
) -> None:
    """Get value from cache."""
    settings = get_settings()

    async def _action():
        async with client() as c:
            resp = await c.get(f"{settings.cache_api}/v1/cache/{key}")
            
            if resp.status_code == 404:
                console.print(f"❌ Key not found: {key}")
                return
                
            resp.raise_for_status()
            data = resp.json()
            
            console.print(f"🔑 Cache Key: {key}")
            console.print(f"Value: {data.get('value', '')}")
            console.print(f"TTL: {data.get('ttl', 0)}s")
            console.print(f"Size: {data.get('size_bytes', 0)} bytes")
            console.print(f"Layer: {data.get('cache_layer', 'Unknown')}")
            
            if decode:
                try:
                    import json
                    decoded = json.loads(data.get('value', '{}'))
                    console.print("\n📋 Decoded JSON:")
                    console.print_json(data=decoded)
                except json.JSONDecodeError:
                    console.print("❌ Value is not valid JSON")

    _run(_action)

@app.command()
def set(
    key: str = typer.Argument(..., help="Cache key"),
    value: str = typer.Argument(..., help="Cache value"),
    ttl: Optional[int] = typer.Option(None, "--ttl", "-t", help="Time to live (seconds)"),
    layer: Optional[str] = typer.Option(None, "--layer", "-l", help="Cache layer: L1|L2|L3"),
    compress: bool = typer.Option(False, "--compress", "-c", help="Compress value"),
) -> None:
    """Set value in cache."""
    settings = get_settings()

    async def _action():
        payload = {
            "value": value,
            "compress": compress
        }
        if ttl:
            payload["ttl"] = ttl
        if layer:
            payload["layer"] = layer
            
        async with client() as c:
            resp = await c.put(f"{settings.cache_api}/v1/cache/{key}", json=payload)
            resp.raise_for_status()
            data = resp.json()
            
            console.print(f"✅ Cache key set: {key}")
            console.print(f"Layer: {data.get('cache_layer', 'Auto')}")
            console.print(f"Size: {data.get('size_bytes', 0)} bytes")
            console.print(f"Compressed: {'Yes' if data.get('compressed', False) else 'No'}")
            console.print(f"TTL: {data.get('ttl', 'Never')}s")

    _run(_action)

@app.command()
def delete(
    key: str = typer.Argument(..., help="Cache key to delete"),
    pattern: bool = typer.Option(False, "--pattern", "-p", help="Treat key as pattern"),
) -> None:
    """Delete key(s) from cache."""
    settings = get_settings()

    async def _action():
        if pattern:
            # Delete by pattern
            payload = {"pattern": key}
            async with client() as c:
                resp = await c.post(f"{settings.cache_api}/v1/cache/invalidate", json=payload)
                resp.raise_for_status()
                data = resp.json()
                
                console.print(f"🗑️  Deleted keys matching pattern: {key}")
                console.print(f"Count: {data.get('deleted_count', 0)}")
        else:
            # Delete single key
            async with client() as c:
                resp = await c.delete(f"{settings.cache_api}/v1/cache/{key}")
                
                if resp.status_code == 404:
                    console.print(f"❌ Key not found: {key}")
                    return
                    
                resp.raise_for_status()
                console.print(f"🗑️  Cache key deleted: {key}")

    _run(_action)

@app.command()
def keys(
    pattern: Optional[str] = typer.Option(None, "--pattern", "-p", help="Key pattern"),
    layer: Optional[str] = typer.Option(None, "--layer", "-l", help="Cache layer"),
    limit: int = typer.Option(100, "--limit", help="Results limit"),
) -> None:
    """List cache keys."""
    settings = get_settings()

    async def _action():
        params = {"limit": limit}
        if pattern:
            params["pattern"] = pattern
        if layer:
            params["layer"] = layer
            
        async with client() as c:
            resp = await c.get(f"{settings.cache_api}/v1/cache", params=params)
            resp.raise_for_status()
            data = resp.json()
            
            table = Table(title=f"Cache Keys ({data.get('total', 0)})")
            table.add_column("Key")
            table.add_column("Layer")
            table.add_column("Size")
            table.add_column("TTL")
            table.add_column("Last Access")
            
            for item in data.get("items", []):
                ttl_str = f"{item.get('ttl', 0)}s" if item.get('ttl') else "Never"
                table.add_row(
                    item.get("key", "")[:50],
                    item.get("layer", ""),
                    str(item.get("size_bytes", 0)),
                    ttl_str,
                    item.get("last_access", ""),
                )
            
            console.print(table)

    _run(_action)

@app.command()
def bulk(
    action: str = typer.Argument(..., help="Action: set|get|delete"),
    file: typer.FileText = typer.Argument(..., help="JSON file with key-value pairs"),
    ttl: Optional[int] = typer.Option(None, "--ttl", "-t", help="TTL for bulk set"),
) -> None:
    """Bulk cache operations."""
    settings = get_settings()

    async def _action():
        import json
        
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            console.print("❌ Invalid JSON file")
            return
        
        if action == "set":
            # Bulk set
            payload = {"items": data}
            if ttl:
                payload["ttl"] = ttl
                
            async with client() as c:
                resp = await c.post(f"{settings.cache_api}/v1/cache/bulk", json=payload)
                resp.raise_for_status()
                result = resp.json()
                
                console.print(f"✅ Bulk set completed")
                console.print(f"Success: {result.get('success_count', 0)}")
                console.print(f"Failed: {result.get('failed_count', 0)}")
                
                if result.get("errors"):
                    console.print("❌ Errors:")
                    for error in result.get("errors", []):
                        console.print(f"  {error.get('key', '')}: {error.get('message', '')}")
                        
        elif action == "get":
            # Bulk get
            keys = data if isinstance(data, list) else list(data.keys())
            
            async with client() as c:
                resp = await c.post(f"{settings.cache_api}/v1/cache/bulk", json={"keys": keys})
                resp.raise_for_status()
                result = resp.json()
                
                table = Table(title="Bulk Get Results")
                table.add_column("Key")
                table.add_column("Found")
                table.add_column("Value")
                table.add_column("Size")
                
                for item in result.get("items", []):
                    found_icon = "✅" if item.get("found", False) else "❌"
                    value_preview = str(item.get("value", ""))[:30] + "..."
                    
                    table.add_row(
                        item.get("key", ""),
                        found_icon,
                        value_preview,
                        str(item.get("size_bytes", 0)),
                    )
                
                console.print(table)
                
        elif action == "delete":
            # Bulk delete
            keys = data if isinstance(data, list) else list(data.keys())
            
            async with client() as c:
                resp = await c.delete(f"{settings.cache_api}/v1/cache/bulk", json={"keys": keys})
                resp.raise_for_status()
                result = resp.json()
                
                console.print(f"🗑️  Bulk delete completed")
                console.print(f"Deleted: {result.get('deleted_count', 0)}")

    _run(_action)

@app.command()
def stats(
    layer: Optional[str] = typer.Option(None, "--layer", "-l", help="Specific cache layer"),
    detailed: bool = typer.Option(False, "--detailed", "-d", help="Detailed statistics"),
) -> None:
    """Show cache statistics."""
    settings = get_settings()

    async def _action():
        params = {}
        if layer:
            params["layer"] = layer
        if detailed:
            params["detailed"] = True
            
        async with client() as c:
            resp = await c.get(f"{settings.cache_api}/v1/cache/stats", params=params)
            resp.raise_for_status()
            data = resp.json()
            
            console.print("📊 Cache Statistics")
            
            # Overall stats
            overall = data.get("overall", {})
            console.print(f"Total Keys: {overall.get('total_keys', 0)}")
            console.print(f"Total Size: {overall.get('total_size_mb', 0)}MB")
            console.print(f"Hit Rate: {overall.get('hit_rate', 0):.1f}%")
            console.print(f"Memory Usage: {overall.get('memory_usage_mb', 0)}MB")
            
            # Layer breakdown
            if data.get("by_layer"):
                table = Table(title="By Cache Layer")
                table.add_column("Layer")
                table.add_column("Keys")
                table.add_column("Size")
                table.add_column("Hit Rate")
                table.add_column("Evictions")
                
                for layer_data in data.get("by_layer", []):
                    table.add_row(
                        layer_data.get("layer", ""),
                        str(layer_data.get("keys", 0)),
                        f"{layer_data.get('size_mb', 0)}MB",
                        f"{layer_data.get('hit_rate', 0):.1f}%",
                        str(layer_data.get("evictions", 0)),
                    )
                
                console.print(table)
            
            # Performance metrics
            if detailed and data.get("performance"):
                perf = data.get("performance", {})
                console.print(f"\n⚡ Performance:")
                console.print(f"  Avg Get Time: {perf.get('avg_get_time_ms', 0)}ms")
                console.print(f"  Avg Set Time: {perf.get('avg_set_time_ms', 0)}ms")
                console.print(f"  Operations/sec: {perf.get('ops_per_second', 0)}")

    _run(_action)

@app.command()
def warm(
    keys: List[str] = typer.Option([], "--key", "-k", help="Keys to warm"),
    pattern: Optional[str] = typer.Option(None, "--pattern", "-p", help="Key pattern to warm"),
    source: Optional[str] = typer.Option(None, "--source", "-s", help="Data source for warming"),
) -> None:
    """Warm cache with data."""
    settings = get_settings()

    async def _action():
        payload = {}
        if keys:
            payload["keys"] = keys
        if pattern:
            payload["pattern"] = pattern
        if source:
            payload["source"] = source
            
        if not any([keys, pattern, source]):
            console.print("❌ Specify --key, --pattern, or --source")
            return
            
        async with client() as c:
            resp = await c.post(f"{settings.cache_api}/v1/cache/warm", json=payload)
            resp.raise_for_status()
            data = resp.json()
            
            console.print("🔥 Cache warming completed")
            console.print(f"Warmed Keys: {data.get('warmed_count', 0)}")
            console.print(f"Failed: {data.get('failed_count', 0)}")
            console.print(f"Duration: {data.get('duration_ms', 0)}ms")
            
            if data.get("errors"):
                console.print("❌ Errors:")
                for error in data.get("errors", []):
                    console.print(f"  {error}")

    _run(_action)

@app.command()
def invalidate(
    pattern: str = typer.Argument(..., help="Pattern to invalidate"),
    layer: Optional[str] = typer.Option(None, "--layer", "-l", help="Specific cache layer"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show what would be invalidated"),
) -> None:
    """Invalidate cache entries by pattern."""
    settings = get_settings()

    async def _action():
        payload = {
            "pattern": pattern,
            "dry_run": dry_run
        }
        if layer:
            payload["layer"] = layer
            
        async with client() as c:
            resp = await c.post(f"{settings.cache_api}/v1/cache/invalidate", json=payload)
            resp.raise_for_status()
            data = resp.json()
            
            if dry_run:
                console.print(f"🔍 Would invalidate {data.get('match_count', 0)} keys:")
                for key in data.get("matching_keys", []):
                    console.print(f"  - {key}")
            else:
                console.print(f"🗑️  Invalidated {data.get('invalidated_count', 0)} keys")
                console.print(f"Pattern: {pattern}")

    _run(_action)

@app.command()
def health(
    layer: Optional[str] = typer.Option(None, "--layer", "-l", help="Specific cache layer"),
) -> None:
    """Check cache health."""
    settings = get_settings()

    async def _action():
        params = {}
        if layer:
            params["layer"] = layer
            
        async with client() as c:
            resp = await c.get(f"{settings.cache_api}/v1/cache/health", params=params)
            resp.raise_for_status()
            data = resp.json()
            
            console.print("🏥 Cache Health")
            
            # Overall health
            overall_health = data.get("overall_health", "Unknown")
            health_icon = "✅" if overall_health == "healthy" else "❌"
            console.print(f"Status: {health_icon} {overall_health}")
            
            # Layer health
            if data.get("layers"):
                table = Table(title="Layer Health")
                table.add_column("Layer")
                table.add_column("Status")
                table.add_column("Connection")
                table.add_column("Response Time")
                table.add_column("Memory")
                
                for layer_health in data.get("layers", []):
                    status_icon = "✅" if layer_health.get("healthy", False) else "❌"
                    
                    table.add_row(
                        layer_health.get("layer", ""),
                        f"{status_icon} {layer_health.get('status', '')}",
                        layer_health.get("connection_status", ""),
                        f"{layer_health.get('response_time_ms', 0)}ms",
                        f"{layer_health.get('memory_usage_percent', 0)}%",
                    )
                
                console.print(table)

    _run(_action)

@app.command()
def backup(
    output_file: Path = typer.Argument(..., help="Backup output file"),
    layer: Optional[str] = typer.Option(None, "--layer", "-l", help="Specific cache layer"),
    pattern: Optional[str] = typer.Option(None, "--pattern", "-p", help="Key pattern"),
    compress: bool = typer.Option(True, "--compress", "-c", help="Compress backup"),
) -> None:
    """Backup cache data."""
    settings = get_settings()

    async def _action():
        payload = {"compress": compress}
        if layer:
            payload["layer"] = layer
        if pattern:
            payload["pattern"] = pattern
            
        async with client() as c:
            resp = await c.post(f"{settings.cache_api}/v1/cache/backup", json=payload)
            resp.raise_for_status()
            
            # Save backup data
            output_file.write_bytes(resp.content)
            
            # Get metadata from headers
            key_count = resp.headers.get("X-Key-Count", "Unknown")
            backup_size = resp.headers.get("Content-Length", "Unknown")
            
            console.print(f"✅ Cache backup created")
            console.print(f"File: {output_file}")
            console.print(f"Keys: {key_count}")
            console.print(f"Size: {backup_size} bytes")

    _run(_action)

@app.command()
def restore(
    backup_file: Path = typer.Argument(..., help="Backup file to restore"),
    layer: Optional[str] = typer.Option(None, "--layer", "-l", help="Target cache layer"),
    overwrite: bool = typer.Option(False, "--overwrite", help="Overwrite existing keys"),
) -> None:
    """Restore cache data from backup."""
    if not backup_file.exists():
        console.print(f"❌ Backup file not found: {backup_file}")
        raise typer.Exit(1)

    settings = get_settings()

    async def _action():
        # Read backup file
        backup_data = backup_file.read_bytes()
        
        async with client() as c:
            files = {"backup": (backup_file.name, backup_data)}
            data = {"overwrite": overwrite}
            if layer:
                data["layer"] = layer
                
            resp = await c.post(
                f"{settings.cache_api}/v1/cache/restore",
                files=files,
                data=data
            )
            resp.raise_for_status()
            result = resp.json()
            
            console.print(f"✅ Cache restore completed")
            console.print(f"Restored Keys: {result.get('restored_count', 0)}")
            console.print(f"Skipped: {result.get('skipped_count', 0)}")
            console.print(f"Failed: {result.get('failed_count', 0)}")
            
            if result.get("errors"):
                console.print("❌ Errors:")
                for error in result.get("errors", []):
                    console.print(f"  {error}")

    _run(_action)

@app.command()
def flush(
    layer: Optional[str] = typer.Option(None, "--layer", "-l", help="Specific cache layer"),
    confirm: bool = typer.Option(False, "--confirm", "-y", help="Confirm flush operation"),
) -> None:
    """Flush/clear cache."""
    if not confirm:
        confirm_flush = typer.confirm("Are you sure you want to flush the cache?")
        if not confirm_flush:
            console.print("❌ Operation cancelled")
            return

    settings = get_settings()

    async def _action():
        payload = {}
        if layer:
            payload["layer"] = layer
            
        async with client() as c:
            resp = await c.post(f"{settings.cache_api}/v1/cache/flush", json=payload)
            resp.raise_for_status()
            data = resp.json()
            
            console.print("🧹 Cache flushed")
            console.print(f"Cleared Keys: {data.get('cleared_count', 0)}")
            console.print(f"Freed Memory: {data.get('freed_memory_mb', 0)}MB")

    _run(_action)

@app.command()
def analytics(
    period: str = typer.Option("24h", "--period", "-p", help="Analysis period"),
    metric: Optional[str] = typer.Option(None, "--metric", "-m", help="Specific metric"),
) -> None:
    """Show cache analytics."""
    settings = get_settings()

    async def _action():
        params = {"period": period}
        if metric:
            params["metric"] = metric
            
        async with client() as c:
            resp = await c.get(f"{settings.cache_api}/v1/cache/analytics", params=params)
            resp.raise_for_status()
            data = resp.json()
            
            console.print(f"📈 Cache Analytics ({period})")
            
            # Performance trends
            if data.get("performance_trends"):
                table = Table(title="Performance Trends")
                table.add_column("Metric")
                table.add_column("Current")
                table.add_column("Average")
                table.add_column("Trend")
                
                for trend in data.get("performance_trends", []):
                    direction = trend.get("trend_direction", "stable")
                    trend_icon = "📈" if direction == "up" else "📉" if direction == "down" else "➡️"
                    
                    table.add_row(
                        trend.get("metric", ""),
                        str(trend.get("current_value", 0)),
                        str(trend.get("average_value", 0)),
                        f"{trend_icon} {direction}",
                    )
                
                console.print(table)
            
            # Usage patterns
            if data.get("usage_patterns"):
                patterns = data.get("usage_patterns", {})
                console.print(f"\n🔍 Usage Patterns:")
                console.print(f"  Peak Hour: {patterns.get('peak_hour', 'Unknown')}")
                console.print(f"  Most Active Layer: {patterns.get('most_active_layer', 'Unknown')}")
                console.print(f"  Hot Keys: {', '.join(patterns.get('hot_keys', [])[:5])}")

    _run(_action)
