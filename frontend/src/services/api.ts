import axios from 'axios';
import { PatientCreate, QueueStatus, ApiResponse, CallPatientRequest, RecallPatientRequest } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8001';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const queueApi = {
  // Get available polies
  getPolies: async (): Promise<string[]> => {
    const response = await api.get('/api/queue/polies');
    return response.data;
  },

  // Add patient to queue
  addPatient: async (patient: PatientCreate): Promise<ApiResponse> => {
    const response = await api.post('/api/queue/add', patient);
    return response.data;
  },

  // Call next patient
  callNextPatient: async (request: CallPatientRequest): Promise<ApiResponse> => {
    const response = await api.post('/api/queue/call', request);
    return response.data;
  },

  // Recall patient
  recallPatient: async (request: RecallPatientRequest): Promise<ApiResponse> => {
    const response = await api.post('/api/queue/recall', request);
    return response.data;
  },

  // Get queue status for specific poly
  getQueueStatus: async (poly: string): Promise<QueueStatus> => {
    const response = await api.get(`/api/queue/status/${poly}`);
    return response.data;
  },

  // Get all queue statuses
  getAllQueueStatus: async (): Promise<QueueStatus[]> => {
    const response = await api.get('/api/queue/status');
    return response.data;
  },

  // Clear called history for poly
  clearCalledHistory: async (poly: string): Promise<ApiResponse> => {
    const response = await api.delete(`/api/queue/history/${poly}`);
    return response.data;
  },

  // Delete specific patient history
  deletePatientHistory: async (patientId: number): Promise<ApiResponse> => {
    const response = await api.delete(`/api/queue/history/patient/${patientId}`);
    return response.data;
  },
};

export default api;