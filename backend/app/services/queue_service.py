from typing import List, Dict, Optional
from datetime import datetime
from ..database.connection import db_manager
from ..models.queue import Patient, QueueStatus
import json

class QueueService:
    def __init__(self):
        self.polies = ["Poli Umum", "Poli Gigi", "Poli Anak", "Poli Kandungan", "Pemeriksaan BPJS"]
    
    def get_current_number(self, poly: str) -> int:
        """Get current queue number for a poly"""
        result = db_manager.execute_query(
            "SELECT current_number FROM queue_numbers WHERE poly = ?",
            (poly,)
        )
        return result[0]['current_number'] if result else 1
    
    def increment_queue_number(self, poly: str) -> int:
        """Increment and return new queue number"""
        current = self.get_current_number(poly)
        new_number = current + 1
        db_manager.execute_update(
            "UPDATE queue_numbers SET current_number = ? WHERE poly = ?",
            (new_number, poly)
        )
        return current
    
    def add_patient(self, name: str, poly: str) -> Patient:
        """Add patient to queue"""
        if poly not in self.polies:
            raise ValueError(f"Invalid poly: {poly}")
        
        number = self.increment_queue_number(poly)
        
        # Insert to database
        db_manager.execute_update(
            """INSERT INTO patients (name, poly, number, status) 
               VALUES (?, ?, ?, 'waiting')""",
            (name, poly, number)
        )
        
        return Patient(
            name=name,
            poly=poly,
            number=number,
            created_at=datetime.now()
        )
    
    def get_waiting_patients(self, poly: str) -> List[Patient]:
        """Get all waiting patients for a poly"""
        result = db_manager.execute_query(
            """SELECT * FROM patients 
               WHERE poly = ? AND status = 'waiting' 
               ORDER BY number ASC""",
            (poly,)
        )
        
        return [
            Patient(
                id=row['id'],
                name=row['name'],
                poly=row['poly'],
                number=row['number'],
                created_at=datetime.fromisoformat(row['created_at'])
            )
            for row in result
        ]
    
    def get_called_patients(self, poly: str, limit: int = 20) -> List[Patient]:
        """Get recently called patients"""
        result = db_manager.execute_query(
            """SELECT * FROM patients 
               WHERE poly = ? AND status = 'called' 
               ORDER BY called_at DESC LIMIT ?""",
            (poly, limit)
        )
        
        return [
            Patient(
                id=row['id'],
                name=row['name'],
                poly=row['poly'],
                number=row['number'],
                created_at=datetime.fromisoformat(row['created_at']),
                called_at=datetime.fromisoformat(row['called_at']) if row['called_at'] else None
            )
            for row in result
        ]
    
    def call_next_patient(self, poly: str) -> Optional[Patient]:
        """Call next patient in queue"""
        waiting_patients = self.get_waiting_patients(poly)
        if not waiting_patients:
            return None
        
        patient = waiting_patients[0]
        
        # Update patient status
        db_manager.execute_update(
            """UPDATE patients 
               SET status = 'called', called_at = CURRENT_TIMESTAMP 
               WHERE id = ?""",
            (patient.id,)
        )
        
        patient.called_at = datetime.now()
        return patient
    
    def recall_patient(self, patient_id: int) -> Optional[Patient]:
        """Recall a previously called patient"""
        # Get patient info
        result = db_manager.execute_query(
            "SELECT * FROM patients WHERE id = ?",
            (patient_id,)
        )
        
        if not result:
            return None
        
        # Update status back to waiting
        db_manager.execute_update(
            """UPDATE patients 
               SET status = 'waiting', called_at = NULL 
               WHERE id = ?""",
            (patient_id,)
        )
        
        row = result[0]
        return Patient(
            id=row['id'],
            name=row['name'],
            poly=row['poly'],
            number=row['number'],
            created_at=datetime.fromisoformat(row['created_at'])
        )
    
    def get_queue_status(self, poly: str) -> QueueStatus:
        """Get complete queue status for a poly"""
        waiting = self.get_waiting_patients(poly)
        called = self.get_called_patients(poly)
        current_number = self.get_current_number(poly)
        
        return QueueStatus(
            poly=poly,
            current_queue=waiting,
            called_patients=called,
            current_number=current_number,
            total_waiting=len(waiting)
        )
    
    def clear_called_history(self, poly: str) -> int:
        """Clear all called patients history for a poly"""
        return db_manager.execute_update(
            "DELETE FROM patients WHERE poly = ? AND status = 'called'",
            (poly,)
        )
    
    def delete_patient_history(self, patient_id: int) -> bool:
        """Delete specific patient from history"""
        affected = db_manager.execute_update(
            "DELETE FROM patients WHERE id = ? AND status = 'called'",
            (patient_id,)
        )
        return affected > 0

# Global service instance
queue_service = QueueService()