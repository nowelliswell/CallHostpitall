export interface Patient {
  id?: number;
  name: string;
  poly: string;
  number: number;
  created_at: string;
  called_at?: string;
}

export interface QueueStatus {
  poly: string;
  current_queue: Patient[];
  called_patients: Patient[];
  current_number: number;
  total_waiting: number;
}

export interface ApiResponse<T = any> {
  success: boolean;
  message: string;
  data?: T;
}

export interface PatientCreate {
  name: string;
  poly: string;
}

export interface CallPatientRequest {
  poly: string;
}

export interface RecallPatientRequest {
  patient_id: number;
  poly: string;
}