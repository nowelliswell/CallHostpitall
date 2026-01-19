import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  TextField,
  Button,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Grid,
  Typography,
} from '@mui/material';
import {
  Add as AddIcon,
  Campaign as CallIcon,
  Refresh as RefreshIcon,
  Delete as DeleteIcon,
  Replay as ReplayIcon,
} from '@mui/icons-material';
import { usePolies, useAddPatient, useCallNextPatient, useClearHistory } from '../hooks/useQueue';

interface QueueControlProps {
  selectedPoly: string;
  onPolyChange: (poly: string) => void;
}

const QueueControl: React.FC<QueueControlProps> = ({ selectedPoly, onPolyChange }) => {
  const [patientName, setPatientName] = useState('');
  
  const { data: polies = [] } = usePolies();
  const addPatientMutation = useAddPatient();
  const callNextMutation = useCallNextPatient();
  const clearHistoryMutation = useClearHistory();

  const handleAddPatient = async () => {
    if (!patientName.trim()) {
      return;
    }

    await addPatientMutation.mutateAsync({
      name: patientName.trim(),
      poly: selectedPoly,
    });

    setPatientName('');
  };

  const handleCallNext = async () => {
    await callNextMutation.mutateAsync({ poly: selectedPoly });
  };

  const handleClearHistory = async () => {
    if (window.confirm('Apakah Anda yakin ingin menghapus semua riwayat pemanggilan?')) {
      await clearHistoryMutation.mutateAsync(selectedPoly);
    }
  };

  const handleKeyPress = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter') {
      handleAddPatient();
    }
  };

  return (
    <Card elevation={3}>
      <CardContent>
        <Typography variant="h6" gutterBottom color="primary">
          Kontrol Antrian
        </Typography>
        
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} sm={6} md={2}>
            <FormControl fullWidth>
              <InputLabel>Pilih Poli</InputLabel>
              <Select
                value={selectedPoly}
                onChange={(e) => onPolyChange(e.target.value)}
                label="Pilih Poli"
              >
                {polies.map((poly) => (
                  <MenuItem key={poly} value={poly}>
                    {poly}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <TextField
              fullWidth
              label="Nama Pasien"
              value={patientName}
              onChange={(e) => setPatientName(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={addPatientMutation.isLoading}
            />
          </Grid>

          <Grid item xs={6} sm={3} md={2}>
            <Button
              fullWidth
              variant="contained"
              color="primary"
              startIcon={<AddIcon />}
              onClick={handleAddPatient}
              disabled={!patientName.trim() || addPatientMutation.isLoading}
            >
              Tambah
            </Button>
          </Grid>

          <Grid item xs={6} sm={3} md={2}>
            <Button
              fullWidth
              variant="contained"
              color="success"
              startIcon={<CallIcon />}
              onClick={handleCallNext}
              disabled={callNextMutation.isLoading}
            >
              Panggil
            </Button>
          </Grid>

          <Grid item xs={6} sm={3} md={2}>
            <Button
              fullWidth
              variant="contained"
              color="error"
              startIcon={<DeleteIcon />}
              onClick={handleClearHistory}
              disabled={clearHistoryMutation.isLoading}
            >
              Clear
            </Button>
          </Grid>

          <Grid item xs={6} sm={3} md={1}>
            <Button
              fullWidth
              variant="outlined"
              startIcon={<RefreshIcon />}
              onClick={() => window.location.reload()}
            >
              Refresh
            </Button>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
};

export default QueueControl;