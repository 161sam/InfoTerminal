"""
WebSocket Manager Service Models

Comprehensive Pydantic models for WebSocket management API requests and responses.
Includes models for real-time communication, collaboration, and system notifications.
"""

from .requests import (
    # Enums
    MessageType,
    Channel,
    
    # Core models
    WebSocketMessage,
    ConnectedClient,
    
    # Request/Response models
    BroadcastRequest,
    BroadcastResponse,
    PluginStatusRequest,
    EntityDiscoveredRequest,
    SystemAlertRequest,
    
    # Channel and room management
    ChannelSubscriptionRequest,
    InvestigationRoomRequest,
    
    # Statistics and monitoring
    WebSocketStats,
    DetailedStatsResponse,
    ChannelStatsResponse,
    HealthStatus,
    
    # Authentication and connection
    ConnectionTokenRequest,
    ConnectionTokenResponse,
    ClientInfo,
    ActiveClientsResponse,
    
    # Investigation rooms
    InvestigationRoomInfo,
    InvestigationRoomsResponse,
    
    # Message history
    MessageHistory,
    MessageHistoryResponse,
    
    # Collaboration
    CollaborationEvent,
    
    # Bulk operations
    BulkBroadcastRequest,
    BulkBroadcastResponse,
    
    # Configuration
    WebSocketConfig,
    UpdateConfigRequest,
    ConfigResponse,
)

__all__ = [
    # Enums
    "MessageType",
    "Channel",
    
    # Core models
    "WebSocketMessage",
    "ConnectedClient",
    
    # Broadcast operations
    "BroadcastRequest",
    "BroadcastResponse",
    "PluginStatusRequest",
    "EntityDiscoveredRequest", 
    "SystemAlertRequest",
    
    # Channel management
    "ChannelSubscriptionRequest",
    "InvestigationRoomRequest",
    
    # Statistics
    "WebSocketStats",
    "DetailedStatsResponse",
    "ChannelStatsResponse",
    "HealthStatus",
    
    # Connection management
    "ConnectionTokenRequest",
    "ConnectionTokenResponse",
    "ClientInfo",
    "ActiveClientsResponse",
    
    # Investigation rooms
    "InvestigationRoomInfo", 
    "InvestigationRoomsResponse",
    
    # Message history
    "MessageHistory",
    "MessageHistoryResponse",
    
    # Collaboration
    "CollaborationEvent",
    
    # Bulk operations
    "BulkBroadcastRequest",
    "BulkBroadcastResponse",
    
    # Configuration
    "WebSocketConfig",
    "UpdateConfigRequest",
    "ConfigResponse",
]
