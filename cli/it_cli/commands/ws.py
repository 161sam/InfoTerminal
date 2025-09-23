"""WebSocket and real-time communication commands."""
from __future__ import annotations

import asyncio
from typing import List, Optional

import typer
from rich.console import Console
from rich.table import Table

from ..config import get_settings
from ..http import client

app = typer.Typer(help="WebSocket & Real-time Communication")
console = Console()

def _run(action):
    asyncio.run(action())

@app.command()
def token(
    client_id: Optional[str] = typer.Option(None, "--client-id", "-c", help="Client ID"),
    channels: List[str] = typer.Option([], "--channel", help="Channels to subscribe"),
    ttl: Optional[int] = typer.Option(None, "--ttl", "-t", help="Token TTL (seconds)"),
) -> None:
    """Generate WebSocket connection token."""
    settings = get_settings()

    async def _action():
        payload = {}
        if client_id:
            payload["client_id"] = client_id
        if channels:
            payload["channels"] = channels
        if ttl:
            payload["ttl"] = ttl
            
        async with client() as c:
            resp = await c.post(f"{settings.websocket_api}/v1/ws/token", json=payload)
            resp.raise_for_status()
            data = resp.json()
            
            console.print("🎫 WebSocket Token Generated")
            console.print(f"Token: {data.get('token', '')}")
            console.print(f"Client ID: {data.get('client_id', '')}")
            console.print(f"Expires: {data.get('expires_at', '')}")
            console.print(f"WebSocket URL: {data.get('websocket_url', '')}")
            
            if data.get("channels"):
                channels_str = ", ".join(data.get("channels", []))
                console.print(f"Channels: {channels_str}")

    _run(_action)

@app.command()
def connect(
    token: str = typer.Argument(..., help="WebSocket token"),
    duration: int = typer.Option(30, "--duration", "-d", help="Connection duration (seconds)"),
    debug: bool = typer.Option(False, "--debug", help="Enable debug output"),
) -> None:
    """Connect to WebSocket and listen for messages."""
    settings = get_settings()

    async def _action():
        try:
            import websockets
            import json
            import time
            
            # Extract WebSocket URL from settings
            ws_url = settings.websocket_api.replace("http://", "ws://").replace("https://", "wss://")
            ws_url = f"{ws_url}/v1/ws/connect?token={token}"
            
            console.print(f"🔌 Connecting to WebSocket...")
            console.print(f"URL: {ws_url}")
            console.print(f"Duration: {duration}s")
            console.print("Press Ctrl+C to disconnect")
            
            start_time = time.time()
            
            async with websockets.connect(ws_url) as websocket:
                console.print("✅ Connected to WebSocket")
                
                while time.time() - start_time < duration:
                    try:
                        # Wait for message with timeout
                        message = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                        
                        if debug:
                            console.print(f"📨 Raw: {message}")
                        
                        try:
                            data = json.loads(message)
                            msg_type = data.get("type", "unknown")
                            timestamp = data.get("timestamp", "")
                            
                            if msg_type == "ping":
                                console.print("💓 Ping received")
                            elif msg_type == "broadcast":
                                channel = data.get("channel", "")
                                content = data.get("content", {})
                                console.print(f"📢 Broadcast [{channel}]: {content}")
                            elif msg_type == "notification":
                                level = data.get("level", "info")
                                message_text = data.get("message", "")
                                icon = "🔴" if level == "error" else "🟡" if level == "warning" else "ℹ️"
                                console.print(f"{icon} {level.upper()}: {message_text}")
                            else:
                                console.print(f"📨 {msg_type}: {data}")
                                
                        except json.JSONDecodeError:
                            console.print(f"📨 Text: {message}")
                            
                    except asyncio.TimeoutError:
                        # No message received, continue
                        continue
                    except websockets.exceptions.ConnectionClosed:
                        console.print("❌ WebSocket connection closed")
                        break
                        
        except ImportError:
            console.print("❌ websockets library not available")
            console.print("Install with: pip install websockets")
        except KeyboardInterrupt:
            console.print("\n⏹️  Disconnected by user")
        except Exception as e:
            console.print(f"❌ Connection error: {e}")

    _run(_action)

@app.command()
def broadcast(
    channel: str = typer.Argument(..., help="Channel name"),
    message: str = typer.Argument(..., help="Message to broadcast"),
    event_type: Optional[str] = typer.Option(None, "--type", "-t", help="Event type"),
    data: Optional[str] = typer.Option(None, "--data", "-d", help="Additional data (JSON)"),
) -> None:
    """Broadcast message to channel."""
    settings = get_settings()

    async def _action():
        payload = {
            "channel": channel,
            "message": message
        }
        if event_type:
            payload["event_type"] = event_type
        if data:
            import json
            try:
                payload["data"] = json.loads(data)
            except json.JSONDecodeError:
                console.print("❌ Invalid JSON data")
                return
                
        async with client() as c:
            resp = await c.post(f"{settings.websocket_api}/v1/broadcast", json=payload)
            resp.raise_for_status()
            result = resp.json()
            
            console.print(f"📢 Message broadcasted")
            console.print(f"Channel: {channel}")
            console.print(f"Recipients: {result.get('recipient_count', 0)}")
            console.print(f"Message ID: {result.get('message_id', '')}")

    _run(_action)

@app.command()
def bulk_broadcast(
    file: typer.FileText = typer.Argument(..., help="JSON file with messages"),
    channel: Optional[str] = typer.Option(None, "--channel", "-c", help="Default channel"),
) -> None:
    """Broadcast multiple messages from file."""
    settings = get_settings()

    async def _action():
        import json
        
        try:
            messages = json.load(file)
        except json.JSONDecodeError:
            console.print("❌ Invalid JSON file")
            return
        
        # Ensure messages is a list
        if not isinstance(messages, list):
            messages = [messages]
        
        # Set default channel if provided
        if channel:
            for msg in messages:
                if "channel" not in msg:
                    msg["channel"] = channel
        
        async with client() as c:
            resp = await c.post(
                f"{settings.websocket_api}/v1/broadcast/bulk",
                json={"messages": messages}
            )
            resp.raise_for_status()
            result = resp.json()
            
            console.print(f"📢 Bulk broadcast completed")
            console.print(f"Sent: {result.get('sent_count', 0)}")
            console.print(f"Failed: {result.get('failed_count', 0)}")
            console.print(f"Total Recipients: {result.get('total_recipients', 0)}")
            
            if result.get("errors"):
                console.print("❌ Errors:")
                for error in result.get("errors", []):
                    console.print(f"  {error}")

    _run(_action)

@app.command()
def notify(
    event_type: str = typer.Argument(..., help="Notification type"),
    message: str = typer.Argument(..., help="Notification message"),
    level: str = typer.Option("info", "--level", "-l", help="Level: info|warning|error"),
    recipients: List[str] = typer.Option([], "--recipient", "-r", help="Specific recipients"),
    data: Optional[str] = typer.Option(None, "--data", "-d", help="Additional data (JSON)"),
) -> None:
    """Send system notification."""
    settings = get_settings()

    async def _action():
        payload = {
            "event_type": event_type,
            "message": message,
            "level": level
        }
        if recipients:
            payload["recipients"] = recipients
        if data:
            import json
            try:
                payload["data"] = json.loads(data)
            except json.JSONDecodeError:
                console.print("❌ Invalid JSON data")
                return
        
        # Map to appropriate endpoint based on event type
        if event_type == "plugin_status":
            endpoint = "/v1/broadcast/plugin-status"
        elif event_type == "entity_discovered":
            endpoint = "/v1/broadcast/entity-discovered"
        elif event_type == "system_alert":
            endpoint = "/v1/broadcast/system-alert"
        else:
            endpoint = "/v1/broadcast"
            
        async with client() as c:
            resp = await c.post(f"{settings.websocket_api}{endpoint}", json=payload)
            resp.raise_for_status()
            result = resp.json()
            
            level_icon = "🔴" if level == "error" else "🟡" if level == "warning" else "ℹ️"
            console.print(f"{level_icon} Notification sent: {event_type}")
            console.print(f"Message: {message}")
            console.print(f"Recipients: {result.get('recipient_count', 0)}")

    _run(_action)

@app.command()
def channels(
    action: Optional[str] = typer.Argument(None, help="Action: list|subscribe|unsubscribe"),
    channel: Optional[str] = typer.Option(None, "--channel", "-c", help="Channel name"),
    client_id: Optional[str] = typer.Option(None, "--client-id", help="Client ID"),
) -> None:
    """Manage channel subscriptions."""
    settings = get_settings()

    async def _action():
        if not action or action == "list":
            # List available channels
            async with client() as c:
                resp = await c.get(f"{settings.websocket_api}/v1/channels")
                resp.raise_for_status()
                data = resp.json()
                
                table = Table(title="WebSocket Channels")
                table.add_column("Channel")
                table.add_column("Subscribers")
                table.add_column("Description")
                table.add_column("Status")
                
                for channel_info in data.get("channels", []):
                    table.add_row(
                        channel_info.get("name", ""),
                        str(channel_info.get("subscriber_count", 0)),
                        channel_info.get("description", ""),
                        channel_info.get("status", ""),
                    )
                
                console.print(table)
                
        elif action == "subscribe":
            if not channel:
                console.print("❌ Channel name required for subscribe action")
                return
                
            payload = {"channel": channel}
            if client_id:
                payload["client_id"] = client_id
                
            async with client() as c:
                resp = await c.post(f"{settings.websocket_api}/v1/channels/subscribe", json=payload)
                resp.raise_for_status()
                result = resp.json()
                
                console.print(f"✅ Subscribed to channel: {channel}")
                console.print(f"Subscription ID: {result.get('subscription_id', '')}")
                
        elif action == "unsubscribe":
            if not channel:
                console.print("❌ Channel name required for unsubscribe action")
                return
                
            payload = {"channel": channel}
            if client_id:
                payload["client_id"] = client_id
                
            async with client() as c:
                resp = await c.delete(f"{settings.websocket_api}/v1/channels/subscribe", json=payload)
                resp.raise_for_status()
                console.print(f"❌ Unsubscribed from channel: {channel}")

    _run(_action)

@app.command()
def clients(
    status: Optional[str] = typer.Option(None, "--status", "-s", help="Filter by status"),
    channel: Optional[str] = typer.Option(None, "--channel", "-c", help="Filter by channel"),
) -> None:
    """List connected WebSocket clients."""
    settings = get_settings()

    async def _action():
        params = {}
        if status:
            params["status"] = status
        if channel:
            params["channel"] = channel
            
        async with client() as c:
            resp = await c.get(f"{settings.websocket_api}/v1/clients", params=params)
            resp.raise_for_status()
            data = resp.json()
            
            table = Table(title=f"WebSocket Clients ({data.get('total', 0)})")
            table.add_column("Client ID")
            table.add_column("Status")
            table.add_column("Connected")
            table.add_column("Channels")
            table.add_column("Last Activity")
            
            for client_info in data.get("clients", []):
                client_id = client_info.get("id", "")[:8] + "..."
                channels = ", ".join(client_info.get("channels", [])[:3])
                status_icon = "🟢" if client_info.get("status") == "connected" else "🔴"
                
                table.add_row(
                    client_id,
                    f"{status_icon} {client_info.get('status', '')}",
                    client_info.get("connected_at", ""),
                    channels,
                    client_info.get("last_activity", ""),
                )
            
            console.print(table)

    _run(_action)

@app.command()
def investigations(
    action: str = typer.Argument(..., help="Action: list|create|join|leave"),
    room_id: Optional[str] = typer.Option(None, "--room", "-r", help="Investigation room ID"),
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Room name (for create)"),
    description: Optional[str] = typer.Option(None, "--desc", "-d", help="Room description"),
) -> None:
    """Manage investigation rooms."""
    settings = get_settings()

    async def _action():
        if action == "list":
            # List investigation rooms
            async with client() as c:
                resp = await c.get(f"{settings.websocket_api}/v1/investigations")
                resp.raise_for_status()
                data = resp.json()
                
                table = Table(title="Investigation Rooms")
                table.add_column("Room ID")
                table.add_column("Name")
                table.add_column("Participants")
                table.add_column("Status")
                table.add_column("Created")
                
                for room in data.get("rooms", []):
                    room_id_short = room.get("id", "")[:8] + "..."
                    table.add_row(
                        room_id_short,
                        room.get("name", ""),
                        str(room.get("participant_count", 0)),
                        room.get("status", ""),
                        room.get("created_at", ""),
                    )
                
                console.print(table)
                
        elif action == "create":
            if not name:
                console.print("❌ Room name required for create action")
                return
                
            payload = {"name": name}
            if description:
                payload["description"] = description
                
            async with client() as c:
                resp = await c.post(f"{settings.websocket_api}/v1/investigations", json=payload)
                resp.raise_for_status()
                result = resp.json()
                
                console.print(f"✅ Investigation room created")
                console.print(f"Room ID: {result.get('room_id', '')}")
                console.print(f"Name: {name}")
                
        elif action in ["join", "leave"]:
            if not room_id:
                console.print(f"❌ Room ID required for {action} action")
                return
                
            payload = {"room_id": room_id}
            endpoint = f"/v1/investigations/manage"
            payload["action"] = action
            
            async with client() as c:
                resp = await c.post(f"{settings.websocket_api}{endpoint}", json=payload)
                resp.raise_for_status()
                
                action_past = "joined" if action == "join" else "left"
                console.print(f"✅ {action_past.title()} investigation room: {room_id}")

    _run(_action)

@app.command()
def collaboration(
    event_type: str = typer.Argument(..., help="Event type: cursor|typing|presence"),
    room_id: str = typer.Option(..., "--room", "-r", help="Room ID"),
    data: str = typer.Option(..., "--data", "-d", help="Event data (JSON)"),
) -> None:
    """Send collaboration events."""
    settings = get_settings()

    async def _action():
        import json
        
        try:
            event_data = json.loads(data)
        except json.JSONDecodeError:
            console.print("❌ Invalid JSON data")
            return
        
        payload = {
            "event_type": event_type,
            "room_id": room_id,
            "data": event_data
        }
        
        async with client() as c:
            resp = await c.post(f"{settings.websocket_api}/v1/collaboration/event", json=payload)
            resp.raise_for_status()
            result = resp.json()
            
            console.print(f"✅ Collaboration event sent: {event_type}")
            console.print(f"Room: {room_id}")
            console.print(f"Recipients: {result.get('recipient_count', 0)}")

    _run(_action)

@app.command()
def stats(
    detailed: bool = typer.Option(False, "--detailed", "-d", help="Detailed statistics"),
    period: str = typer.Option("1h", "--period", "-p", help="Time period"),
) -> None:
    """Show WebSocket statistics."""
    settings = get_settings()

    async def _action():
        params = {"period": period}
        if detailed:
            params["detailed"] = True
            
        async with client() as c:
            if detailed:
                resp = await c.get(f"{settings.websocket_api}/v1/stats/detailed", params=params)
            else:
                resp = await c.get(f"{settings.websocket_api}/v1/stats", params=params)
            resp.raise_for_status()
            data = resp.json()
            
            console.print(f"📊 WebSocket Statistics ({period})")
            
            # Connection stats
            console.print(f"Active Connections: {data.get('active_connections', 0)}")
            console.print(f"Total Messages: {data.get('total_messages', 0)}")
            console.print(f"Channels: {data.get('channel_count', 0)}")
            console.print(f"Broadcasts: {data.get('broadcast_count', 0)}")
            
            if detailed:
                # Channel breakdown
                if data.get("channel_stats"):
                    table = Table(title="Channel Statistics")
                    table.add_column("Channel")
                    table.add_column("Subscribers")
                    table.add_column("Messages")
                    table.add_column("Avg Size")
                    
                    for channel_stat in data.get("channel_stats", []):
                        table.add_row(
                            channel_stat.get("channel", ""),
                            str(channel_stat.get("subscriber_count", 0)),
                            str(channel_stat.get("message_count", 0)),
                            f"{channel_stat.get('avg_message_size', 0)} bytes",
                        )
                    
                    console.print(table)
                
                # Performance metrics
                if data.get("performance"):
                    perf = data.get("performance", {})
                    console.print(f"\n⚡ Performance:")
                    console.print(f"  Avg Message Latency: {perf.get('avg_latency_ms', 0)}ms")
                    console.print(f"  Messages/sec: {perf.get('messages_per_second', 0)}")
                    console.print(f"  Memory Usage: {perf.get('memory_usage_mb', 0)}MB")

    _run(_action)

@app.command()
def health() -> None:
    """Check WebSocket service health."""
    settings = get_settings()

    async def _action():
        async with client() as c:
            resp = await c.get(f"{settings.websocket_api}/v1/health")
            resp.raise_for_status()
            data = resp.json()
            
            console.print("🏥 WebSocket Service Health")
            
            # Overall health
            overall_health = data.get("status", "Unknown")
            health_icon = "✅" if overall_health == "healthy" else "❌"
            console.print(f"Status: {health_icon} {overall_health}")
            
            # Component health
            if data.get("components"):
                table = Table(title="Component Health")
                table.add_column("Component")
                table.add_column("Status")
                table.add_column("Details")
                
                for component in data.get("components", []):
                    status_icon = "✅" if component.get("healthy", False) else "❌"
                    
                    table.add_row(
                        component.get("name", ""),
                        f"{status_icon} {component.get('status', '')}",
                        component.get("details", ""),
                    )
                
                console.print(table)
            
            # Connection info
            if data.get("connections"):
                conn_info = data.get("connections", {})
                console.print(f"\n🔌 Connections:")
                console.print(f"  Active: {conn_info.get('active', 0)}")
                console.print(f"  Peak: {conn_info.get('peak', 0)}")
                console.print(f"  Total: {conn_info.get('total', 0)}")

    _run(_action)
