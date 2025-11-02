import React, { useEffect, useState } from 'react';
import {
  Container,
  Grid,
  Card,
  CardContent,
  CardMedia,
  Typography,
  Chip,
  Box,
  CircularProgress,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import SentimentVerySatisfiedIcon from '@mui/icons-material/SentimentVerySatisfied';
import SentimentVeryDissatisfiedIcon from '@mui/icons-material/SentimentVeryDissatisfied';
import SentimentNeutralIcon from '@mui/icons-material/SentimentNeutral';

interface Game {
  id: number;
  name: string;
  genre: string;
  description: string;
  image_url: string;
  avg_sentiment?: number;
  post_count?: number;
}

const GamesList: React.FC = () => {
  const [games, setGames] = useState<Game[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchGames();
  }, []);

  const fetchGames = async () => {
    try {
      const response = await axios.get('/api/games');
      setGames(response.data);
    } catch (error) {
      console.error('Error fetching games:', error);
    } finally {
      setLoading(false);
    }
  };

  const getSentimentIcon = (sentiment?: number) => {
    if (!sentiment) return <SentimentNeutralIcon />;
    if (sentiment > 0.3) return <SentimentVerySatisfiedIcon color="success" />;
    if (sentiment < -0.3) return <SentimentVeryDissatisfiedIcon color="error" />;
    return <SentimentNeutralIcon color="warning" />;
  };

  const getSentimentColor = (sentiment?: number) => {
    if (!sentiment) return 'default';
    if (sentiment > 0.3) return 'success';
    if (sentiment < -0.3) return 'error';
    return 'warning';
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        Gaming Forum - Explore Games
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" gutterBottom sx={{ mb: 3 }}>
        Discuss your favorite games and see community sentiment
      </Typography>

      <Grid container spacing={3}>
        {games.map((game) => (
          <Grid item xs={12} sm={6} md={4} key={game.id}>
            <Card
              sx={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                cursor: 'pointer',
                transition: 'transform 0.2s',
                '&:hover': {
                  transform: 'scale(1.02)',
                },
              }}
              onClick={() => navigate(`/game/${game.id}`)}
            >
              <CardMedia
                component="img"
                height="200"
                image={game.image_url}
                alt={game.name}
              />
              <CardContent sx={{ flexGrow: 1 }}>
                <Typography gutterBottom variant="h6" component="div">
                  {game.name}
                </Typography>
                <Chip label={game.genre} size="small" sx={{ mb: 1 }} />
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  {game.description}
                </Typography>

                <Box display="flex" justifyContent="space-between" alignItems="center">
                  <Box display="flex" alignItems="center" gap={1}>
                    {getSentimentIcon(game.avg_sentiment)}
                    <Chip
                      label={
                        game.avg_sentiment
                          ? `${(game.avg_sentiment * 100).toFixed(0)}% Positive`
                          : 'No reviews yet'
                      }
                      size="small"
                      color={getSentimentColor(game.avg_sentiment)}
                    />
                  </Box>
                  <Typography variant="caption" color="text.secondary">
                    {game.post_count || 0} posts
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
};

export default GamesList;
