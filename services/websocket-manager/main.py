"""
WebSocket Manager Service

Provides real-time updates for InfoTerminal including:
- Live plugin execution status
- Graph updates when new entities are discovered
- Collaborative investigation features
- System notifications and alerts
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
import logging
import uuid
from datetime import datetime
from typing import Dict, List, Set, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import redis
import aioredis
from pydantic import BaseModel
import jwt
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="WebSocket Manager Service", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessageType(str, Enum):
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
    GLOBAL = "global"
    USER = "user"
    INVESTIGATION = "investigation"
    PLUGIN_EXECUTION = "plugin_execution"
    GRAPH_ANALYSIS = "graph_analysis"
    SYSTEM_HEALTH = "system_health"

@dataclass
class WebSocketMessage:
    """WebSocket message structure"""
    id: str
    type: MessageType
    channel: Channel
    timestamp: datetime
    data: Dict[str, Any]
    sender_id: Optional[str] = None
    target_user_id: Optional[str] = None
    investigation_id: Optional[str] = None
    metadata: Dict[str, Any] = None

@dataclass
class ConnectedClient:
    """Connected WebSocket client information"""
    websocket: WebSocket
    client_id: str
    user_id: Optional[str]
    connected_at: datetime
    last_ping: datetime
    subscribed_channels: Set[Channel]
    investigation_ids: Set[str]
    metadata: Dict[str, Any]

class WebSocketManager:
    """Manages WebSocket connections and message broadcasting"""
    
    def __init__(self):
        # Active connections
        self.connections: Dict[str, ConnectedClient] = {}
        
        # Channel subscriptions
        self.channel_subscribers: Dict[Channel, Set[str]] = {
            channel: set() for channel in Channel
        }
        
        # Investigation room subscriptions
        self.investigation_rooms: Dict[str, Set[str]] = {}
        
        # Redis for pub/sub across multiple service instances
        self.redis: Optional[aioredis.Redis] = None
        
        # Message queue for offline users
        self.offline_messages: Dict[str, List[WebSocketMessage]] = {}
        
        # Statistics
        self.stats = {
            "total_connections": 0,
            "active_connections": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "channels_active": 0
        }
    
    async def initialize_redis(self):
        """Initialize Redis connection for pub/sub"""
        try:
            self.redis = await aioredis.from_url("redis://localhost:6379")
            logger.info("Connected to Redis for WebSocket pub/sub")
            
            # Subscribe to Redis channels for distributed messaging
            await self._setup_redis_subscriptions()
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}")
    
    async def _setup_redis_subscriptions(self):
        """Setup Redis pub/sub subscriptions"""
        if not self.redis:
            return
        
        # Subscribe to distributed message channels
        pubsub = self.redis.pubsub()
        await pubsub.subscribe(
            "websocket:broadcast",
            "websocket:user_message",
            "websocket:investigation_message",
            "websocket:system_alert"
        )
        
        # Start background task to handle Redis messages
        asyncio.create_task(self._handle_redis_messages(pubsub))
    
    async def _handle_redis_messages(self, pubsub):
        """Handle incoming Redis pub/sub messages"""
        try:
            async for message in pubsub.listen():
                if message["type"] == "message":
                    try:
                        data = json.loads(message["data"].decode())
                        ws_message = WebSocketMessage(**data)
                        await self._distribute_message(ws_message)
                    except Exception as e:
                        logger.error(f"Failed to process Redis message: {e}")
        except Exception as e:
            logger.error(f"Redis message handler error: {e}")
    
    async def connect(self, websocket: WebSocket, client_id: str, 
                     user_id: Optional[str] = None, 
                     token: Optional[str] = None) -> bool:
        """Accept and register a new WebSocket connection"""
        try:
            await websocket.accept()
            
            # Validate token if provided
            if token and not self._validate_token(token):
                await websocket.close(code=1008, reason="Invalid token")
                return False
            
            # Create client record
            client = ConnectedClient(
                websocket=websocket,
                client_id=client_id,
                user_id=user_id,
                connected_at=datetime.now(),
                last_ping=datetime.now(),
                subscribed_channels={Channel.GLOBAL},  # Default subscription
                investigation_ids=set(),
                metadata={}
            )
            
            self.connections[client_id] = client
            self.stats["total_connections"] += 1
            self.stats["active_connections"] = len(self.connections)
            
            # Subscribe to global channel
            self.channel_subscribers[Channel.GLOBAL].add(client_id)
            
            # Send connection confirmation
            await self._send_to_client(client_id, WebSocketMessage(
                id=str(uuid.uuid4()),
                type=MessageType.USER_JOINED,
                channel=Channel.GLOBAL,
                timestamp=datetime.now(),
                data={
                    "client_id": client_id,
                    "user_id": user_id,
                    "message": "Connected successfully"
                }
            ))
            
            # Send any queued offline messages
            if user_id and user_id in self.offline_messages:
                for message in self.offline_messages[user_id]:
                    await self._send_to_client(client_id, message)
                del self.offline_messages[user_id]
            
            logger.info(f"WebSocket client connected: {client_id} (user: {user_id})")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect WebSocket client: {e}")
            return False
    
    async def disconnect(self, client_id: str):
        """Handle client disconnection"""
        if client_id not in self.connections:
            return
        
        client = self.connections[client_id]
        
        # Remove from all channel subscriptions
        for channel in client.subscribed_channels:
            self.channel_subscribers[channel].discard(client_id)
        
        # Remove from investigation rooms
        for investigation_id in client.investigation_ids:
            if investigation_id in self.investigation_rooms:
                self.investigation_rooms[investigation_id].discard(client_id)
                if not self.investigation_rooms[investigation_id]:
                    del self.investigation_rooms[investigation_id]
        
        # Remove client
        del self.connections[client_id]
        self.stats["active_connections"] = len(self.connections)
        
        logger.info(f"WebSocket client disconnected: {client_id}")
    
    async def subscribe_to_channel(self, client_id: str, channel: Channel) -> bool:
        """Subscribe client to a specific channel"""
        if client_id not in self.connections:
            return False
        
        client = self.connections[client_id]
        client.subscribed_channels.add(channel)
        self.channel_subscribers[channel].add(client_id)
        
        logger.info(f"Client {client_id} subscribed to channel {channel}")
        return True
    
    async def unsubscribe_from_channel(self, client_id: str, channel: Channel) -> bool:
        """Unsubscribe client from a specific channel"""
        if client_id not in self.connections:
            return False
        
        client = self.connections[client_id]
        client.subscribed_channels.discard(channel)
        self.channel_subscribers[channel].discard(client_id)
        
        logger.info(f"Client {client_id} unsubscribed from channel {channel}")
        return True
    
    async def join_investigation(self, client_id: str, investigation_id: str) -> bool:
        """Join client to an investigation room"""
        if client_id not in self.connections:
            return False
        
        client = self.connections[client_id]
        client.investigation_ids.add(investigation_id)
        
        if investigation_id not in self.investigation_rooms:
            self.investigation_rooms[investigation_id] = set()
        self.investigation_rooms[investigation_id].add(client_id)
        
        # Notify other users in the investigation
        await self.broadcast_to_investigation(investigation_id, WebSocketMessage(
            id=str(uuid.uuid4()),
            type=MessageType.USER_JOINED,
            channel=Channel.INVESTIGATION,
            timestamp=datetime.now(),
            data={
                "user_id": client.user_id,
                "investigation_id": investigation_id,
                "message": f"User joined investigation"
            },
            sender_id=client.user_id,
            investigation_id=investigation_id
        ), exclude_client=client_id)
        
        logger.info(f"Client {client_id} joined investigation {investigation_id}")
        return True
    
    async def leave_investigation(self, client_id: str, investigation_id: str) -> bool:
        """Remove client from an investigation room"""
        if client_id not in self.connections:
            return False
        
        client = self.connections[client_id]
        client.investigation_ids.discard(investigation_id)
        
        if investigation_id in self.investigation_rooms:
            self.investigation_rooms[investigation_id].discard(client_id)
            if not self.investigation_rooms[investigation_id]:
                del self.investigation_rooms[investigation_id]
        
        # Notify other users in the investigation
        await self.broadcast_to_investigation(investigation_id, WebSocketMessage(
            id=str(uuid.uuid4()),
            type=MessageType.USER_LEFT,
            channel=Channel.INVESTIGATION,
            timestamp=datetime.now(),
            data={
                "user_id": client.user_id,
                "investigation_id": investigation_id,
                "message": f"User left investigation"
            },
            sender_id=client.user_id,
            investigation_id=investigation_id
        ), exclude_client=client_id)
        
        logger.info(f"Client {client_id} left investigation {investigation_id}")
        return True
    
    async def send_to_user(self, user_id: str, message: WebSocketMessage):
        """Send message to a specific user"""
        # Find all connections for this user
        user_clients = [
            client_id for client_id, client in self.connections.items()
            if client.user_id == user_id
        ]
        
        if user_clients:
            for client_id in user_clients:
                await self._send_to_client(client_id, message)
        else:
            # Queue message for offline user
            if user_id not in self.offline_messages:
                self.offline_messages[user_id] = []
            self.offline_messages[user_id].append(message)
            
            # Limit offline message queue
            if len(self.offline_messages[user_id]) > 100:
                self.offline_messages[user_id] = self.offline_messages[user_id][-100:]
    
    async def broadcast_to_channel(self, channel: Channel, message: WebSocketMessage, 
                                  exclude_client: Optional[str] = None):
        """Broadcast message to all subscribers of a channel"""
        subscribers = self.channel_subscribers[channel].copy()
        
        if exclude_client:
            subscribers.discard(exclude_client)
        
        for client_id in subscribers:
            await self._send_to_client(client_id, message)
    
    async def broadcast_to_investigation(self, investigation_id: str, message: WebSocketMessage,
                                       exclude_client: Optional[str] = None):
        """Broadcast message to all users in an investigation room"""
        if investigation_id not in self.investigation_rooms:
            return
        
        room_members = self.investigation_rooms[investigation_id].copy()
        
        if exclude_client:
            room_members.discard(exclude_client)
        
        for client_id in room_members:
            await self._send_to_client(client_id, message)
    
    async def broadcast_to_all(self, message: WebSocketMessage, 
                              exclude_client: Optional[str] = None):
        """Broadcast message to all connected clients"""
        clients = list(self.connections.keys())
        
        if exclude_client:
            clients = [c for c in clients if c != exclude_client]
        
        for client_id in clients:
            await self._send_to_client(client_id, message)
    
    async def _send_to_client(self, client_id: str, message: WebSocketMessage):
        """Send message to a specific client"""
        if client_id not in self.connections:
            return
        
        client = self.connections[client_id]
        
        try:
            message_data = asdict(message)
            # Convert datetime to ISO string for JSON serialization
            message_data["timestamp"] = message.timestamp.isoformat()
            
            await client.websocket.send_text(json.dumps(message_data, default=str))
            self.stats["messages_sent"] += 1
            
            # Update last ping
            client.last_ping = datetime.now()
            
        except Exception as e:
            logger.warning(f"Failed to send message to client {client_id}: {e}")
            # Connection likely broken, remove client
            await self.disconnect(client_id)
    
    async def _distribute_message(self, message: WebSocketMessage):
        """Distribute message based on its routing information"""
        if message.target_user_id:
            await self.send_to_user(message.target_user_id, message)
        elif message.investigation_id:
            await self.broadcast_to_investigation(message.investigation_id, message)
        elif message.channel:
            await self.broadcast_to_channel(message.channel, message)
        else:
            await self.broadcast_to_all(message)
    
    def _validate_token(self, token: str) -> bool:
        """Validate JWT token"""
        try:
            secret = os.getenv("JWT_SECRET", "your-secret-key")
            payload = jwt.decode(token, secret, algorithms=["HS256"])
            return True
        except jwt.InvalidTokenError:
            return False
    
    async def ping_clients(self):
        """Ping all clients to check connection health"""
        current_time = datetime.now()
        disconnected_clients = []
        
        for client_id, client in self.connections.items():
            # Check if client hasn't responded in 60 seconds
            if (current_time - client.last_ping).total_seconds() > 60:
                disconnected_clients.append(client_id)
            else:
                # Send ping
                ping_message = WebSocketMessage(
                    id=str(uuid.uuid4()),
                    type=MessageType.HEALTH_STATUS,
                    channel=Channel.GLOBAL,
                    timestamp=current_time,
                    data={"type": "ping"}
                )
                await self._send_to_client(client_id, ping_message)
        
        # Disconnect stale clients
        for client_id in disconnected_clients:
            await self.disconnect(client_id)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get WebSocket manager statistics"""
        self.stats["channels_active"] = sum(
            1 for subscribers in self.channel_subscribers.values() 
            if subscribers
        )
        
        return {
            **self.stats,
            "investigation_rooms": len(self.investigation_rooms),
            "offline_message_queues": len(self.offline_messages)
        }

# Initialize WebSocket manager
ws_manager = WebSocketManager()

@app.on_event("startup")
async def startup_event():
    await ws_manager.initialize_redis()
    
    # Start periodic ping task
    async def ping_task():
        while True:
            await asyncio.sleep(30)  # Ping every 30 seconds
            await ws_manager.ping_clients()
    
    asyncio.create_task(ping_task())

# WebSocket endpoint
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str, 
                           user_id: Optional[str] = None, 
                           token: Optional[str] = None):
    """Main WebSocket endpoint"""
    connected = await ws_manager.connect(websocket, client_id, user_id, token)
    
    if not connected:
        return
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Handle client message
            await handle_client_message(client_id, message_data)
            
    except WebSocketDisconnect:
        await ws_manager.disconnect(client_id)
    except Exception as e:
        logger.error(f"WebSocket error for client {client_id}: {e}")
        await ws_manager.disconnect(client_id)

async def handle_client_message(client_id: str, message_data: Dict[str, Any]):
    """Handle incoming message from client"""
    try:
        message_type = message_data.get("type")
        
        if message_type == "subscribe":
            channel = Channel(message_data.get("channel"))
            await ws_manager.subscribe_to_channel(client_id, channel)
            
        elif message_type == "unsubscribe":
            channel = Channel(message_data.get("channel"))
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
                            WebSocketMessage(
                                id=str(uuid.uuid4()),
                                type=MessageType.CURSOR_MOVED,
                                channel=Channel.INVESTIGATION,
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

# REST API endpoints for external services

class BroadcastRequest(BaseModel):
    type: MessageType
    channel: Channel
    data: Dict[str, Any]
    target_user_id: Optional[str] = None
    investigation_id: Optional[str] = None
    sender_id: Optional[str] = None

@app.post("/broadcast")
async def broadcast_message(request: BroadcastRequest):
    """Broadcast message via REST API"""
    message = WebSocketMessage(
        id=str(uuid.uuid4()),
        type=request.type,
        channel=request.channel,
        timestamp=datetime.now(),
        data=request.data,
        sender_id=request.sender_id,
        target_user_id=request.target_user_id,
        investigation_id=request.investigation_id
    )
    
    await ws_manager._distribute_message(message)
    return {"success": True, "message_id": message.id}

@app.post("/broadcast/plugin-status")
async def broadcast_plugin_status(
    plugin_id: str,
    status: str,
    progress: Optional[int] = None,
    message: Optional[str] = None,
    error: Optional[str] = None,
    user_id: Optional[str] = None
):
    """Broadcast plugin execution status"""
    message_type = MessageType.PLUGIN_PROGRESS
    
    if status == "started":
        message_type = MessageType.PLUGIN_STARTED
    elif status == "completed":
        message_type = MessageType.PLUGIN_COMPLETED
    elif status == "error":
        message_type = MessageType.PLUGIN_ERROR
    
    ws_message = WebSocketMessage(
        id=str(uuid.uuid4()),
        type=message_type,
        channel=Channel.PLUGIN_EXECUTION,
        timestamp=datetime.now(),
        data={
            "plugin_id": plugin_id,
            "status": status,
            "progress": progress,
            "message": message,
            "error": error
        },
        target_user_id=user_id
    )
    
    await ws_manager._distribute_message(ws_message)
    return {"success": True}

@app.post("/broadcast/entity-discovered")
async def broadcast_entity_discovered(
    entity_id: str,
    entity_type: str,
    entity_name: str,
    investigation_id: Optional[str] = None,
    discovered_by: Optional[str] = None
):
    """Broadcast new entity discovery"""
    ws_message = WebSocketMessage(
        id=str(uuid.uuid4()),
        type=MessageType.ENTITY_DISCOVERED,
        channel=Channel.GRAPH_ANALYSIS,
        timestamp=datetime.now(),
        data={
            "entity_id": entity_id,
            "entity_type": entity_type,
            "entity_name": entity_name,
            "discovered_by": discovered_by
        },
        investigation_id=investigation_id
    )
    
    await ws_manager._distribute_message(ws_message)
    return {"success": True}

@app.post("/broadcast/system-alert")
async def broadcast_system_alert(
    level: str,
    title: str,
    message: str,
    target_user_id: Optional[str] = None
):
    """Broadcast system alert"""
    ws_message = WebSocketMessage(
        id=str(uuid.uuid4()),
        type=MessageType.SYSTEM_ALERT,
        channel=Channel.GLOBAL,
        timestamp=datetime.now(),
        data={
            "level": level,
            "title": title,
            "message": message
        },
        target_user_id=target_user_id
    )
    
    await ws_manager._distribute_message(ws_message)
    return {"success": True}

@app.get("/stats")
async def get_websocket_stats():
    """Get WebSocket manager statistics"""
    return ws_manager.get_stats()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "websocket-manager",
        "active_connections": len(ws_manager.connections),
        "redis_connected": ws_manager.redis is not None
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8083)
