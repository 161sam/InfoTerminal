"""
Tor Controller for InfoTerminal Egress Gateway
Manages Tor connection and identity rotation
"""

import asyncio
import subprocess
import time
from typing import Optional
import socket
import structlog

try:
    from stem import Signal
    from stem.control import Controller
    STEM_AVAILABLE = True
except ImportError:
    STEM_AVAILABLE = False

logger = structlog.get_logger()

class TorController:
    """Controls Tor daemon and circuit management."""
    
    def __init__(self):
        self.controller: Optional[Controller] = None
        self.is_running = False
        self.control_port = 9051
        self.socks_port = 9050
        self.control_password = None
        self.last_new_identity = 0.0
        self.min_identity_interval = 10.0  # Minimum seconds between new identities
        
    async def initialize(self):
        """Initialize Tor controller."""
        logger.info("Initializing Tor controller")
        
        if not STEM_AVAILABLE:
            logger.warning("Stem library not available, Tor control disabled")
            return
        
        try:
            # Check if Tor is running
            if await self._check_tor_running():
                await self._connect_controller()
                self.is_running = True
                logger.info("Tor controller connected successfully")
            else:
                logger.warning("Tor daemon not running, attempting to start")
                # In production, you might want to start Tor here
                # await self._start_tor_daemon()
                
        except Exception as e:
            logger.error("Failed to initialize Tor controller", error=str(e))
    
    async def _check_tor_running(self) -> bool:
        """Check if Tor daemon is running."""
        try:
            # Try to connect to Tor SOCKS port
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex(('127.0.0.1', self.socks_port))
            sock.close()
            
            return result == 0
            
        except Exception:
            return False
    
    async def _connect_controller(self):
        """Connect to Tor control port."""
        try:
            self.controller = Controller.from_port(port=self.control_port)
            self.controller.authenticate()
            
            # Get circuit information
            circuits = self.controller.get_circuits()
            logger.info(
                "Connected to Tor controller",
                circuits_count=len(circuits)
            )
            
        except Exception as e:
            logger.error("Failed to connect to Tor controller", error=str(e))
            self.controller = None
    
    async def _start_tor_daemon(self):
        """Start Tor daemon (for development/docker environments)."""
        try:
            # Basic Tor configuration
            tor_config = {
                'SocksPort': str(self.socks_port),
                'ControlPort': str(self.control_port),
                'DataDirectory': '/tmp/tor-data',
                'Log': 'notice stdout'
            }
            
            # In a real implementation, you would use stem.process.launch_tor_with_config
            # For now, we assume Tor is managed externally (docker, systemd, etc.)
            logger.info("Tor daemon management not implemented in this version")
            
        except Exception as e:
            logger.error("Failed to start Tor daemon", error=str(e))
    
    def is_available(self) -> bool:
        """Check if Tor is available and connected."""
        return self.is_running and self.controller is not None and STEM_AVAILABLE
    
    def is_circuit_established(self) -> bool:
        """Check if Tor has established circuits."""
        if not self.is_available():
            return False
        
        try:
            circuits = self.controller.get_circuits()
            built_circuits = [c for c in circuits if c.status == 'BUILT']
            return len(built_circuits) > 0
            
        except Exception as e:
            logger.error("Failed to check Tor circuits", error=str(e))
            return False
    
    async def new_identity(self) -> bool:
        """Request a new Tor identity (new circuit)."""
        
        # Rate limiting for new identities
        current_time = time.time()
        if current_time - self.last_new_identity < self.min_identity_interval:
            logger.warning(
                "New identity request rate limited",
                last_request=self.last_new_identity,
                min_interval=self.min_identity_interval
            )
            return False
        
        if not self.is_available():
            logger.warning("Cannot request new identity: Tor not available")
            return False
        
        try:
            logger.info("Requesting new Tor identity")
            
            # Signal Tor to create new circuits
            self.controller.signal(Signal.NEWNYM)
            
            # Wait briefly for new circuit establishment
            await asyncio.sleep(2.0)
            
            self.last_new_identity = current_time
            
            logger.info("New Tor identity requested successfully")
            return True
            
        except Exception as e:
            logger.error("Failed to request new Tor identity", error=str(e))
            return False
    
    def get_current_ip(self) -> Optional[str]:
        """Get current exit IP through Tor (for verification)."""
        if not self.is_available():
            return None
        
        try:
            # This would require making an HTTP request through Tor
            # to a service like httpbin.org/ip
            # Implementation depends on your HTTP client setup
            return None
            
        except Exception as e:
            logger.error("Failed to get current Tor IP", error=str(e))
            return None
    
    def get_circuit_info(self) -> dict:
        """Get information about current Tor circuits."""
        if not self.is_available():
            return {}
        
        try:
            circuits = self.controller.get_circuits()
            
            circuit_info = {
                "total_circuits": len(circuits),
                "built_circuits": len([c for c in circuits if c.status == 'BUILT']),
                "building_circuits": len([c for c in circuits if c.status == 'BUILDING']),
                "failed_circuits": len([c for c in circuits if c.status == 'FAILED'])
            }
            
            # Get info about active circuits
            if circuits:
                active_circuits = [c for c in circuits if c.status == 'BUILT']
                if active_circuits:
                    circuit = active_circuits[0]
                    circuit_info["active_circuit"] = {
                        "id": circuit.id,
                        "status": circuit.status,
                        "purpose": circuit.purpose,
                        "path_length": len(circuit.path)
                    }
            
            return circuit_info
            
        except Exception as e:
            logger.error("Failed to get circuit info", error=str(e))
            return {}
    
    async def cleanup(self):
        """Cleanup Tor controller resources."""
        logger.info("Cleaning up Tor controller")
        
        if self.controller:
            try:
                self.controller.close()
            except Exception as e:
                logger.error("Error closing Tor controller", error=str(e))
            
            self.controller = None
        
        self.is_running = False
