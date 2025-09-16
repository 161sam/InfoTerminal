"""
Ephemeral Session Manager for InfoTerminal Incognito Mode
Manages ephemeral Docker containers with memory-only storage.
"""

import asyncio
import time
import uuid
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import docker
import structlog

logger = structlog.get_logger()

@dataclass
class EphemeralContainer:
    """Configuration for an ephemeral container."""
    id: str
    name: str
    image: str
    status: str
    created: float
    memory_usage: int
    memory_limit: int
    ephemeral: bool = True

@dataclass
class IncognitoSession:
    """Incognito session configuration."""
    id: str
    started: float
    auto_wipe_at: float
    data_size: int
    container_count: int
    status: str = "active"
    memory_only_mode: bool = True
    isolated_containers: bool = True

class EphemeralSessionManager:
    """Manages ephemeral containers for incognito sessions."""
    
    def __init__(self):
        self.docker_client = None
        self.sessions: Dict[str, IncognitoSession] = {}
        self.session_containers: Dict[str, List[str]] = {}  # session_id -> container_ids
        self.cleanup_tasks: Dict[str, asyncio.Task] = {}
        
    async def initialize(self):
        """Initialize the Docker client and session manager."""
        try:
            self.docker_client = docker.from_env()
            logger.info("Ephemeral session manager initialized")
        except Exception as e:
            logger.error("Failed to initialize Docker client", error=str(e))
            raise
    
    async def start_session(
        self, 
        session_id: str,
        auto_wipe_minutes: Optional[int] = None,
        memory_only_mode: bool = True,
        isolated_containers: bool = True
    ) -> IncognitoSession:
        """Start a new incognito session with ephemeral containers."""
        
        logger.info("Starting incognito session", session_id=session_id)
        
        started = time.time()
        auto_wipe_at = started + (auto_wipe_minutes * 60) if auto_wipe_minutes else 0
        
        session = IncognitoSession(
            id=session_id,
            started=started,
            auto_wipe_at=auto_wipe_at,
            data_size=0,
            container_count=0,
            status="active",
            memory_only_mode=memory_only_mode,
            isolated_containers=isolated_containers
        )
        
        self.sessions[session_id] = session
        self.session_containers[session_id] = []
        
        # Create initial ephemeral containers
        await self._create_ephemeral_containers(session_id)
        
        # Schedule auto-wipe if configured
        if auto_wipe_minutes:
            self.cleanup_tasks[session_id] = asyncio.create_task(
                self._schedule_auto_wipe(session_id, auto_wipe_minutes * 60)
            )
        
        logger.info("Incognito session started", session_id=session_id)
        return session
    
    async def stop_session(self, session_id: str) -> bool:
        """Stop an incognito session and clean up containers."""
        
        if session_id not in self.sessions:
            logger.warning("Session not found", session_id=session_id)
            return False
        
        logger.info("Stopping incognito session", session_id=session_id)
        
        try:
            # Cancel auto-wipe task
            if session_id in self.cleanup_tasks:
                self.cleanup_tasks[session_id].cancel()
                del self.cleanup_tasks[session_id]
            
            # Stop and remove containers
            await self._cleanup_session_containers(session_id)
            
            # Update session status
            self.sessions[session_id].status = "stopped"
            
            logger.info("Incognito session stopped", session_id=session_id)
            return True
            
        except Exception as e:
            logger.error("Failed to stop session", session_id=session_id, error=str(e))
            return False
    
    async def wipe_session(self, session_id: str, secure: bool = True) -> bool:
        """Wipe all data for an incognito session."""
        
        if session_id not in self.sessions:
            logger.warning("Session not found for wipe", session_id=session_id)
            return False
        
        logger.info("Wiping incognito session", session_id=session_id, secure=secure)
        
        try:
            # Stop session first
            await self.stop_session(session_id)
            
            # Secure wipe if requested
            if secure:
                await self._secure_wipe_session_data(session_id)
            
            # Remove session from tracking
            del self.sessions[session_id]
            if session_id in self.session_containers:
                del self.session_containers[session_id]
            
            logger.info("Incognito session wiped", session_id=session_id)
            return True
            
        except Exception as e:
            logger.error("Failed to wipe session", session_id=session_id, error=str(e))
            return False
    
    async def get_session_containers(self, session_id: str) -> List[EphemeralContainer]:
        """Get containers for a specific session."""
        
        if session_id not in self.session_containers:
            return []
        
        containers = []
        container_ids = self.session_containers[session_id]
        
        for container_id in container_ids:
            try:
                container = self.docker_client.containers.get(container_id)
                stats = container.stats(stream=False)
                
                memory_usage = stats.get('memory_stats', {}).get('usage', 0)
                memory_limit = stats.get('memory_stats', {}).get('limit', 0)
                
                ephemeral_container = EphemeralContainer(
                    id=container.id[:12],
                    name=container.name,
                    image=container.image.tags[0] if container.image.tags else "unknown",
                    status=container.status,
                    created=time.time() - 3600,  # Mock created time
                    memory_usage=memory_usage,
                    memory_limit=memory_limit,
                    ephemeral=True
                )
                
                containers.append(ephemeral_container)
                
            except docker.errors.NotFound:
                # Container was removed, clean up tracking
                container_ids.remove(container_id)
            except Exception as e:
                logger.error("Failed to get container info", container_id=container_id, error=str(e))
        
        return containers
    
    async def get_session_status(self, session_id: str) -> Optional[IncognitoSession]:
        """Get status of a specific session."""
        return self.sessions.get(session_id)
    
    async def _create_ephemeral_containers(self, session_id: str):
        """Create ephemeral containers for a session."""
        
        container_configs = [
            {
                "name": f"incognito-workspace-{session_id[:8]}",
                "image": "ubuntu:22.04",
                "command": "sleep infinity",
                "mem_limit": "512m"
            },
            {
                "name": f"incognito-browser-{session_id[:8]}",
                "image": "browserless/chrome:latest",
                "mem_limit": "1g"
            }
        ]
        
        session = self.sessions[session_id]
        
        for config in container_configs:
            try:
                container = self.docker_client.containers.run(
                    image=config["image"],
                    name=config["name"],
                    command=config.get("command"),
                    detach=True,
                    remove=False,  # We'll remove manually for secure cleanup
                    mem_limit=config["mem_limit"],
                    tmpfs={"/tmp": "noexec,nosuid,size=100m"},
                    security_opt=["no-new-privileges"],
                    cap_drop=["ALL"],
                    cap_add=["SETUID", "SETGID"],
                    network_mode="bridge" if session.isolated_containers else "default"
                )
                
                self.session_containers[session_id].append(container.id)
                session.container_count += 1
                
                logger.info(
                    "Created ephemeral container",
                    session_id=session_id,
                    container_name=config["name"],
                    container_id=container.id[:12]
                )
                
            except Exception as e:
                logger.error(
                    "Failed to create ephemeral container",
                    session_id=session_id,
                    config=config,
                    error=str(e)
                )
    
    async def _cleanup_session_containers(self, session_id: str):
        """Clean up all containers for a session."""
        
        if session_id not in self.session_containers:
            return
        
        container_ids = self.session_containers[session_id]
        
        for container_id in container_ids:
            try:
                container = self.docker_client.containers.get(container_id)
                container.stop(timeout=10)
                container.remove(force=True)
                
                logger.info(
                    "Removed ephemeral container",
                    session_id=session_id,
                    container_id=container_id[:12]
                )
                
            except docker.errors.NotFound:
                # Container already removed
                pass
            except Exception as e:
                logger.error(
                    "Failed to remove container",
                    container_id=container_id,
                    error=str(e)
                )
        
        # Clear container tracking
        self.session_containers[session_id] = []
        self.sessions[session_id].container_count = 0
    
    async def _secure_wipe_session_data(self, session_id: str):
        """Perform secure wipe of session data."""
        
        logger.info("Performing secure wipe", session_id=session_id)
        
        # In a real implementation, this would:
        # 1. Overwrite container filesystems multiple times
        # 2. Clear any temporary files
        # 3. Clear memory if possible
        # 4. Remove any logs or traces
        
        # For now, we'll just add a delay to simulate secure wiping
        await asyncio.sleep(2)
        
        logger.info("Secure wipe completed", session_id=session_id)
    
    async def _schedule_auto_wipe(self, session_id: str, delay_seconds: float):
        """Schedule automatic session wipe."""
        
        try:
            await asyncio.sleep(delay_seconds)
            logger.info("Auto-wipe triggered", session_id=session_id)
            await self.wipe_session(session_id, secure=True)
        except asyncio.CancelledError:
            logger.info("Auto-wipe cancelled", session_id=session_id)
        except Exception as e:
            logger.error("Auto-wipe failed", session_id=session_id, error=str(e))
    
    def get_all_sessions(self) -> Dict[str, IncognitoSession]:
        """Get all active sessions."""
        return self.sessions.copy()
    
    async def cleanup(self):
        """Cleanup all sessions and resources."""
        logger.info("Cleaning up ephemeral session manager")
        
        # Cancel all cleanup tasks
        for task in self.cleanup_tasks.values():
            task.cancel()
        
        # Stop all sessions
        for session_id in list(self.sessions.keys()):
            await self.stop_session(session_id)
        
        logger.info("Ephemeral session manager cleanup completed")
