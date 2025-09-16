"""
Auto-Wipe Module for InfoTerminal Security
Handles automatic data wiping and secure deletion.
"""

import asyncio
import os
import time
import shutil
import subprocess
from typing import List, Dict, Optional
from dataclasses import dataclass
from pathlib import Path
import structlog

logger = structlog.get_logger()

@dataclass
class DataCategory:
    """Data category for selective wiping."""
    id: str
    name: str
    description: str
    path: str
    size: int
    file_count: int
    last_accessed: float
    sensitive: bool

@dataclass
class WipeProgress:
    """Progress tracking for wipe operations."""
    category: str
    progress: int
    completed: bool
    error: Optional[str] = None

class AutoWipeManager:
    """Manages automatic data wiping for security."""
    
    def __init__(self):
        self.wipe_tasks: Dict[str, asyncio.Task] = {}
        self.data_categories: Dict[str, DataCategory] = {}
        
    async def initialize(self):
        """Initialize the auto-wipe manager."""
        logger.info("Auto-wipe manager initialized")
    
    async def scan_data_categories(self, session_id: str) -> List[DataCategory]:
        """Scan and categorize data for potential wiping."""
        
        logger.info("Scanning data categories", session_id=session_id)
        
        # Define base paths to scan
        base_paths = [
            "/tmp",
            "/var/tmp", 
            f"/data/sessions/{session_id}" if session_id else None,
            "/data/cache",
            "/data/downloads"
        ]
        
        categories = []
        
        for i, (cat_id, cat_name, description, path) in enumerate([
            ("documents", "Documents", "PDF files, text documents, and reports", "/tmp/documents"),
            ("images", "Images", "Screenshots, photos, and image files", "/tmp/images"),
            ("downloads", "Downloads", "Downloaded files and temporary data", "/tmp/downloads"),
            ("database", "Database", "Temporary database files and caches", "/tmp/db"),
            ("cache", "Cache", "Application cache and temporary files", "/tmp/cache")
        ]):
            # Mock data for demonstration
            category = DataCategory(
                id=cat_id,
                name=cat_name,
                description=description,
                path=path,
                size=1024 * 1024 * (i + 1),  # Mock sizes
                file_count=(i + 1) * 10,
                last_accessed=time.time() - (i * 3600),  # Varying access times
                sensitive=cat_id in ["documents", "database"]
            )
            categories.append(category)
            self.data_categories[cat_id] = category
        
        logger.info(
            "Data categories scanned", 
            session_id=session_id,
            category_count=len(categories)
        )
        
        return categories
    
    async def wipe_category(
        self, 
        category_id: str, 
        session_id: str,
        secure: bool = True,
        overwrite_passes: int = 3
    ) -> WipeProgress:
        """Wipe a specific data category."""
        
        logger.info(
            "Starting category wipe",
            category_id=category_id,
            session_id=session_id,
            secure=secure,
            overwrite_passes=overwrite_passes
        )
        
        progress = WipeProgress(
            category=category_id,
            progress=0,
            completed=False
        )
        
        try:
            category = self.data_categories.get(category_id)
            if not category:
                progress.error = "Category not found"
                return progress
            
            # Simulate wipe progress
            for i in range(0, 101, 10):
                progress.progress = i
                await asyncio.sleep(0.1)  # Simulate work
                
                if i == 50 and secure:
                    logger.info("Performing secure overwrite", category_id=category_id)
                    await self._secure_overwrite(category.path, overwrite_passes)
            
            progress.completed = True
            progress.progress = 100
            
            logger.info("Category wipe completed", category_id=category_id)
            
        except Exception as e:
            logger.error("Category wipe failed", category_id=category_id, error=str(e))
            progress.error = str(e)
        
        return progress
    
    async def _secure_overwrite(self, path: str, passes: int = 3):
        """Securely overwrite files multiple times."""
        
        logger.info("Secure overwrite starting", path=path, passes=passes)
        
        # In a real implementation, this would:
        # 1. Identify all files in the path
        # 2. Overwrite each file multiple times with random data
        # 3. Sync filesystem to ensure data is written
        # 4. Remove files and directories
        
        # For demonstration, we'll simulate the operation
        for pass_num in range(passes):
            logger.debug("Overwrite pass", path=path, pass_number=pass_num + 1)
            await asyncio.sleep(0.2)  # Simulate overwrite time
        
        logger.info("Secure overwrite completed", path=path)
    
    async def schedule_auto_wipe(
        self, 
        session_id: str, 
        delay_minutes: int,
        categories: List[str] = None
    ):
        """Schedule automatic wiping for a session."""
        
        logger.info(
            "Scheduling auto-wipe",
            session_id=session_id,
            delay_minutes=delay_minutes,
            categories=categories
        )
        
        delay_seconds = delay_minutes * 60
        
        # Cancel existing auto-wipe task if present
        if session_id in self.wipe_tasks:
            self.wipe_tasks[session_id].cancel()
        
        # Create new auto-wipe task
        self.wipe_tasks[session_id] = asyncio.create_task(
            self._execute_auto_wipe(session_id, delay_seconds, categories)
        )
    
    async def _execute_auto_wipe(
        self, 
        session_id: str, 
        delay_seconds: float,
        categories: List[str] = None
    ):
        """Execute scheduled auto-wipe."""
        
        try:
            logger.info("Auto-wipe countdown started", session_id=session_id)
            await asyncio.sleep(delay_seconds)
            
            logger.info("Auto-wipe triggered", session_id=session_id)
            
            # Get categories to wipe
            if not categories:
                await self.scan_data_categories(session_id)
                categories = list(self.data_categories.keys())
            
            # Wipe each category
            for category_id in categories:
                await self.wipe_category(
                    category_id=category_id,
                    session_id=session_id,
                    secure=True,
                    overwrite_passes=3
                )
            
            logger.info("Auto-wipe completed", session_id=session_id)
            
        except asyncio.CancelledError:
            logger.info("Auto-wipe cancelled", session_id=session_id)
        except Exception as e:
            logger.error("Auto-wipe failed", session_id=session_id, error=str(e))
        finally:
            # Clean up task reference
            if session_id in self.wipe_tasks:
                del self.wipe_tasks[session_id]
    
    async def cancel_auto_wipe(self, session_id: str) -> bool:
        """Cancel scheduled auto-wipe for a session."""
        
        if session_id not in self.wipe_tasks:
            return False
        
        self.wipe_tasks[session_id].cancel()
        del self.wipe_tasks[session_id]
        
        logger.info("Auto-wipe cancelled", session_id=session_id)
        return True
    
    async def emergency_wipe_all(self):
        """Emergency wipe of all temporary and sensitive data."""
        
        logger.warning("Emergency wipe initiated")
        
        try:
            # Cancel all scheduled wipes
            for task in self.wipe_tasks.values():
                task.cancel()
            
            # Scan all data
            categories = await self.scan_data_categories("emergency")
            
            # Wipe all categories with maximum security
            for category in categories:
                await self.wipe_category(
                    category_id=category.id,
                    session_id="emergency",
                    secure=True,
                    overwrite_passes=7  # Military-grade overwriting
                )
            
            logger.warning("Emergency wipe completed")
            
        except Exception as e:
            logger.error("Emergency wipe failed", error=str(e))
            raise
    
    def get_wipe_status(self, session_id: str) -> Dict:
        """Get current wipe status for a session."""
        
        has_scheduled_wipe = session_id in self.wipe_tasks
        
        return {
            "session_id": session_id,
            "auto_wipe_scheduled": has_scheduled_wipe,
            "categories_available": len(self.data_categories),
            "last_scan": time.time()
        }
    
    async def cleanup(self):
        """Cleanup auto-wipe manager resources."""
        logger.info("Cleaning up auto-wipe manager")
        
        # Cancel all pending wipe tasks
        for task in self.wipe_tasks.values():
            task.cancel()
        
        # Wait for tasks to complete
        if self.wipe_tasks:
            await asyncio.gather(*self.wipe_tasks.values(), return_exceptions=True)
        
        self.wipe_tasks.clear()
        self.data_categories.clear()
        
        logger.info("Auto-wipe manager cleanup completed")
