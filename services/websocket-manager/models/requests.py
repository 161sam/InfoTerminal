"""
Pydantic models for WebSocket Manager Service v1.
"""

from typing import List, Dict, Any, Optional, Set
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
import uuid


class MessageType(str, Enum):
    """WebSocket message types for different events."""
    # Plugin execution updates
    PLUGIN_STARTED = "plugin_started"
    PLUGIN_PROGRESS = "plugin_progress"
    PLUGIN_COMPLETED = "plugin_completed"
    PLUGIN_ERROR = "plugin_error"
    
    # Entity and graph updates
    ENTITY_DISCOVERED = "entity_discovered"
    GRAPH_UPDATED = "graph_updated"
    RELATIONSHIP_ADDED = "relationship_added"
    
    # Investigation updates
    INVESTIGATION_CREATED = "investigation_created"
    INVESTIGATION_UPDATED = "investigation_updated"
    ANALYSIS_COMPLETED = "analysis_completed"
    
    # System notifications
    SYSTEM_ALERT = "system_alert"
    USER_NOTIFICATION = "user_notification"
    
    # Collaboration features
    USER_JOINED = "user_joined"
    USER_LEFT = "user_left"
    CURSOR_MOVED = "cursor_moved"
    SELECTION_CHANGED = "selection_changed"
    
    # Performance and health
    PERFORMANCE_ALERT = "performance_alert"
    HEALTH_STATUS = "health_status"


class Channel(str, Enum):
    """WebSocket channels for message routing."""
    GLOBAL = "global"
    USER = "user"
    INVESTIGATION = "investigation"
    PLUGIN_EXECUTION = "plugin_execution"
    GRAPH_ANALYSIS = "graph_analysis"
    SYSTEM_HEALTH = "system_health"


class WebSocketMessage(BaseModel):
    """WebSocket message structure."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique message ID")
    type: MessageType = Field(..., description="Message type")
    channel: Channel = Field(..., description="Target channel")
    timestamp: datetime = Field(default_factory=datetime.now, description="Message timestamp")
    data: Dict[str, Any] = Field(..., description="Message payload")
    sender_id: Optional[str] = Field(None, description="Sender user ID")
    target_user_id: Optional[str] = Field(None, description="Target user ID for direct messages")
    investigation_id: Optional[str] = Field(None, description="Investigation room ID")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class ConnectedClient(BaseModel):
    """Connected WebSocket client information."""
    client_id: str = Field(..., description="Unique client identifier")
    user_id: Optional[str] = Field(None, description="User ID if authenticated")
    connected_at: datetime = Field(..., description="Connection timestamp")
    last_ping: datetime = Field(..., description="Last ping timestamp")
    subscribed_channels: List[Channel] = Field(default_factory=list, description="Subscribed channels")
    investigation_ids: List[str] = Field(default_factory=list, description="Joined investigations")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Client metadata")


class BroadcastRequest(BaseModel):
    """Request to broadcast a message."""
    type: MessageType = Field(..., description="Message type")
    channel: Channel = Field(..., description="Target channel")
    data: Dict[str, Any] = Field(..., description="Message data")
    target_user_id: Optional[str] = Field(None, description="Target specific user")
    investigation_id: Optional[str] = Field(None, description="Target investigation room")
    sender_id: Optional[str] = Field(None, description="Sender user ID")
    
    class Config:
        schema_extra = {
            "example": {
                "type": "entity_discovered",
                "channel": "graph_analysis",
                "data": {
                    "entity_id": "person_123",
                    "entity_type": "person",
                    "entity_name": "John Doe"
                },
                "investigation_id": "inv_456"
            }
        }


class BroadcastResponse(BaseModel):
    """Response for broadcast operations."""
    success: bool = Field(..., description="Operation success status")
    message_id: str = Field(..., description="Broadcast message ID")
    message: str = Field(default="Message broadcast successfully")


class PluginStatusRequest(BaseModel):
    """Request to broadcast plugin execution status."""
    plugin_id: str = Field(..., description="Plugin identifier")
    status: str = Field(..., description="Plugin status", regex="^(started|progress|completed|error)$")
    progress: Optional[int] = Field(None, description="Progress percentage (0-100)", ge=0, le=100)
    message: Optional[str] = Field(None, description="Status message")
    error: Optional[str] = Field(None, description="Error message if status is error")
    user_id: Optional[str] = Field(None, description="Target user ID")
    
    class Config:
        schema_extra = {
            "example": {
                "plugin_id": "osint_scanner_v1",
                "status": "progress",
                "progress": 75,
                "message": "Scanning social media profiles...",
                "user_id": "user_123"
            }
        }


class EntityDiscoveredRequest(BaseModel):
    """Request to broadcast entity discovery."""
    entity_id: str = Field(..., description="Entity identifier")
    entity_type: str = Field(..., description="Entity type (person, organization, etc.)")
    entity_name: str = Field(..., description="Entity name/label")
    investigation_id: Optional[str] = Field(None, description="Investigation context")
    discovered_by: Optional[str] = Field(None, description="User who discovered the entity")
    properties: Optional[Dict[str, Any]] = Field(None, description="Additional entity properties")
    
    class Config:
        schema_extra = {
            "example": {
                "entity_id": "person_12345",
                "entity_type": "person",
                "entity_name": "Jane Smith",
                "investigation_id": "inv_67890",
                "discovered_by": "analyst_001",
                "properties": {
                    "confidence": 0.95,
                    "source": "linkedin_scraper"
                }
            }
        }


class SystemAlertRequest(BaseModel):
    """Request to broadcast system alert."""
    level: str = Field(..., description="Alert level", regex="^(info|warning|error|critical)$")
    title: str = Field(..., description="Alert title")
    message: str = Field(..., description="Alert message")
    target_user_id: Optional[str] = Field(None, description="Target specific user")
    category: Optional[str] = Field(None, description="Alert category")
    action_url: Optional[str] = Field(None, description="URL for alert action")
    
    class Config:
        schema_extra = {
            "example": {
                "level": "warning",
                "title": "High CPU Usage",
                "message": "System CPU usage has exceeded 80% for the last 5 minutes",
                "category": "performance"
            }
        }


class ChannelSubscriptionRequest(BaseModel):
    """Request to subscribe/unsubscribe from channels."""
    client_id: str = Field(..., description="Client identifier")
    channels: List[Channel] = Field(..., description="Channels to subscribe to")
    action: str = Field(..., description="Action to perform", regex="^(subscribe|unsubscribe)$")


class InvestigationRoomRequest(BaseModel):
    """Request to join/leave investigation room."""
    client_id: str = Field(..., description="Client identifier")
    investigation_id: str = Field(..., description="Investigation identifier")
    action: str = Field(..., description="Action to perform", regex="^(join|leave)$")


class WebSocketStats(BaseModel):
    """WebSocket manager statistics."""
    total_connections: int = Field(..., description="Total connections since startup", ge=0)
    active_connections: int = Field(..., description="Currently active connections", ge=0)
    messages_sent: int = Field(..., description="Total messages sent", ge=0)
    messages_received: int = Field(..., description="Total messages received", ge=0)
    channels_active: int = Field(..., description="Active channels with subscribers", ge=0)
    investigation_rooms: int = Field(..., description="Active investigation rooms", ge=0)
    offline_message_queues: int = Field(..., description="Users with queued offline messages", ge=0)


class ConnectionTokenRequest(BaseModel):
    """Request to generate WebSocket connection token."""
    user_id: str = Field(..., description="User identifier")
    expires_in: int = Field(3600, description="Token expiry in seconds", ge=60, le=86400)
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional token metadata")


class ConnectionTokenResponse(BaseModel):
    """Response with WebSocket connection token."""
    token: str = Field(..., description="JWT token for WebSocket authentication")
    expires_at: datetime = Field(..., description="Token expiration timestamp")
    websocket_url: str = Field(..., description="WebSocket connection URL")


class ClientInfo(BaseModel):
    """Information about a connected client."""
    client_id: str = Field(..., description="Client identifier")
    user_id: Optional[str] = Field(None, description="User ID if authenticated")
    connected_at: datetime = Field(..., description="Connection timestamp")
    last_activity: datetime = Field(..., description="Last activity timestamp")
    subscribed_channels: List[Channel] = Field(..., description="Subscribed channels")
    investigation_rooms: List[str] = Field(..., description="Joined investigations")
    connection_info: Dict[str, Any] = Field(..., description="Connection metadata")


class ActiveClientsResponse(BaseModel):
    """Response listing active WebSocket clients."""
    clients: List[ClientInfo] = Field(..., description="List of active clients")
    total_count: int = Field(..., description="Total number of clients", ge=0)


class InvestigationRoomInfo(BaseModel):
    """Information about an investigation room."""
    investigation_id: str = Field(..., description="Investigation identifier")
    member_count: int = Field(..., description="Number of connected members", ge=0)
    members: List[str] = Field(..., description="List of member user IDs")
    created_at: datetime = Field(..., description="Room creation timestamp")
    last_activity: datetime = Field(..., description="Last activity in room")


class InvestigationRoomsResponse(BaseModel):
    """Response listing active investigation rooms."""
    rooms: List[InvestigationRoomInfo] = Field(..., description="List of active rooms")
    total_count: int = Field(..., description="Total number of rooms", ge=0)


class MessageHistory(BaseModel):
    """Historical message information."""
    message_id: str = Field(..., description="Message identifier")
    type: MessageType = Field(..., description="Message type")
    channel: Channel = Field(..., description="Channel")
    timestamp: datetime = Field(..., description="Message timestamp")
    sender_id: Optional[str] = Field(None, description="Sender user ID")
    data_summary: Dict[str, Any] = Field(..., description="Summary of message data")


class MessageHistoryResponse(BaseModel):
    """Response with message history."""
    messages: List[MessageHistory] = Field(..., description="Recent messages")
    total_count: int = Field(..., description="Total messages in history", ge=0)
    page: int = Field(..., description="Current page number", ge=1)
    per_page: int = Field(..., description="Messages per page", ge=1)


class HealthStatus(BaseModel):
    """WebSocket manager health status."""
    status: str = Field(..., description="Overall health status")
    service: str = Field(..., description="Service name")
    active_connections: int = Field(..., description="Number of active connections", ge=0)
    redis_connected: bool = Field(..., description="Redis connection status")
    uptime_seconds: float = Field(..., description="Service uptime in seconds", ge=0)
    memory_usage_mb: float = Field(..., description="Memory usage in MB", ge=0)
    message_queue_size: int = Field(..., description="Pending message queue size", ge=0)


class CollaborationEvent(BaseModel):
    """Collaboration event for real-time features."""
    event_type: str = Field(..., description="Event type", regex="^(cursor_moved|selection_changed|user_typing|user_idle)$")
    user_id: str = Field(..., description="User who triggered event")
    investigation_id: str = Field(..., description="Investigation context")
    data: Dict[str, Any] = Field(..., description="Event-specific data")
    timestamp: datetime = Field(default_factory=datetime.now, description="Event timestamp")


class BulkBroadcastRequest(BaseModel):
    """Request to broadcast multiple messages."""
    messages: List[BroadcastRequest] = Field(..., description="Messages to broadcast", min_items=1, max_items=100)


class BulkBroadcastResponse(BaseModel):
    """Response for bulk broadcast operations."""
    total_messages: int = Field(..., description="Total messages processed", ge=0)
    successful: int = Field(..., description="Successfully broadcast messages", ge=0)
    failed: int = Field(..., description="Failed messages", ge=0)
    message_ids: List[str] = Field(..., description="List of broadcast message IDs")
    errors: List[Dict[str, str]] = Field(default_factory=list, description="Broadcast errors")


class ChannelStatsResponse(BaseModel):
    """Statistics for individual channels."""
    channel: Channel = Field(..., description="Channel name")
    subscriber_count: int = Field(..., description="Number of subscribers", ge=0)
    messages_sent: int = Field(..., description="Messages sent to channel", ge=0)
    last_activity: Optional[datetime] = Field(None, description="Last message timestamp")


class DetailedStatsResponse(BaseModel):
    """Detailed WebSocket manager statistics."""
    overall: WebSocketStats = Field(..., description="Overall statistics")
    by_channel: List[ChannelStatsResponse] = Field(..., description="Per-channel statistics")
    top_users: List[Dict[str, Any]] = Field(..., description="Most active users")
    performance_metrics: Dict[str, Any] = Field(..., description="Performance metrics")


class WebSocketConfig(BaseModel):
    """WebSocket manager configuration."""
    max_connections: int = Field(1000, description="Maximum concurrent connections", ge=1)
    ping_interval_seconds: int = Field(30, description="Ping interval in seconds", ge=10)
    connection_timeout_seconds: int = Field(60, description="Connection timeout", ge=30)
    max_offline_messages: int = Field(100, description="Max queued offline messages per user", ge=10)
    enable_redis_pubsub: bool = Field(True, description="Enable Redis pub/sub for scaling")
    jwt_secret: str = Field(..., description="JWT secret for token validation")
    allowed_origins: List[str] = Field(default_factory=list, description="CORS allowed origins")


class UpdateConfigRequest(BaseModel):
    """Request to update WebSocket configuration."""
    config: WebSocketConfig = Field(..., description="New configuration")


class ConfigResponse(BaseModel):
    """WebSocket configuration response."""
    config: WebSocketConfig = Field(..., description="Current configuration")
    applied_at: datetime = Field(..., description="Configuration application timestamp")
