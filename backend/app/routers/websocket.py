"""
WebSocket Router
Handles WebSocket connections and message routing
"""

import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import verify_token
from app.models.patient_and_health_data import Patient, DiagnosticFinding
from app.services.websocket_manager import (
    get_connection_manager,
    WebSocketMessage,
    broadcast_recommendation_update,
    broadcast_effectiveness_update,
    broadcast_feedback_update
)

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/ws",
    tags=["websocket"]
)


@router.websocket("/ws/{diagnosis_id}")
async def websocket_endpoint(
    diagnosis_id: int,
    websocket: WebSocket,
    token: str = Query(None),
    db: Session = Depends(get_db)
):
    """
    WebSocket endpoint for real-time diagnosis updates
    
    Connection format:
    ws://localhost:8000/ws/{diagnosis_id}?token=jwt_token
    
    Sends:
    - recommendation_update: When recommendations change
    - effectiveness_update: When effectiveness scores update
    - feedback_update: When new feedback received
    - analytics_update: When analytics data changes
    
    Returns:
    JSON messages with type and data fields
    """
    
    # Verify diagnosis exists
    diagnosis = db.query(DiagnosticFinding).filter(
        DiagnosticFinding.id == diagnosis_id
    ).first()
    
    if not diagnosis:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Diagnosis not found")
        logger.warning(f"❌ WebSocket connection rejected: diagnosis_id={diagnosis_id} not found")
        return
    
    # Verify token if provided
    user_id = None
    if token:
        try:
            payload = verify_token(token)
            user_id = payload.get("sub")
            
            # Verify user owns this diagnosis
            user = db.query(Patient).filter(Patient.id == user_id).first()
            if not user or diagnosis.patient_id != user_id:
                await websocket.close(
                    code=status.WS_1008_POLICY_VIOLATION,
                    reason="Access denied"
                )
                logger.warning(
                    f"❌ WebSocket connection rejected: user_id={user_id} "
                    f"doesn't own diagnosis_id={diagnosis_id}"
                )
                return
            
            logger.info(f"🔐 WebSocket authenticated: user_id={user_id}, diagnosis_id={diagnosis_id}")
        except Exception as e:
            await websocket.close(
                code=status.WS_1008_POLICY_VIOLATION,
                reason="Invalid token"
            )
            logger.warning(f"❌ WebSocket connection rejected: invalid token - {str(e)}")
            return
    else:
        # If no token provided, use diagnosis patient_id
        user_id = diagnosis.patient_id
        logger.info(f"ℹ️ WebSocket connected (no auth): user_id={user_id}, diagnosis_id={diagnosis_id}")
    
    # Get connection manager and connect
    manager = get_connection_manager()
    
    try:
        await manager.connect(diagnosis_id, user_id, websocket)
        
        # Send welcome message
        welcome_msg = WebSocketMessage(
            type="connect",
            diagnosis_id=diagnosis_id,
            data={
                "message": "Connected to real-time updates",
                "diagnosis_id": diagnosis_id,
                "user_id": user_id
            }
        )
        await websocket.send_json(welcome_msg.dict())
        logger.info(f"✅ WebSocket welcome sent: diagnosis_id={diagnosis_id}")
        
        # Keep connection open and listen for messages
        while True:
            data = await websocket.receive_text()
            
            try:
                message_data = eval(data)  # Parse JSON
                logger.debug(f"📥 WebSocket message received: {message_data}")
                
                # Handle ping/pong for keep-alive
                if message_data.get("type") == "ping":
                    pong = WebSocketMessage(
                        type="pong",
                        diagnosis_id=diagnosis_id
                    )
                    await websocket.send_json(pong.dict())
                    logger.debug("🏓 Pong sent")
                
            except Exception as e:
                logger.error(f"❌ Error processing message: {str(e)}")
                # Continue listening for more messages
                continue
    
    except WebSocketDisconnect:
        await manager.disconnect(diagnosis_id, websocket)
        logger.info(f"🔌 WebSocket disconnected: diagnosis_id={diagnosis_id}")
    
    except Exception as e:
        logger.error(f"❌ WebSocket error: {str(e)}")
        try:
            await manager.disconnect(diagnosis_id, websocket)
        except:
            pass


@router.get("/ws/status")
async def get_websocket_status():
    """
    Get WebSocket connection status and statistics
    
    Returns:
    {
        "active_connections": {
            diagnosis_id: {
                "connection_count": int,
                "queued_messages": int,
                "users": [int, ...]
            }
        },
        "total_diagoses": int,
        "total_connections": int
    }
    """
    
    manager = get_connection_manager()
    connections_info = manager.get_all_connections_info()
    
    total_connections = sum(
        info["connection_count"] for info in connections_info.values()
    )
    
    status_data = {
        "active_connections": connections_info,
        "total_diagnoses": len(connections_info),
        "total_connections": total_connections,
        "timestamp": __import__('datetime').datetime.utcnow().isoformat()
    }
    
    logger.info(f"📊 WebSocket status: {total_connections} total connections across {len(connections_info)} diagnoses")
    
    return {
        "success": True,
        "data": status_data
    }


@router.post("/ws/broadcast-recommendation-update")
async def broadcast_recommendation_update_endpoint(
    diagnosis_id: int,
    old_data: dict,
    new_data: dict,
    reason: str = "Updated",
    db: Session = Depends(get_db),
    current_user: Patient = Depends(get_current_user)
):
    """
    Broadcast recommendation update to all connected clients
    (Internal endpoint for backend services)
    
    Args:
        diagnosis_id: The diagnosis ID
        old_data: Old recommendation data
        new_data: New recommendation data
        reason: Reason for update
    """
    
    try:
        # Verify user owns this diagnosis
        diagnosis = db.query(DiagnosticFinding).filter(
            DiagnosticFinding.id == diagnosis_id
        ).first()
        
        if not diagnosis or diagnosis.patient_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Broadcast update
        await broadcast_recommendation_update(
            diagnosis_id,
            old_data,
            new_data,
            reason
        )
        
        return {
            "success": True,
            "message": "Recommendation update broadcasted",
            "diagnosis_id": diagnosis_id
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Broadcast error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ws/broadcast-effectiveness-update")
async def broadcast_effectiveness_update_endpoint(
    diagnosis_id: int,
    recommendation_id: int,
    new_effectiveness: float,
    confidence: float,
    sample_size: int,
    db: Session = Depends(get_db),
    current_user: Patient = Depends(get_current_user)
):
    """
    Broadcast effectiveness update to all connected clients
    (Internal endpoint for analytics service)
    
    Args:
        diagnosis_id: The diagnosis ID
        recommendation_id: The recommendation ID
        new_effectiveness: New effectiveness score (0-1)
        confidence: Confidence in score (0-1)
        sample_size: Number of samples used
    """
    
    try:
        # Verify user owns this diagnosis
        diagnosis = db.query(DiagnosticFinding).filter(
            DiagnosticFinding.id == diagnosis_id
        ).first()
        
        if not diagnosis or diagnosis.patient_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Broadcast update
        await broadcast_effectiveness_update(
            diagnosis_id,
            recommendation_id,
            new_effectiveness,
            confidence,
            sample_size
        )
        
        return {
            "success": True,
            "message": "Effectiveness update broadcasted",
            "recommendation_id": recommendation_id,
            "new_effectiveness": new_effectiveness
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Broadcast error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ws/broadcast-feedback-update")
async def broadcast_feedback_update_endpoint(
    diagnosis_id: int,
    feedback_id: int,
    rating: int,
    effectiveness: float,
    db: Session = Depends(get_db),
    current_user: Patient = Depends(get_current_user)
):
    """
    Broadcast feedback update to all connected clients
    (Internal endpoint for feedback service)
    
    Args:
        diagnosis_id: The diagnosis ID
        feedback_id: The feedback ID
        rating: User rating (1-5)
        effectiveness: Effectiveness score (0-1)
    """
    
    try:
        # Verify user owns this diagnosis
        diagnosis = db.query(DiagnosticFinding).filter(
            DiagnosticFinding.id == diagnosis_id
        ).first()
        
        if not diagnosis or diagnosis.patient_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Validate input
        if not (1 <= rating <= 5):
            raise HTTPException(status_code=400, detail="Rating must be 1-5")
        
        if not (0 <= effectiveness <= 1):
            raise HTTPException(status_code=400, detail="Effectiveness must be 0-1")
        
        # Broadcast update
        await broadcast_feedback_update(
            diagnosis_id,
            feedback_id,
            rating,
            effectiveness
        )
        
        return {
            "success": True,
            "message": "Feedback update broadcasted",
            "feedback_id": feedback_id,
            "rating": rating
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Broadcast error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Import at end to avoid circular imports
from app.core.security import get_current_user
