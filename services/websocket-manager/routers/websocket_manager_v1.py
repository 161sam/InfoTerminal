"""
WebSocket Manager v1 router - Real-time Communication API.

Provides comprehensive WebSocket management with real-time messaging,
collaboration features, and distributed broadcasting capabilities.
"""

import asyncio
import json
import logging
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect, Query, Path, Depends
from fastapi.responses import JSONResponse

from main import ws_manager, WebSocketMessage as WSMessage, MessageType as WSMessageType, Channel as WSChannel
from _shared.api_standards.error_schemas import StandardError, ErrorCodes, create_error_response
from _shared.api_standards.pagination import PaginatedResponse, PaginationParams
from models.requests import (
    BroadcastRequest, BroadcastResponse, PluginStatusRequest, EntityDiscoveredRequest,
    SystemAlertRequest, ChannelSubscriptionRequest, InvestigationRoomRequest,
    WebSocketStats, DetailedStatsResponse, ChannelStatsResponse, HealthStatus,
    ConnectionTokenRequest, ConnectionTokenResponse, ClientInfo, ActiveClientsResponse,
    InvestigationRoomInfo, InvestigationRoomsResponse, MessageHistory, MessageHistoryResponse,
    CollaborationEvent, BulkBroadcastRequest, BulkBroadcastResponse, WebSocketConfig,
    UpdateConfigRequest, ConfigResponse, MessageType, Channel
)

logger = logging.getLogger(__name__)
router = APIRouter(tags=["WebSocket Management"])


# Dependency for error handling
def handle_websocket_errors(func):
    """Decorator to handle WebSocket operation errors with standard error format"""
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ValueError as e:
            logger.warning(f"WebSocket validation error: {e}")
            error_response = create_error_response(
                ErrorCodes.VALIDATION_ERROR,
                str(e),
                {"service": "websocket-manager"}
            )
            raise HTTPException(status_code=400, detail=error_response.dict())
        except Exception as e:
            logger.error(f"WebSocket operation failed: {e}")
            error_response = create_error_response(
                ErrorCodes.INTERNAL_ERROR,
                "Internal WebSocket operation error",
                {"service": "websocket-manager", "original_error": str(e)}
            )
            raise HTTPException(status_code=500, detail=error_response.dict())
    return wrapper


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    client_id: str = Path(..., description="Unique client identifier"),
    user_id: Optional[str] = Query(None, description="User identifier for authentication"),
    token: Optional[str] = Query(None, description="JWT authentication token")
):
    """
    Main WebSocket endpoint for real-time communication.
    
    Supports:
    - Channel-based message broadcasting
    - Investigation room collaboration
    - Plugin execution status updates
    - Real-time entity discovery notifications
    - System alerts and user notifications
    """
    connected = await ws_manager.connect(websocket, client_id, user_id, token)
    
    if not connected:
        return
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Handle client message
            await _handle_client_message(client_id, message_data)
            
    except WebSocketDisconnect:
        await ws_manager.disconnect(client_id)
    except Exception as e:
        logger.error(f"WebSocket error for client {client_id}: {e}")
        await ws_manager.disconnect(client_id)


async def _handle_client_message(client_id: str, message_data: Dict[str, Any]):
    """Handle incoming message from WebSocket client"""
    try:
        message_type = message_data.get("type")
        
        if message_type == "subscribe":
            channel = WSChannel(message_data.get("channel"))
            await ws_manager.subscribe_to_channel(client_id, channel)
            
        elif message_type == "unsubscribe":
            channel = WSChannel(message_data.get("channel"))
            await ws_manager.unsubscribe_from_channel(client_id, channel)
            
        elif message_type == "join_investigation":
            investigation_id = message_data.get("investigation_id")
            await ws_manager.join_investigation(client_id, investigation_id)
            
        elif message_type == "leave_investigation":
            investigation_id = message_data.get("investigation_id")
            await ws_manager.leave_investigation(client_id, investigation_id)
            
        elif message_type == "cursor_moved":
            # Handle collaborative cursor movement
            if client_id in ws_manager.connections:
                client = ws_manager.connections[client_id]
                if client.investigation_ids:
                    for investigation_id in client.investigation_ids:
                        await ws_manager.broadcast_to_investigation(
                            investigation_id,
                            WSMessage(
                                id=str(uuid.uuid4()),
                                type=WSMessageType.CURSOR_MOVED,
                                channel=WSChannel.INVESTIGATION,
                                timestamp=datetime.now(),
                                data={
                                    "user_id": client.user_id,
                                    "x": message_data.get("x"),
                                    "y": message_data.get("y")
                                },
                                sender_id=client.user_id,
                                investigation_id=investigation_id
                            ),
                            exclude_client=client_id
                        )
        
        elif message_type == "pong":
            # Handle ping response
            if client_id in ws_manager.connections:
                ws_manager.connections[client_id].last_ping = datetime.now()
        
        ws_manager.stats["messages_received"] += 1
        
    except Exception as e:
        logger.error(f"Failed to handle client message: {e}")


@router.post("/broadcast", response_model=BroadcastResponse)
@handle_websocket_errors
async def broadcast_message(request: BroadcastRequest) -> BroadcastResponse:
    """
    Broadcast a message to WebSocket clients via REST API.
    
    Supports broadcasting to:
    - Specific channels (global, user, investigation, etc.)
    - Individual users by user ID
    - Investigation rooms
    - All connected clients
    """
    message = WSMessage(
        id=str(uuid.uuid4()),
        type=WSMessageType(request.type),
        channel=WSChannel(request.channel),
        timestamp=datetime.now(),
        data=request.data,
        sender_id=request.sender_id,
        target_user_id=request.target_user_id,
        investigation_id=request.investigation_id
    )
    
    await ws_manager._distribute_message(message)
    
    return BroadcastResponse(
        success=True,
        message_id=message.id,
        message="Message broadcast successfully"
    )


@router.post("/broadcast/bulk", response_model=BulkBroadcastResponse)
@handle_websocket_errors
async def bulk_broadcast_messages(request: BulkBroadcastRequest) -> BulkBroadcastResponse:
    """
    Broadcast multiple messages in a single operation.
    
    Processes up to 100 messages concurrently with individual error handling.
    """
    total_messages = len(request.messages)
    successful = 0
    message_ids = []
    errors = []
    
    async def broadcast_single(broadcast_req: BroadcastRequest):
        try:
            message = WSMessage(
                id=str(uuid.uuid4()),
                type=WSMessageType(broadcast_req.type),
                channel=WSChannel(broadcast_req.channel),
                timestamp=datetime.now(),
                data=broadcast_req.data,
                sender_id=broadcast_req.sender_id,
                target_user_id=broadcast_req.target_user_id,
                investigation_id=broadcast_req.investigation_id
            )
            
            await ws_manager._distribute_message(message)
            return message.id, None
        except Exception as e:
            return None, str(e)
    
    # Execute bulk broadcasts
    tasks = [broadcast_single(msg) for msg in request.messages]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Process results
    for i, (msg_id, error) in enumerate(results):
        if msg_id:
            message_ids.append(msg_id)
            successful += 1
        else:
            errors.append({
                "index": i,
                "error": error or "Unknown error"
            })
    
    return BulkBroadcastResponse(
        total_messages=total_messages,
        successful=successful,
        failed=len(errors),
        message_ids=message_ids,
        errors=errors
    )


@router.post("/broadcast/plugin-status", response_model=BroadcastResponse)
@handle_websocket_errors
async def broadcast_plugin_status(request: PluginStatusRequest) -> BroadcastResponse:
    """
    Broadcast plugin execution status updates.
    
    Automatically determines message type based on status:
    - started → PLUGIN_STARTED
    - progress → PLUGIN_PROGRESS  
    - completed → PLUGIN_COMPLETED
    - error → PLUGIN_ERROR
    """
    message_type = WSMessageType.PLUGIN_PROGRESS
    
    if request.status == "started":
        message_type = WSMessageType.PLUGIN_STARTED
    elif request.status == "completed":
        message_type = WSMessageType.PLUGIN_COMPLETED
    elif request.status == "error":
        message_type = WSMessageType.PLUGIN_ERROR
    
    message = WSMessage(
        id=str(uuid.uuid4()),
        type=message_type,
        channel=WSChannel.PLUGIN_EXECUTION,
        timestamp=datetime.now(),
        data={
            "plugin_id": request.plugin_id,
            "status": request.status,
            "progress": request.progress,
            "message": request.message,
            "error": request.error
        },
        target_user_id=request.user_id
    )
    
    await ws_manager._distribute_message(message)
    
    return BroadcastResponse(
        success=True,
        message_id=message.id,
        message=f"Plugin status '{request.status}' broadcast successfully"
    )


@router.post("/broadcast/entity-discovered", response_model=BroadcastResponse)
@handle_websocket_errors
async def broadcast_entity_discovered(request: EntityDiscoveredRequest) -> BroadcastResponse:
    """
    Broadcast new entity discovery notifications.
    
    Notifies investigation team members when new entities are discovered
    during analysis or investigation workflows.
    """
    message = WSMessage(
        id=str(uuid.uuid4()),
        type=WSMessageType.ENTITY_DISCOVERED,
        channel=WSChannel.GRAPH_ANALYSIS,
        timestamp=datetime.now(),
        data={
            "entity_id": request.entity_id,
            "entity_type": request.entity_type,
            "entity_name": request.entity_name,
            "discovered_by": request.discovered_by,
            "properties": request.properties or {}
        },
        investigation_id=request.investigation_id
    )
    
    await ws_manager._distribute_message(message)
    
    return BroadcastResponse(
        success=True,
        message_id=message.id,
        message=f"Entity discovery '{request.entity_name}' broadcast successfully"
    )


@router.post("/broadcast/system-alert", response_model=BroadcastResponse)
@handle_websocket_errors
async def broadcast_system_alert(request: SystemAlertRequest) -> BroadcastResponse:
    """
    Broadcast system alerts and notifications.
    
    Supports different alert levels (info, warning, error, critical)
    and can target specific users or broadcast globally.
    """
    message = WSMessage(
        id=str(uuid.uuid4()),
        type=WSMessageType.SYSTEM_ALERT,
        channel=WSChannel.GLOBAL,
        timestamp=datetime.now(),
        data={
            "level": request.level,
            "title": request.title,
            "message": request.message,
            "category": request.category,
            "action_url": request.action_url
        },
        target_user_id=request.target_user_id
    )
    
    await ws_manager._distribute_message(message)
    
    return BroadcastResponse(
        success=True,
        message_id=message.id,
        message=f"System alert '{request.title}' broadcast successfully"
    )


@router.post("/channels/subscribe", response_model=Dict[str, Any])
@handle_websocket_errors
async def manage_channel_subscription(request: ChannelSubscriptionRequest) -> Dict[str, Any]:
    """
    Subscribe or unsubscribe client from channels.
    
    Allows dynamic channel management for connected WebSocket clients.
    """
    success_count = 0
    errors = []
    
    for channel in request.channels:
        try:
            if request.action == "subscribe":
                success = await ws_manager.subscribe_to_channel(request.client_id, WSChannel(channel))
            else:  # unsubscribe
                success = await ws_manager.unsubscribe_from_channel(request.client_id, WSChannel(channel))
            
            if success:
                success_count += 1
            else:
                errors.append(f"Client {request.client_id} not found")
        except Exception as e:
            errors.append(f"Failed to {request.action} {channel}: {str(e)}")
    
    return {
        "action": request.action,
        "client_id": request.client_id,
        "channels_processed": len(request.channels),
        "successful": success_count,
        "errors": errors
    }


@router.post("/investigations/manage", response_model=Dict[str, Any])
@handle_websocket_errors
async def manage_investigation_room(request: InvestigationRoomRequest) -> Dict[str, Any]:
    """
    Join or leave investigation rooms.
    
    Manages client participation in investigation-specific collaboration rooms.
    """
    try:
        if request.action == "join":
            success = await ws_manager.join_investigation(request.client_id, request.investigation_id)
            action_message = "joined"
        else:  # leave
            success = await ws_manager.leave_investigation(request.client_id, request.investigation_id)
            action_message = "left"
        
        if not success:
            error_response = create_error_response(
                ErrorCodes.RESOURCE_NOT_FOUND,
                f"Client {request.client_id} not found",
                {"client_id": request.client_id, "service": "websocket-manager"}
            )
            raise HTTPException(status_code=404, detail=error_response.dict())
        
        return {
            "action": request.action,
            "client_id": request.client_id,
            "investigation_id": request.investigation_id,
            "message": f"Client {action_message} investigation {request.investigation_id} successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        error_response = create_error_response(
            ErrorCodes.INTERNAL_ERROR,
            f"Failed to {request.action} investigation room",
            {"client_id": request.client_id, "investigation_id": request.investigation_id, "error": str(e)}
        )
        raise HTTPException(status_code=500, detail=error_response.dict())


@router.get("/clients", response_model=ActiveClientsResponse)
async def get_active_clients(
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    channel: Optional[Channel] = Query(None, description="Filter by subscribed channel")
) -> ActiveClientsResponse:
    """
    Get list of active WebSocket clients with filtering options.
    
    Provides information about connected clients, their subscriptions,
    and current activity status.
    """
    clients = []
    
    for client_id, client in ws_manager.connections.items():
        # Apply filters
        if user_id and client.user_id != user_id:
            continue
        
        if channel and WSChannel(channel) not in client.subscribed_channels:
            continue
        
        client_info = ClientInfo(
            client_id=client_id,
            user_id=client.user_id,
            connected_at=client.connected_at,
            last_activity=client.last_ping,
            subscribed_channels=[Channel(ch.value) for ch in client.subscribed_channels],
            investigation_rooms=list(client.investigation_ids),
            connection_info={
                "uptime_seconds": (datetime.now() - client.connected_at).total_seconds(),
                "metadata": client.metadata
            }
        )
        clients.append(client_info)
    
    return ActiveClientsResponse(
        clients=clients,
        total_count=len(clients)
    )


@router.get("/investigations", response_model=InvestigationRoomsResponse)
async def get_investigation_rooms() -> InvestigationRoomsResponse:
    """
    Get list of active investigation rooms.
    
    Shows current investigation rooms with member counts and activity information.
    """
    rooms = []
    
    for investigation_id, members in ws_manager.investigation_rooms.items():
        # Get member user IDs
        member_user_ids = []
        last_activity = None
        
        for client_id in members:
            if client_id in ws_manager.connections:
                client = ws_manager.connections[client_id]
                if client.user_id:
                    member_user_ids.append(client.user_id)
                
                # Track most recent activity
                if not last_activity or client.last_ping > last_activity:
                    last_activity = client.last_ping
        
        room_info = InvestigationRoomInfo(
            investigation_id=investigation_id,
            member_count=len(members),
            members=member_user_ids,
            created_at=datetime.now(),  # Note: Would need tracking for real creation time
            last_activity=last_activity or datetime.now()
        )
        rooms.append(room_info)
    
    return InvestigationRoomsResponse(
        rooms=rooms,
        total_count=len(rooms)
    )


@router.get("/stats", response_model=WebSocketStats)
async def get_websocket_stats() -> WebSocketStats:
    """
    Get basic WebSocket manager statistics.
    
    Provides overview of connection counts, message throughput,
    and active channels/rooms.
    """
    stats = ws_manager.get_stats()
    
    return WebSocketStats(
        total_connections=stats["total_connections"],
        active_connections=stats["active_connections"],
        messages_sent=stats["messages_sent"],
        messages_received=stats["messages_received"],
        channels_active=stats["channels_active"],
        investigation_rooms=stats["investigation_rooms"],
        offline_message_queues=stats["offline_message_queues"]
    )


@router.get("/stats/detailed", response_model=DetailedStatsResponse)
async def get_detailed_stats() -> DetailedStatsResponse:
    """
    Get comprehensive WebSocket manager statistics.
    
    Includes per-channel statistics, top users, and performance metrics.
    """
    # Get basic stats
    basic_stats = await get_websocket_stats()
    
    # Calculate per-channel stats
    channel_stats = []
    for channel, subscribers in ws_manager.channel_subscribers.items():
        channel_stat = ChannelStatsResponse(
            channel=Channel(channel.value),
            subscriber_count=len(subscribers),
            messages_sent=0,  # Would need tracking
            last_activity=datetime.now() if subscribers else None
        )
        channel_stats.append(channel_stat)
    
    # Top users (most active connections)
    top_users = []
    user_activity = {}
    
    for client in ws_manager.connections.values():
        if client.user_id:
            if client.user_id not in user_activity:
                user_activity[client.user_id] = {
                    "user_id": client.user_id,
                    "connections": 0,
                    "total_uptime": 0
                }
            
            user_activity[client.user_id]["connections"] += 1
            user_activity[client.user_id]["total_uptime"] += (datetime.now() - client.connected_at).total_seconds()
    
    # Sort by activity and take top 10
    sorted_users = sorted(user_activity.values(), key=lambda x: x["total_uptime"], reverse=True)[:10]
    top_users = sorted_users
    
    # Performance metrics
    performance_metrics = {
        "average_uptime_seconds": sum(
            (datetime.now() - client.connected_at).total_seconds() 
            for client in ws_manager.connections.values()
        ) / max(len(ws_manager.connections), 1),
        "redis_connected": ws_manager.redis is not None,
        "offline_message_total": sum(len(msgs) for msgs in ws_manager.offline_messages.values()),
        "memory_usage_estimate_mb": len(ws_manager.connections) * 0.1  # Rough estimate
    }
    
    return DetailedStatsResponse(
        overall=basic_stats,
        by_channel=channel_stats,
        top_users=top_users,
        performance_metrics=performance_metrics
    )


@router.get("/health", response_model=HealthStatus)
async def get_websocket_health() -> HealthStatus:
    """
    Get comprehensive WebSocket manager health status.
    
    Includes service status, connection health, Redis connectivity,
    and resource utilization metrics.
    """
    import psutil
    
    # Calculate uptime
    start_time = getattr(ws_manager, '_start_time', datetime.now())
    uptime = (datetime.now() - start_time).total_seconds()
    
    # Check Redis connectivity
    redis_connected = False
    if ws_manager.redis:
        try:
            await ws_manager.redis.ping()
            redis_connected = True
        except Exception:
            pass
    
    # Memory usage
    memory = psutil.virtual_memory()
    memory_usage_mb = (memory.total - memory.available) / (1024 * 1024)
    
    # Message queue size
    message_queue_size = sum(len(msgs) for msgs in ws_manager.offline_messages.values())
    
    # Determine health status
    health_checks = [
        len(ws_manager.connections) < 1000,  # Not overwhelmed with connections
        memory.available > 512 * 1024 * 1024,  # At least 512MB available
        message_queue_size < 1000  # Message queue not backing up
    ]
    
    status = "healthy" if all(health_checks) else "degraded"
    
    return HealthStatus(
        status=status,
        service="websocket-manager",
        active_connections=len(ws_manager.connections),
        redis_connected=redis_connected,
        uptime_seconds=uptime,
        memory_usage_mb=memory_usage_mb,
        message_queue_size=message_queue_size
    )


@router.post("/clients/{client_id}/disconnect")
@handle_websocket_errors
async def disconnect_client(
    client_id: str = Path(..., description="Client ID to disconnect")
) -> Dict[str, Any]:
    """
    Forcefully disconnect a WebSocket client.
    
    Useful for administrative purposes or handling problematic connections.
    """
    if client_id not in ws_manager.connections:
        error_response = create_error_response(
            ErrorCodes.RESOURCE_NOT_FOUND,
            f"Client {client_id} not found",
            {"client_id": client_id, "service": "websocket-manager"}
        )
        raise HTTPException(status_code=404, detail=error_response.dict())
    
    await ws_manager.disconnect(client_id)
    
    return {
        "client_id": client_id,
        "message": "Client disconnected successfully"
    }


@router.post("/collaboration/event", response_model=BroadcastResponse)
@handle_websocket_errors
async def broadcast_collaboration_event(event: CollaborationEvent) -> BroadcastResponse:
    """
    Broadcast collaboration events for real-time features.
    
    Supports cursor movement, selection changes, typing indicators,
    and other collaborative interaction events.
    """
    message = WSMessage(
        id=str(uuid.uuid4()),
        type=WSMessageType.CURSOR_MOVED if event.event_type == "cursor_moved" else WSMessageType.SELECTION_CHANGED,
        channel=WSChannel.INVESTIGATION,
        timestamp=event.timestamp,
        data={
            "event_type": event.event_type,
            "user_id": event.user_id,
            **event.data
        },
        sender_id=event.user_id,
        investigation_id=event.investigation_id
    )
    
    await ws_manager.broadcast_to_investigation(event.investigation_id, message)
    
    return BroadcastResponse(
        success=True,
        message_id=message.id,
        message=f"Collaboration event '{event.event_type}' broadcast successfully"
    )


@router.delete("/offline-messages/{user_id}")
@handle_websocket_errors
async def clear_offline_messages(
    user_id: str = Path(..., description="User ID to clear offline messages for")
) -> Dict[str, Any]:
    """
    Clear queued offline messages for a user.
    
    Removes all pending messages that were queued while the user was offline.
    """
    if user_id in ws_manager.offline_messages:
        message_count = len(ws_manager.offline_messages[user_id])
        del ws_manager.offline_messages[user_id]
        
        return {
            "user_id": user_id,
            "cleared_messages": message_count,
            "message": f"Cleared {message_count} offline messages"
        }
    else:
        return {
            "user_id": user_id,
            "cleared_messages": 0,
            "message": "No offline messages found"
        }
