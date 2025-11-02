import React from 'react';
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import SportsEsportsIcon from '@mui/icons-material/SportsEsports';

const Navbar: React.FC = () => {
  const navigate = useNavigate();

  return (
    <AppBar position="sticky">
      <Toolbar>
        <SportsEsportsIcon sx={{ mr: 2 }} />
        <Typography
          variant="h6"
          component="div"
          sx={{ flexGrow: 1, cursor: 'pointer' }}
          onClick={() => navigate('/')}
        >
          Gaming Forum - Sentiment Analysis
        </Typography>
        <Button color="inherit" onClick={() => navigate('/')}>
          Games
        </Button>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
