"""
Proxy Manager for InfoTerminal Egress Gateway
Manages different types of proxies: Tor, VPN, HTTP proxies
"""

import asyncio
import time
import random
from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import httpx
import structlog

logger = structlog.get_logger()

class ProxyType(str, Enum):
    """Available proxy types."""
    AUTO = "auto"
    TOR = "tor"
    VPN = "vpn"
    HTTP = "http"
    DIRECT = "direct"

@dataclass
class ProxyConfig:
    """Configuration for a proxy endpoint."""
    name: str
    proxy_url: str
    anonymity_level: str  # high, medium, low
    type: ProxyType
    country: Optional[str] = None
    latency: Optional[float] = None
    success_rate: float = 1.0
    last_used: float = 0.0
    is_healthy: bool = True

class ProxyManager:
    """Manages proxy pool and rotation for anonymized requests."""
    
    def __init__(self):
        self.proxies: Dict[str, ProxyConfig] = {}
        self.active_proxy: Optional[str] = None
        self.request_count = 0
        self.last_rotation = 0.0
        self.health_check_interval = 300  # 5 minutes
        self.rotation_threshold = 10  # Rotate after N requests
        
    async def initialize(self):
        """Initialize proxy manager with available proxies."""
        logger.info("Initializing proxy manager")
        
        # Load proxy configurations
        await self._load_proxy_configs()
        
        # Start health check task
        asyncio.create_task(self._health_check_loop())
        
        logger.info(
            "Proxy manager initialized",
            proxy_count=len(self.proxies),
            active_proxy=self.active_proxy
        )
    
    async def _load_proxy_configs(self):
        """Load proxy configurations from environment/config."""
        
        # Tor proxy (if available)
        tor_proxy = ProxyConfig(
            name="tor",
            proxy_url="socks5://127.0.0.1:9050",
            anonymity_level="high",
            type=ProxyType.TOR,
            country="unknown"
        )
        
        # Check if Tor is available
        if await self._test_proxy(tor_proxy):
            self.proxies["tor"] = tor_proxy
            logger.info("Tor proxy available")
        else:
            logger.warning("Tor proxy not available")
        
        # Example VPN proxies (would be loaded from config)
        vpn_configs = [
            {
                "name": "vpn_us_east",
                "url": "http://user:pass@vpn-us-east.example.com:8080",
                "country": "US",
                "anonymity": "medium"
            },
            {
                "name": "vpn_eu_west", 
                "url": "http://user:pass@vpn-eu-west.example.com:8080",
                "country": "DE",
                "anonymity": "medium"
            }
        ]
        
        # Load VPN proxies (in production, these would come from config/env)
        for config in vpn_configs:
            vpn_proxy = ProxyConfig(
                name=config["name"],
                proxy_url=config["url"],
                anonymity_level=config["anonymity"],
                type=ProxyType.VPN,
                country=config["country"]
            )
            
            # In production, test VPN connectivity
            # if await self._test_proxy(vpn_proxy):
            #     self.proxies[config["name"]] = vpn_proxy
        
        # Example HTTP proxies
        http_configs = [
            {
                "name": "http_public_1",
                "url": "http://proxy1.example.com:3128",
                "anonymity": "low"
            },
            {
                "name": "http_public_2",
                "url": "http://proxy2.example.com:8080", 
                "anonymity": "low"
            }
        ]
        
        # Load HTTP proxies (in production, test these)
        for config in http_configs:
            http_proxy = ProxyConfig(
                name=config["name"],
                proxy_url=config["url"],
                anonymity_level=config["anonymity"],
                type=ProxyType.HTTP
            )
            
            # In production, test HTTP proxy connectivity
            # if await self._test_proxy(http_proxy):
            #     self.proxies[config["name"]] = http_proxy
        
        # Direct connection fallback
        direct_proxy = ProxyConfig(
            name="direct",
            proxy_url="",
            anonymity_level="none",
            type=ProxyType.DIRECT
        )
        self.proxies["direct"] = direct_proxy
        
        # Set initial active proxy
        if "tor" in self.proxies:
            self.active_proxy = "tor"
        elif self.proxies:
            self.active_proxy = next(iter(self.proxies.keys()))
    
    async def _test_proxy(self, proxy: ProxyConfig) -> bool:
        """Test if a proxy is working."""
        try:
            start_time = time.time()
            
            async with httpx.AsyncClient(
                proxies=proxy.proxy_url if proxy.proxy_url else None,
                timeout=10.0
            ) as client:
                response = await client.get("http://httpbin.org/ip")
                
                if response.status_code == 200:
                    proxy.latency = time.time() - start_time
                    proxy.is_healthy = True
                    logger.debug(
                        "Proxy test successful",
                        proxy=proxy.name,
                        latency=proxy.latency
                    )
                    return True
                    
        except Exception as e:
            logger.warning(
                "Proxy test failed",
                proxy=proxy.name,
                error=str(e)
            )
            proxy.is_healthy = False
        
        return False
    
    async def get_proxy(self, preferred_type: ProxyType = ProxyType.AUTO) -> Optional[ProxyConfig]:
        """Get the best available proxy for a request."""
        
        self.request_count += 1
        
        # Auto-rotate if threshold reached
        if (self.request_count % self.rotation_threshold == 0 and 
            time.time() - self.last_rotation > 60):  # At least 1 minute between rotations
            await self.rotate_identity()
        
        # Filter proxies by type preference
        if preferred_type == ProxyType.AUTO:
            available_proxies = [p for p in self.proxies.values() if p.is_healthy]
        else:
            available_proxies = [
                p for p in self.proxies.values() 
                if p.type == preferred_type and p.is_healthy
            ]
        
        if not available_proxies:
            # Fallback to direct connection
            return self.proxies.get("direct")
        
        # Select proxy based on anonymity and performance
        if preferred_type == ProxyType.AUTO:
            # Prefer high anonymity proxies
            high_anonymity = [p for p in available_proxies if p.anonymity_level == "high"]
            if high_anonymity:
                proxy = random.choice(high_anonymity)
            else:
                proxy = random.choice(available_proxies)
        else:
            proxy = random.choice(available_proxies)
        
        # Update usage stats
        proxy.last_used = time.time()
        self.active_proxy = proxy.name
        
        logger.debug(
            "Selected proxy for request",
            proxy=proxy.name,
            type=proxy.type,
            anonymity=proxy.anonymity_level
        )
        
        return proxy
    
    async def rotate_identity(self, proxy_type: Optional[ProxyType] = None):
        """Rotate to a different proxy/identity."""
        
        logger.info("Rotating proxy identity", proxy_type=proxy_type)
        
        if proxy_type:
            # Rotate within specific type
            type_proxies = [
                p for p in self.proxies.values() 
                if p.type == proxy_type and p.is_healthy and p.name != self.active_proxy
            ]
        else:
            # Rotate to any different proxy
            type_proxies = [
                p for p in self.proxies.values() 
                if p.is_healthy and p.name != self.active_proxy
            ]
        
        if type_proxies:
            new_proxy = random.choice(type_proxies)
            self.active_proxy = new_proxy.name
            self.last_rotation = time.time()
            
            logger.info(
                "Rotated to new proxy",
                new_proxy=new_proxy.name,
                type=new_proxy.type,
                anonymity=new_proxy.anonymity_level
            )
    
    async def _health_check_loop(self):
        """Periodic health checks for all proxies."""
        
        while True:
            try:
                await asyncio.sleep(self.health_check_interval)
                
                logger.debug("Starting proxy health checks")
                
                for proxy in self.proxies.values():
                    if proxy.type != ProxyType.DIRECT:
                        await self._test_proxy(proxy)
                
                logger.debug(
                    "Proxy health checks completed",
                    healthy_count=sum(1 for p in self.proxies.values() if p.is_healthy)
                )
                
            except Exception as e:
                logger.error("Health check loop error", error=str(e))
    
    def get_vpn_pools(self) -> List[str]:
        """Get list of available VPN pools."""
        return [
            p.name for p in self.proxies.values() 
            if p.type == ProxyType.VPN and p.is_healthy
        ]
    
    def get_proxy_pools(self) -> List[str]:
        """Get list of available proxy pools."""
        return [
            p.name for p in self.proxies.values() 
            if p.type in [ProxyType.HTTP, ProxyType.TOR] and p.is_healthy
        ]
    
    def get_active_proxy(self) -> str:
        """Get currently active proxy."""
        return self.active_proxy or "none"
    
    def get_request_count(self) -> int:
        """Get total request count."""
        return self.request_count
    
    def get_last_rotation(self) -> float:
        """Get timestamp of last rotation."""
        return self.last_rotation
    
    async def cleanup(self):
        """Cleanup proxy manager resources."""
        logger.info("Cleaning up proxy manager")
        # Any cleanup needed for proxy connections
