import React, { useEffect, useState } from 'react';
import {
  Container,
  Typography,
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  Avatar,
  CircularProgress,
  Divider,
} from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import AddIcon from '@mui/icons-material/Add';
import PersonIcon from '@mui/icons-material/Person';

interface Post {
  id: number;
  title: string;
  content: string;
  username: string;
  sentiment_label?: string;
  sentiment_score?: number;
  created_at: string;
}

interface Game {
  id: number;
  name: string;
  genre: string;
  description: string;
}

const GameDiscussion: React.FC = () => {
  const { gameId } = useParams<{ gameId: string }>();
  const [game, setGame] = useState<Game | null>(null);
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchGameDetails();
    fetchPosts();
  }, [gameId]);

  const fetchGameDetails = async () => {
    try {
      const response = await axios.get(`/api/games/${gameId}`);
      setGame(response.data);
    } catch (error) {
      console.error('Error fetching game details:', error);
    }
  };

  const fetchPosts = async () => {
    try {
      const response = await axios.get(`/api/posts?game_id=${gameId}`);
      setPosts(response.data);
    } catch (error) {
      console.error('Error fetching posts:', error);
    } finally {
      setLoading(false);
    }
  };

  const getSentimentColor = (label?: string) => {
    if (label === 'POSITIVE') return 'success';
    if (label === 'NEGATIVE') return 'error';
    return 'default';
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
      {game && (
        <Box mb={4}>
          <Typography variant="h4" gutterBottom>
            {game.name}
          </Typography>
          <Chip label={game.genre} sx={{ mr: 1 }} />
          <Typography variant="body1" color="text.secondary" sx={{ mt: 2 }}>
            {game.description}
          </Typography>
        </Box>
      )}

      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h5">Discussions ({posts.length})</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => navigate(`/game/${gameId}/create-post`)}
        >
          New Post
        </Button>
      </Box>

      {posts.length === 0 ? (
        <Card>
          <CardContent>
            <Typography variant="body1" color="text.secondary" textAlign="center">
              No discussions yet. Be the first to share your thoughts!
            </Typography>
          </CardContent>
        </Card>
      ) : (
        posts.map((post) => (
          <Card key={post.id} sx={{ mb: 2 }}>
            <CardContent>
              <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={2}>
                <Box display="flex" alignItems="center" gap={1}>
                  <Avatar sx={{ width: 32, height: 32 }}>
                    <PersonIcon />
                  </Avatar>
                  <Typography variant="subtitle2">{post.username}</Typography>
                  <Typography variant="caption" color="text.secondary">
                    • {new Date(post.created_at).toLocaleDateString()}
                  </Typography>
                </Box>
                {post.sentiment_label && (
                  <Chip
                    label={post.sentiment_label}
                    size="small"
                    color={getSentimentColor(post.sentiment_label)}
                  />
                )}
              </Box>

              <Typography variant="h6" gutterBottom>
                {post.title}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                {post.content}
              </Typography>
            </CardContent>
          </Card>
        ))
      )}
    </Container>
  );
};

export default GameDiscussion;
