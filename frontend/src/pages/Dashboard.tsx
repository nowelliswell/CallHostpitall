import React, { useState } from 'react';
import {
  Container,
  Typography,
  Box,
  AppBar,
  Toolbar,
  Paper,
} from '@mui/material';
import { LocalHospital as HospitalIcon } from '@mui/icons-material';
import QueueControl from '../components/QueueControl';
import QueueDisplay from '../components/QueueDisplay';
import { usePolies } from '../hooks/useQueue';

const Dashboard: React.FC = () => {
  const { data: polies = [] } = usePolies();
  const [selectedPoly, setSelectedPoly] = useState(polies[0] || 'Poli Umum');

  // Update selected poly when polies are loaded
  React.useEffect(() => {
    if (polies.length > 0 && !selectedPoly) {
      setSelectedPoly(polies[0]);
    }
  }, [polies, selectedPoly]);

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static" elevation={0}>
        <Toolbar>
          <HospitalIcon sx={{ mr: 2 }} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Sistem Antrian Rumah Sakit
          </Typography>
          <Typography variant="body2">
            {new Date().toLocaleDateString('id-ID', {
              weekday: 'long',
              year: 'numeric',
              month: 'long',
              day: 'numeric',
            })}
          </Typography>
        </Toolbar>
      </AppBar>

      <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
        <Box mb={3}>
          <QueueControl
            selectedPoly={selectedPoly}
            onPolyChange={setSelectedPoly}
          />
        </Box>

        <QueueDisplay selectedPoly={selectedPoly} />
      </Container>
    </Box>
  );
};

export default Dashboard;