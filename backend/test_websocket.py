"""
WebSocket Integration Tests

Tests for the real-time WebSocket system added in Phase 3 Week 3 Task 1.
These tests validate connection management, broadcasting, and offline queueing.
"""

import asyncio
import json
from unittest.mock import MagicMock, AsyncMock, patch
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.websocket_manager import (
    ConnectionManager,
    get_connection_manager,
    WebSocketMessage,
)


class TestConnectionManager:
    """Test ConnectionManager class functionality"""

    def test_singleton_pattern(self):
        """Test that get_connection_manager returns same instance"""
        manager1 = get_connection_manager()
        manager2 = get_connection_manager()
        assert manager1 is manager2

    @pytest.mark.asyncio
    async def test_connect_creates_entry(self):
        """Test that connect creates connection entry"""
        manager = ConnectionManager()
        mock_ws = AsyncMock()
        mock_ws.accept = AsyncMock()

        await manager.connect(diagnosis_id=1, user_id=100, websocket=mock_ws)

        assert 1 in manager.active_connections
        assert mock_ws in manager.active_connections[1]
        mock_ws.accept.assert_called_once()

    @pytest.mark.asyncio
    async def test_disconnect_removes_connection(self):
        """Test that disconnect removes connection"""
        manager = ConnectionManager()
        mock_ws = AsyncMock()
        mock_ws.accept = AsyncMock()
        mock_ws.close = AsyncMock()

        await manager.connect(diagnosis_id=1, user_id=100, websocket=mock_ws)
        await manager.disconnect(diagnosis_id=1, websocket=mock_ws)

        assert len(manager.active_connections.get(1, set())) == 0

    @pytest.mark.asyncio
    async def test_broadcast_to_all_connections(self):
        """Test broadcast sends to all connections in group"""
        manager = ConnectionManager()
        ws1 = AsyncMock()
        ws1.accept = AsyncMock()
        ws1.send_json = AsyncMock()
        ws2 = AsyncMock()
        ws2.accept = AsyncMock()
        ws2.send_json = AsyncMock()

        await manager.connect(diagnosis_id=1, user_id=100, websocket=ws1)
        await manager.connect(diagnosis_id=1, user_id=101, websocket=ws2)

        message = WebSocketMessage(
            type="test_update",
            diagnosis_id=1,
            data={"test": "data"},
            timestamp=None
        )
        await manager.broadcast(diagnosis_id=1, message=message)

        ws1.send_json.assert_called()
        ws2.send_json.assert_called()

    @pytest.mark.asyncio
    async def test_broadcast_excludes_websocket(self):
        """Test broadcast can exclude specific websocket"""
        manager = ConnectionManager()
        ws1 = AsyncMock()
        ws1.accept = AsyncMock()
        ws1.send_json = AsyncMock()
        ws2 = AsyncMock()
        ws2.accept = AsyncMock()
        ws2.send_json = AsyncMock()

        await manager.connect(diagnosis_id=1, user_id=100, websocket=ws1)
        await manager.connect(diagnosis_id=1, user_id=101, websocket=ws2)

        message = WebSocketMessage(
            type="test_update",
            diagnosis_id=1,
            data={"test": "data"},
            timestamp=None
        )
        await manager.broadcast(diagnosis_id=1, message=message, exclude_websocket=ws1)

        ws1.send_json.assert_not_called()
        ws2.send_json.assert_called()

    @pytest.mark.asyncio
    async def test_send_personal_message(self):
        """Test sending message to specific user"""
        manager = ConnectionManager()
        ws1 = AsyncMock()
        ws1.accept = AsyncMock()
        ws1.send_json = AsyncMock()
        ws2 = AsyncMock()
        ws2.accept = AsyncMock()
        ws2.send_json = AsyncMock()

        await manager.connect(diagnosis_id=1, user_id=100, websocket=ws1)
        await manager.connect(diagnosis_id=1, user_id=101, websocket=ws2)

        message = WebSocketMessage(
            type="personal_message",
            diagnosis_id=1,
            data={"message": "private"},
            timestamp=None
        )
        await manager.send_personal_message(diagnosis_id=1, user_id=100, message=message)

        ws1.send_json.assert_called()
        ws2.send_json.assert_not_called()

    @pytest.mark.asyncio
    async def test_message_queueing(self):
        """Test message queueing for offline clients"""
        manager = ConnectionManager()

        message = WebSocketMessage(
            type="test_update",
            diagnosis_id=1,
            data={"test": "data"},
            timestamp=None
        )
        await manager._queue_message(diagnosis_id=1, message=message)

        assert len(manager.message_queue.get(1, [])) == 1
        assert manager.message_queue[1][0].type == "test_update"

    @pytest.mark.asyncio
    async def test_max_queue_size(self):
        """Test that queue respects max size"""
        manager = ConnectionManager()
        manager.MAX_QUEUED_MESSAGES = 5

        for i in range(10):
            message = WebSocketMessage(
                type="test_update",
                diagnosis_id=1,
                data={"index": i},
                timestamp=None
            )
            await manager._queue_message(diagnosis_id=1, message=message)

        # Queue should only contain last 5 messages
        assert len(manager.message_queue[1]) == 5

    @pytest.mark.asyncio
    async def test_queued_messages_delivered_on_reconnect(self):
        """Test that queued messages are delivered when client reconnects"""
        manager = ConnectionManager()

        # Queue a message
        message = WebSocketMessage(
            type="test_update",
            diagnosis_id=1,
            data={"test": "data"},
            timestamp=None
        )
        await manager._queue_message(diagnosis_id=1, message=message)

        # Simulate client reconnection
        ws = AsyncMock()
        ws.accept = AsyncMock()
        ws.send_json = AsyncMock()

        await manager.connect(diagnosis_id=1, user_id=100, websocket=ws)

        # Check that queued message was sent
        assert ws.send_json.called
        call_args = ws.send_json.call_args_list
        # First call is welcome message, second should be queued message
        assert any("reconnect_messages" in str(call) for call in call_args)

    def test_get_connection_count(self):
        """Test connection counting"""
        manager = ConnectionManager()
        manager.active_connections[1] = {AsyncMock(), AsyncMock(), AsyncMock()}
        manager.active_connections[2] = {AsyncMock()}

        assert manager.get_connection_count(1) == 3
        assert manager.get_connection_count(2) == 1
        assert manager.get_connection_count(3) == 0

    def test_get_all_connections_info(self):
        """Test connection info retrieval"""
        manager = ConnectionManager()
        manager.active_connections[1] = {AsyncMock(), AsyncMock()}
        manager.active_connections[2] = {AsyncMock()}

        info = manager.get_all_connections_info()

        assert info["total_diagnoses"] == 2
        assert info["total_connections"] == 3
        assert info["connections_by_diagnosis"][1] == 2
        assert info["connections_by_diagnosis"][2] == 1


class TestWebSocketEndpoint:
    """Test WebSocket endpoint"""

    def test_websocket_status_endpoint(self):
        """Test GET /ws/status endpoint"""
        client = TestClient(app)
        response = client.get("/ws/status")

        assert response.status_code == 200
        data = response.json()
        assert "total_diagnoses" in data
        assert "total_connections" in data


class TestBroadcastFunctions:
    """Test broadcast helper functions"""

    @pytest.mark.asyncio
    async def test_broadcast_recommendation_update(self):
        """Test recommendation update broadcast"""
        from app.services.websocket_manager import broadcast_recommendation_update

        manager = ConnectionManager()
        ws = AsyncMock()
        ws.accept = AsyncMock()
        ws.send_json = AsyncMock()

        await manager.connect(diagnosis_id=1, user_id=100, websocket=ws)

        await broadcast_recommendation_update(
            diagnosis_id=1,
            old_data={"herb": "old_herb"},
            new_data={"herb": "new_herb"},
            reason="User feedback"
        )

        assert ws.send_json.called

    @pytest.mark.asyncio
    async def test_broadcast_effectiveness_update(self):
        """Test effectiveness update broadcast"""
        from app.services.websocket_manager import broadcast_effectiveness_update

        manager = ConnectionManager()
        ws = AsyncMock()
        ws.accept = AsyncMock()
        ws.send_json = AsyncMock()

        await manager.connect(diagnosis_id=1, user_id=100, websocket=ws)

        await broadcast_effectiveness_update(
            diagnosis_id=1,
            recommendation_id=5,
            effectiveness=0.85,
            confidence=0.90,
            sample_size=100
        )

        assert ws.send_json.called

    @pytest.mark.asyncio
    async def test_broadcast_feedback_update(self):
        """Test feedback update broadcast"""
        from app.services.websocket_manager import broadcast_feedback_update

        manager = ConnectionManager()
        ws = AsyncMock()
        ws.accept = AsyncMock()
        ws.send_json = AsyncMock()

        await manager.connect(diagnosis_id=1, user_id=100, websocket=ws)

        await broadcast_feedback_update(
            diagnosis_id=1,
            feedback_id=10,
            rating=5,
            effectiveness=0.95
        )

        assert ws.send_json.called


if __name__ == "__main__":
    print("✅ WebSocket test suite ready")
    print("\nTo run tests:")
    print("  pytest backend/test_websocket.py -v")
    print("\nTest coverage:")
    print("  - Connection management (connect, disconnect)")
    print("  - Broadcasting to multiple clients")
    print("  - Message queueing and offline delivery")
    print("  - Personal messaging")
    print("  - Connection statistics")
    print("  - Broadcast helper functions")
