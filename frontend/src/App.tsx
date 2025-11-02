import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme, CssBaseline } from '@mui/material';
import Navbar from './components/Navbar';
import GamesList from './components/GamesList';
import GameDiscussion from './components/GameDiscussion';
import CreatePost from './components/CreatePost';
import './App.css';

// MUI v7 theme configuration
const theme = createTheme({
  cssVariables: true, // Enable CSS variables for better performance
  palette: {
    mode: 'dark',
    primary: {
      main: '#21808d',
      light: '#32b8c6',
      dark: '#1a6470',
    },
    secondary: {
      main: '#32b8c6',
    },
    background: {
      default: '#1f2121',
      paper: '#262828',
    },
    text: {
      primary: '#f5f5f5',
      secondary: 'rgba(245, 245, 245, 0.7)',
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h4: {
      fontWeight: 600,
    },
    h5: {
      fontWeight: 600,
    },
    h6: {
      fontWeight: 500,
    },
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          scrollbarColor: '#6b6b6b #2b2b2b',
          '&::-webkit-scrollbar, & *::-webkit-scrollbar': {
            width: 8,
          },
          '&::-webkit-scrollbar-thumb, & *::-webkit-scrollbar-thumb': {
            borderRadius: 8,
            backgroundColor: '#6b6b6b',
          },
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          borderRadius: 8,
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12,
        },
      },
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Navbar />
        <Routes>
          <Route path="/" element={<GamesList />} />
          <Route path="/game/:gameId" element={<GameDiscussion />} />
          <Route path="/game/:gameId/create-post" element={<CreatePost />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;
