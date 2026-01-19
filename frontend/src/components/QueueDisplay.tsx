import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  CircularProgress,
  Grid,
} from '@mui/material';
import { useQueueStatus } from '../hooks/useQueue';
import { Patient } from '../types';

interface QueueDisplayProps {
  selectedPoly: string;
}

const QueueDisplay: React.FC<QueueDisplayProps> = ({ selectedPoly }) => {
  const { data: queueStatus, isLoading, error } = useQueueStatus(selectedPoly);

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" p={4}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box p={4}>
        <Typography color="error">Error loading queue data</Typography>
      </Box>
    );
  }

  if (!queueStatus) {
    return null;
  }

  const formatTime = (dateString: string) => {
    return new Date(dateString).toLocaleTimeString('id-ID', {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <Grid container spacing={3}>
      {/* Current Queue */}
      <Grid item xs={12} md={6}>
        <Card elevation={3}>
          <CardContent>
            <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
              <Typography variant="h6" color="primary">
                Antrian Saat Ini - {selectedPoly}
              </Typography>
              <Chip 
                label={`${queueStatus.total_waiting} Pasien`} 
                color="primary" 
                variant="outlined"
              />
            </Box>
            
            <TableContainer component={Paper} variant="outlined">
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell><strong>No. Antrian</strong></TableCell>
                    <TableCell><strong>Nama Pasien</strong></TableCell>
                    <TableCell><strong>Waktu Daftar</strong></TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {queueStatus.current_queue.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={3} align="center">
                        <Typography color="textSecondary">
                          Tidak ada antrian
                        </Typography>
                      </TableCell>
                    </TableRow>
                  ) : (
                    queueStatus.current_queue.map((patient: Patient) => (
                      <TableRow key={patient.id || patient.number}>
                        <TableCell>
                          <Chip 
                            label={String(patient.number).padStart(3, '0')} 
                            color="primary" 
                            size="small"
                          />
                        </TableCell>
                        <TableCell>{patient.name}</TableCell>
                        <TableCell>{formatTime(patient.created_at)}</TableCell>
                      </TableRow>
                    ))
                  )}
                </TableBody>
              </Table>
            </TableContainer>
          </CardContent>
        </Card>
      </Grid>

      {/* Called Patients History */}
      <Grid item xs={12} md={6}>
        <Card elevation={3}>
          <CardContent>
            <Typography variant="h6" color="secondary" gutterBottom>
              Riwayat Pemanggilan
            </Typography>
            
            <TableContainer component={Paper} variant="outlined" sx={{ maxHeight: 400 }}>
              <Table size="small" stickyHeader>
                <TableHead>
                  <TableRow>
                    <TableCell><strong>No. Antrian</strong></TableCell>
                    <TableCell><strong>Nama Pasien</strong></TableCell>
                    <TableCell><strong>Waktu Panggil</strong></TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {queueStatus.called_patients.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={3} align="center">
                        <Typography color="textSecondary">
                          Belum ada yang dipanggil
                        </Typography>
                      </TableCell>
                    </TableRow>
                  ) : (
                    queueStatus.called_patients.map((patient: Patient) => (
                      <TableRow key={patient.id || `called-${patient.number}`}>
                        <TableCell>
                          <Chip 
                            label={String(patient.number).padStart(3, '0')} 
                            color="secondary" 
                            size="small"
                          />
                        </TableCell>
                        <TableCell>{patient.name}</TableCell>
                        <TableCell>
                          {patient.called_at ? formatTime(patient.called_at) : '-'}
                        </TableCell>
                      </TableRow>
                    ))
                  )}
                </TableBody>
              </Table>
            </TableContainer>
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  );
};

export default QueueDisplay;