"""
Session Manager for InfoTerminal Security
Manages incognito sessions and coordinates security features.
"""

import asyncio
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import structlog

from .ephemeral import EphemeralSessionManager, IncognitoSession
from .auto_wipe import AutoWipeManager

logger = structlog.get_logger()

@dataclass
class SecurityStatus:
    """Overall security status."""
    active_sessions: int
    ephemeral_containers: int
    memory_only_mode: bool
    auto_wipe_enabled: bool
    last_updated: float

class SessionManager:
    """Manages security sessions and coordinates security components."""
    
    def __init__(self):
        self.ephemeral_manager = EphemeralSessionManager()
        self.wipe_manager = AutoWipeManager()
        self.active_sessions: Dict[str, IncognitoSession] = {}
        self.security_status = SecurityStatus(
            active_sessions=0,
            ephemeral_containers=0,
            memory_only_mode=False,
            auto_wipe_enabled=True,
            last_updated=time.time()
        )
        
    async def initialize(self):
        """Initialize the session manager and all security components."""
        logger.info("Initializing security session manager")
        
        try:
            await self.ephemeral_manager.initialize()
            await self.wipe_manager.initialize()
            
            # Start status update task
            asyncio.create_task(self._update_status_loop())
            
            logger.info("Security session manager initialized")
            
        except Exception as e:
            logger.error("Failed to initialize session manager", error=str(e))
            raise
    
    async def start_incognito_session(
        self,
        session_id: str,
        auto_wipe_minutes: Optional[int] = None,
        memory_only_mode: bool = True,
        isolated_containers: bool = True
    ) -> IncognitoSession:
        """Start a new incognito session with full security features."""
        
        logger.info(
            "Starting incognito session",
            session_id=session_id,
            auto_wipe_minutes=auto_wipe_minutes,
            memory_only_mode=memory_only_mode
        )
        
        try:
            # Start ephemeral session
            session = await self.ephemeral_manager.start_session(
                session_id=session_id,
                auto_wipe_minutes=auto_wipe_minutes,
                memory_only_mode=memory_only_mode,
                isolated_containers=isolated_containers
            )
            
            # Schedule auto-wipe if configured
            if auto_wipe_minutes:
                await self.wipe_manager.schedule_auto_wipe(
                    session_id=session_id,
                    delay_minutes=auto_wipe_minutes
                )
            
            # Track session
            self.active_sessions[session_id] = session
            
            # Update security status
            await self._update_security_status()
            
            logger.info("Incognito session started successfully", session_id=session_id)
            return session
            
        except Exception as e:
            logger.error("Failed to start incognito session", session_id=session_id, error=str(e))
            raise
    
    async def stop_incognito_session(self, session_id: str) -> bool:
        """Stop an incognito session and clean up resources."""
        
        logger.info("Stopping incognito session", session_id=session_id)
        
        try:
            # Cancel auto-wipe
            await self.wipe_manager.cancel_auto_wipe(session_id)
            
            # Stop ephemeral session
            success = await self.ephemeral_manager.stop_session(session_id)
            
            # Remove from tracking
            if session_id in self.active_sessions:
                del self.active_sessions[session_id]
            
            # Update security status
            await self._update_security_status()
            
            logger.info("Incognito session stopped", session_id=session_id, success=success)
            return success
            
        except Exception as e:
            logger.error("Failed to stop incognito session", session_id=session_id, error=str(e))
            return False
    
    async def wipe_incognito_session(self, session_id: str, secure: bool = True) -> bool:
        """Wipe all data for an incognito session."""
        
        logger.info("Wiping incognito session", session_id=session_id, secure=secure)
        
        try:
            # Scan data categories for the session
            categories = await self.wipe_manager.scan_data_categories(session_id)
            
            # Wipe all categories
            for category in categories:
                await self.wipe_manager.wipe_category(
                    category_id=category.id,
                    session_id=session_id,
                    secure=secure,
                    overwrite_passes=3 if secure else 1
                )
            
            # Wipe ephemeral session
            success = await self.ephemeral_manager.wipe_session(session_id, secure=secure)
            
            # Remove from tracking
            if session_id in self.active_sessions:
                del self.active_sessions[session_id]
            
            # Update security status
            await self._update_security_status()
            
            logger.info("Incognito session wiped", session_id=session_id, success=success)
            return success
            
        except Exception as e:
            logger.error("Failed to wipe incognito session", session_id=session_id, error=str(e))
            return False
    
    async def get_session_status(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed status for a specific session."""
        
        session = self.active_sessions.get(session_id)
        if not session:
            return None
        
        # Get containers
        containers = await self.ephemeral_manager.get_session_containers(session_id)
        
        # Get wipe status
        wipe_status = self.wipe_manager.get_wipe_status(session_id)
        
        return {
            "session": asdict(session),
            "containers": [asdict(c) for c in containers],
            "wipe_status": wipe_status,
            "security_features": {
                "memory_only_mode": session.memory_only_mode,
                "isolated_containers": session.isolated_containers,
                "auto_wipe_enabled": wipe_status["auto_wipe_scheduled"]
            }
        }
    
    async def get_session_containers(self, session_id: str) -> List[Dict[str, Any]]:
        """Get containers for a specific session."""
        containers = await self.ephemeral_manager.get_session_containers(session_id)
        return [asdict(c) for c in containers]
    
    async def get_data_categories(self, session_id: str) -> List[Dict[str, Any]]:
        """Get data categories for wiping."""
        categories = await self.wipe_manager.scan_data_categories(session_id)
        return [asdict(c) for c in categories]
    
    async def wipe_data_category(
        self, 
        category_id: str, 
        session_id: str,
        secure: bool = True
    ) -> Dict[str, Any]:
        """Wipe a specific data category."""
        progress = await self.wipe_manager.wipe_category(
            category_id=category_id,
            session_id=session_id,
            secure=secure
        )
        return asdict(progress)
    
    async def get_security_status(self) -> Dict[str, Any]:
        """Get overall security status."""
        await self._update_security_status()
        return {
            "active_sessions": self.security_status.active_sessions,
            "ephemeral_containers": self.security_status.ephemeral_containers,
            "memory_only_mode": self.security_status.memory_only_mode,
            "auto_wipe_enabled": self.security_status.auto_wipe_enabled,
            "last_updated": self.security_status.last_updated,
            "sessions": {
                session_id: asdict(session) 
                for session_id, session in self.active_sessions.items()
            }
        }
    
    async def emergency_shutdown(self):
        """Emergency shutdown with secure data wiping."""
        logger.warning("Emergency shutdown initiated")
        
        try:
            # Emergency wipe all data
            await self.wipe_manager.emergency_wipe_all()
            
            # Stop all sessions
            for session_id in list(self.active_sessions.keys()):
                await self.stop_incognito_session(session_id)
            
            logger.warning("Emergency shutdown completed")
            
        except Exception as e:
            logger.error("Emergency shutdown failed", error=str(e))
            raise
    
    async def _update_security_status(self):
        """Update internal security status."""
        
        # Count active sessions
        active_count = len(self.active_sessions)
        
        # Count ephemeral containers
        container_count = 0
        for session_id in self.active_sessions:
            containers = await self.ephemeral_manager.get_session_containers(session_id)
            container_count += len(containers)
        
        # Check if any session has memory-only mode
        memory_only = any(
            session.memory_only_mode 
            for session in self.active_sessions.values()
        )
        
        self.security_status = SecurityStatus(
            active_sessions=active_count,
            ephemeral_containers=container_count,
            memory_only_mode=memory_only,
            auto_wipe_enabled=True,  # Always enabled
            last_updated=time.time()
        )
    
    async def _update_status_loop(self):
        """Background task to update security status."""
        while True:
            try:
                await self._update_security_status()
                await asyncio.sleep(30)  # Update every 30 seconds
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error("Status update failed", error=str(e))
                await asyncio.sleep(60)  # Longer delay on error
    
    async def cleanup(self):
        """Cleanup session manager and all resources."""
        logger.info("Cleaning up security session manager")
        
        try:
            # Stop all active sessions
            for session_id in list(self.active_sessions.keys()):
                await self.stop_incognito_session(session_id)
            
            # Cleanup components
            await self.ephemeral_manager.cleanup()
            await self.wipe_manager.cleanup()
            
            logger.info("Security session manager cleanup completed")
            
        except Exception as e:
            logger.error("Cleanup failed", error=str(e))
