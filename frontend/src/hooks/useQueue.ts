import { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { queueApi } from '../services/api';
import { QueueStatus, PatientCreate, CallPatientRequest, RecallPatientRequest } from '../types';
import toast from 'react-hot-toast';
import { playAudioFromBase64 } from '../utils/audioPlayer';

export const usePolies = () => {
  return useQuery('polies', queueApi.getPolies, {
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

export const useQueueStatus = (poly: string) => {
  return useQuery(
    ['queueStatus', poly],
    () => queueApi.getQueueStatus(poly),
    {
      refetchInterval: 3000, // Refresh every 3 seconds
      enabled: !!poly,
    }
  );
};

export const useAllQueueStatus = () => {
  return useQuery('allQueueStatus', queueApi.getAllQueueStatus, {
    refetchInterval: 5000, // Refresh every 5 seconds
  });
};

export const useAddPatient = () => {
  const queryClient = useQueryClient();
  
  return useMutation(queueApi.addPatient, {
    onSuccess: (data) => {
      toast.success(data.message);
      queryClient.invalidateQueries('queueStatus');
      queryClient.invalidateQueries('allQueueStatus');
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Gagal menambahkan pasien');
    },
  });
};

export const useCallNextPatient = () => {
  const queryClient = useQueryClient();
  
  return useMutation(queueApi.callNextPatient, {
    onSuccess: async (data) => {
      toast.success(data.message);
      
      // Play audio if available
      if (data.data?.audio) {
        try {
          await playAudioFromBase64(data.data.audio);
        } catch (error) {
          console.error('Failed to play audio:', error);
          toast.error('Audio tidak dapat diputar');
        }
      }
      
      queryClient.invalidateQueries('queueStatus');
      queryClient.invalidateQueries('allQueueStatus');
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Gagal memanggil pasien');
    },
  });
};

export const useRecallPatient = () => {
  const queryClient = useQueryClient();
  
  return useMutation(queueApi.recallPatient, {
    onSuccess: async (data) => {
      toast.success(data.message);
      
      // Play audio if available
      if (data.data?.audio) {
        try {
          await playAudioFromBase64(data.data.audio);
        } catch (error) {
          console.error('Failed to play audio:', error);
          toast.error('Audio tidak dapat diputar');
        }
      }
      
      queryClient.invalidateQueries('queueStatus');
      queryClient.invalidateQueries('allQueueStatus');
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Gagal memanggil ulang pasien');
    },
  });
};

export const useClearHistory = () => {
  const queryClient = useQueryClient();
  
  return useMutation(queueApi.clearCalledHistory, {
    onSuccess: (data) => {
      toast.success(data.message);
      queryClient.invalidateQueries('queueStatus');
      queryClient.invalidateQueries('allQueueStatus');
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Gagal menghapus riwayat');
    },
  });
};

export const useDeletePatientHistory = () => {
  const queryClient = useQueryClient();
  
  return useMutation(queueApi.deletePatientHistory, {
    onSuccess: (data) => {
      toast.success(data.message);
      queryClient.invalidateQueries('queueStatus');
      queryClient.invalidateQueries('allQueueStatus');
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Gagal menghapus riwayat pasien');
    },
  });
};