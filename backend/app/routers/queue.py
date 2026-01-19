from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List
from ..models.queue import (
    PatientCreate, Patient, QueueStatus, QueueResponse,
    CallPatientRequest, RecallPatientRequest
)
from ..services.queue_service import queue_service
from ..services.tts_service import tts_service

router = APIRouter(prefix="/api/queue", tags=["queue"])

@router.get("/polies", response_model=List[str])
async def get_polies():
    """Get list of available polies"""
    return queue_service.polies

@router.post("/add", response_model=QueueResponse)
async def add_patient(patient: PatientCreate):
    """Add patient to queue"""
    try:
        new_patient = queue_service.add_patient(patient.name, patient.poly)
        return QueueResponse(
            success=True,
            message=f"Pasien {patient.name} berhasil ditambahkan ke antrian {patient.poly}",
            data={"patient": new_patient.dict()}
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding patient: {str(e)}")

@router.post("/call", response_model=QueueResponse)
async def call_next_patient(
    request: CallPatientRequest, 
    background_tasks: BackgroundTasks
):
    """Call next patient in queue"""
    try:
        patient = queue_service.call_next_patient(request.poly)
        if not patient:
            return QueueResponse(
                success=False,
                message=f"Tidak ada antrian di {request.poly}"
            )
        
        # Generate audio for announcement
        announcement = tts_service.create_announcement(
            patient.name, patient.number, patient.poly
        )
        
        # Generate audio base64
        audio_base64 = await tts_service.generate_audio_base64(announcement)
        
        return QueueResponse(
            success=True,
            message=f"Memanggil {patient.name} - Nomor {patient.number}",
            data={
                "patient": patient.dict(),
                "audio": audio_base64,
                "announcement": announcement
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calling patient: {str(e)}")

@router.post("/recall", response_model=QueueResponse)
async def recall_patient(
    request: RecallPatientRequest,
    background_tasks: BackgroundTasks
):
    """Recall a previously called patient"""
    try:
        patient = queue_service.recall_patient(request.patient_id)
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        
        # Generate audio for announcement
        announcement = tts_service.create_announcement(
            patient.name, patient.number, patient.poly
        )
        
        # Generate audio base64
        audio_base64 = await tts_service.generate_audio_base64(announcement)
        
        return QueueResponse(
            success=True,
            message=f"Memanggil ulang {patient.name} - Nomor {patient.number}",
            data={
                "patient": patient.dict(),
                "audio": audio_base64,
                "announcement": announcement
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error recalling patient: {str(e)}")

@router.get("/status/{poly}", response_model=QueueStatus)
async def get_queue_status(poly: str):
    """Get queue status for specific poly"""
    try:
        if poly not in queue_service.polies:
            raise HTTPException(status_code=400, detail=f"Invalid poly: {poly}")
        
        return queue_service.get_queue_status(poly)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting queue status: {str(e)}")

@router.get("/status", response_model=List[QueueStatus])
async def get_all_queue_status():
    """Get queue status for all polies"""
    try:
        return [queue_service.get_queue_status(poly) for poly in queue_service.polies]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting queue status: {str(e)}")

@router.delete("/history/{poly}", response_model=QueueResponse)
async def clear_called_history(poly: str):
    """Clear all called patients history for a poly"""
    try:
        if poly not in queue_service.polies:
            raise HTTPException(status_code=400, detail=f"Invalid poly: {poly}")
        
        deleted_count = queue_service.clear_called_history(poly)
        return QueueResponse(
            success=True,
            message=f"Berhasil menghapus {deleted_count} riwayat pemanggilan",
            data={"deleted_count": deleted_count}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing history: {str(e)}")

@router.delete("/history/patient/{patient_id}", response_model=QueueResponse)
async def delete_patient_history(patient_id: int):
    """Delete specific patient from history"""
    try:
        success = queue_service.delete_patient_history(patient_id)
        if not success:
            raise HTTPException(status_code=404, detail="Patient history not found")
        
        return QueueResponse(
            success=True,
            message="Riwayat pasien berhasil dihapus"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting patient history: {str(e)}")