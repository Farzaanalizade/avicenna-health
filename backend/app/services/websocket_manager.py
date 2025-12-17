"""
WebSocket Manager Service
Handles real-time connections, message broadcasting, and state management
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Set, Optional, List, Any
from fastapi import WebSocket
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class WebSocketMessage(BaseModel):
    """WebSocket message model"""
    type: str  # connect, disconnect, recommendation_update, effectiveness_update, etc.
    diagnosis_id: int
    timestamp: datetime = None
    data: Dict[str, Any] = None
    
    def __init__(self, **data):
        if 'timestamp' not in data or data['timestamp'] is None:
            data['timestamp'] = datetime.utcnow()
        super().__init__(**data)


class ConnectionManager:
    """
    Manages WebSocket connections per diagnosis
    Broadcasts messages to all connected clients for a diagnosis
    """
    
    def __init__(self):
        # diagnosis_id -> Set of WebSocket connections
        self.active_connections: Dict[int, Set[WebSocket]] = {}
        # diagnosis_id -> user_id (for tracking)
        self.connection_users: Dict[int, Dict[WebSocket, int]] = {}
        # Locks for thread-safe operations
        self.locks: Dict[int, asyncio.Lock] = {}
        # Message queue for offline clients
        self.message_queue: Dict[int, List[WebSocketMessage]] = {}
        # Max messages per queue
        self.max_queue_size = 100
        
        logger.info("✅ WebSocket ConnectionManager initialized")
    
    async def _get_lock(self, diagnosis_id: int) -> asyncio.Lock:
        """Get or create lock for diagnosis_id"""
        if diagnosis_id not in self.locks:
            self.locks[diagnosis_id] = asyncio.Lock()
        return self.locks[diagnosis_id]
    
    async def connect(
        self,
        diagnosis_id: int,
        user_id: int,
        websocket: WebSocket
    ) -> None:
        """
        Add new WebSocket connection
        
        Args:
            diagnosis_id: The diagnosis ID to connect to
            user_id: The user ID (for tracking)
            websocket: The WebSocket connection
        """
        await websocket.accept()
        
        lock = await self._get_lock(diagnosis_id)
        async with lock:
            if diagnosis_id not in self.active_connections:
                self.active_connections[diagnosis_id] = set()
                self.connection_users[diagnosis_id] = {}
                self.message_queue[diagnosis_id] = []
            
            self.active_connections[diagnosis_id].add(websocket)
            self.connection_users[diagnosis_id][websocket] = user_id
            
            logger.info(
                f"🔗 WebSocket connected: diagnosis_id={diagnosis_id}, "
                f"user_id={user_id}, total_connections={len(self.active_connections[diagnosis_id])}"
            )
            
            # Send queued messages to new client
            await self._send_queued_messages(diagnosis_id, websocket)
    
    async def disconnect(self, diagnosis_id: int, websocket: WebSocket) -> None:
        """
        Remove WebSocket connection
        
        Args:
            diagnosis_id: The diagnosis ID
            websocket: The WebSocket connection to remove
        """
        lock = await self._get_lock(diagnosis_id)
        async with lock:
            if diagnosis_id in self.active_connections:
                self.active_connections[diagnosis_id].discard(websocket)
                
                if websocket in self.connection_users.get(diagnosis_id, {}):
                    user_id = self.connection_users[diagnosis_id].pop(websocket)
                    logger.info(
                        f"🔌 WebSocket disconnected: diagnosis_id={diagnosis_id}, "
                        f"user_id={user_id}, remaining_connections={len(self.active_connections[diagnosis_id])}"
                    )
                
                # Clean up empty diagnosis entries
                if not self.active_connections[diagnosis_id]:
                    del self.active_connections[diagnosis_id]
                    del self.connection_users[diagnosis_id]
    
    async def broadcast(
        self,
        diagnosis_id: int,
        message: WebSocketMessage,
        exclude_websocket: Optional[WebSocket] = None
    ) -> None:
        """
        Broadcast message to all clients connected to this diagnosis
        
        Args:
            diagnosis_id: The diagnosis ID
            message: The message to broadcast
            exclude_websocket: Optional websocket to exclude from broadcast
        """
        if diagnosis_id not in self.active_connections:
            logger.debug(f"⚠️ No connections for diagnosis_id={diagnosis_id}, queuing message")
            await self._queue_message(diagnosis_id, message)
            return
        
        lock = await self._get_lock(diagnosis_id)
        async with lock:
            disconnected_clients = []
            
            for websocket in self.active_connections.get(diagnosis_id, set()).copy():
                if exclude_websocket and websocket == exclude_websocket:
                    continue
                
                try:
                    await websocket.send_json(message.dict())
                    logger.debug(f"📤 Message sent to diagnosis_id={diagnosis_id}")
                except Exception as e:
                    logger.error(f"❌ Error sending message: {str(e)}")
                    disconnected_clients.append(websocket)
            
            # Remove disconnected clients
            for websocket in disconnected_clients:
                await self.disconnect(diagnosis_id, websocket)
    
    async def _queue_message(
        self,
        diagnosis_id: int,
        message: WebSocketMessage
    ) -> None:
        """Queue message for clients that come online later"""
        if diagnosis_id not in self.message_queue:
            self.message_queue[diagnosis_id] = []
        
        queue = self.message_queue[diagnosis_id]
        
        # Keep queue size limited
        if len(queue) >= self.max_queue_size:
            queue.pop(0)  # Remove oldest
        
        queue.append(message)
        logger.debug(f"📦 Message queued for diagnosis_id={diagnosis_id}")
    
    async def _send_queued_messages(
        self,
        diagnosis_id: int,
        websocket: WebSocket
    ) -> None:
        """Send all queued messages to new client"""
        if diagnosis_id not in self.message_queue:
            return
        
        queue = self.message_queue[diagnosis_id]
        
        for message in queue.copy():
            try:
                await websocket.send_json(message.dict())
                logger.debug(f"📬 Queued message sent to diagnosis_id={diagnosis_id}")
            except Exception as e:
                logger.error(f"❌ Error sending queued message: {str(e)}")
                break
        
        # Clear queue after sending
        self.message_queue[diagnosis_id] = []
    
    async def send_personal_message(
        self,
        diagnosis_id: int,
        user_id: int,
        message: WebSocketMessage
    ) -> bool:
        """
        Send message to specific user's connection
        
        Args:
            diagnosis_id: The diagnosis ID
            user_id: The user ID
            message: The message to send
            
        Returns:
            True if sent, False otherwise
        """
        if diagnosis_id not in self.active_connections:
            await self._queue_message(diagnosis_id, message)
            return False
        
        lock = await self._get_lock(diagnosis_id)
        async with lock:
            for websocket, conn_user_id in self.connection_users.get(diagnosis_id, {}).items():
                if conn_user_id == user_id:
                    try:
                        await websocket.send_json(message.dict())
                        logger.debug(f"💬 Personal message sent to user_id={user_id}")
                        return True
                    except Exception as e:
                        logger.error(f"❌ Error sending personal message: {str(e)}")
                        return False
        
        await self._queue_message(diagnosis_id, message)
        return False
    
    def get_connection_count(self, diagnosis_id: int) -> int:
        """Get number of active connections for diagnosis"""
        return len(self.active_connections.get(diagnosis_id, set()))
    
    def get_all_connections_info(self) -> Dict[int, Dict[str, Any]]:
        """Get info about all active connections"""
        info = {}
        for diagnosis_id, connections in self.active_connections.items():
            info[diagnosis_id] = {
                "connection_count": len(connections),
                "queued_messages": len(self.message_queue.get(diagnosis_id, [])),
                "users": list(set(
                    self.connection_users[diagnosis_id].values()
                )) if diagnosis_id in self.connection_users else []
            }
        return info


# Global connection manager instance
manager: Optional[ConnectionManager] = None


def get_connection_manager() -> ConnectionManager:
    """Get or create global connection manager"""
    global manager
    if manager is None:
        manager = ConnectionManager()
    return manager


async def broadcast_recommendation_update(
    diagnosis_id: int,
    old_data: Dict[str, Any],
    new_data: Dict[str, Any],
    reason: str = "Updated"
) -> None:
    """
    Broadcast recommendation update to all clients
    
    Args:
        diagnosis_id: The diagnosis ID
        old_data: Old recommendation data
        new_data: New recommendation data
        reason: Reason for update
    """
    manager = get_connection_manager()
    
    message = WebSocketMessage(
        type="recommendation_update",
        diagnosis_id=diagnosis_id,
        data={
            "old_data": old_data,
            "new_data": new_data,
            "reason": reason,
            "changed_fields": [
                field for field in new_data.keys()
                if old_data.get(field) != new_data.get(field)
            ]
        }
    )
    
    await manager.broadcast(diagnosis_id, message)
    logger.info(f"📢 Recommendation update broadcasted for diagnosis_id={diagnosis_id}")


async def broadcast_effectiveness_update(
    diagnosis_id: int,
    recommendation_id: int,
    new_effectiveness: float,
    confidence: float,
    sample_size: int
) -> None:
    """
    Broadcast effectiveness update to all clients
    
    Args:
        diagnosis_id: The diagnosis ID
        recommendation_id: The recommendation ID
        new_effectiveness: New effectiveness score (0-1)
        confidence: Confidence in the score (0-1)
        sample_size: Number of samples used
    """
    manager = get_connection_manager()
    
    message = WebSocketMessage(
        type="effectiveness_update",
        diagnosis_id=diagnosis_id,
        data={
            "recommendation_id": recommendation_id,
            "new_effectiveness": new_effectiveness,
            "confidence": confidence,
            "sample_size": sample_size
        }
    )
    
    await manager.broadcast(diagnosis_id, message)
    logger.info(
        f"📊 Effectiveness update broadcasted: "
        f"recommendation_id={recommendation_id}, effectiveness={new_effectiveness}"
    )


async def broadcast_feedback_update(
    diagnosis_id: int,
    feedback_id: int,
    rating: int,
    effectiveness: float
) -> None:
    """
    Broadcast feedback update to all clients
    
    Args:
        diagnosis_id: The diagnosis ID
        feedback_id: The feedback ID
        rating: User rating (1-5)
        effectiveness: Effectiveness score (0-1)
    """
    manager = get_connection_manager()
    
    message = WebSocketMessage(
        type="feedback_update",
        diagnosis_id=diagnosis_id,
        data={
            "feedback_id": feedback_id,
            "rating": rating,
            "effectiveness": effectiveness
        }
    )
    
    await manager.broadcast(diagnosis_id, message)
    logger.info(f"👥 Feedback update broadcasted for diagnosis_id={diagnosis_id}")
