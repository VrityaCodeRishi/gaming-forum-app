import React, { useState } from 'react';
import {
  Container,
  Typography,
  TextField,
  Button,
  Box,
  Card,
  CardContent,
  Alert,
} from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import apiClient from '../api/client';

const CreatePost: React.FC = () => {
  const { gameId } = useParams<{ gameId: string }>();
  const navigate = useNavigate();
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [username, setUsername] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!title.trim() || !content.trim() || !username.trim()) {
      setError('All fields are required');
      return;
    }

    setLoading(true);

    try {
      await apiClient.post('/api/posts', {
        game_id: parseInt(gameId!),
        title,
        content,
        username,
      });
      navigate(`/game/${gameId}`);
    } catch (err) {
      setError('Failed to create post. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        Create New Post
      </Typography>

      <Card>
        <CardContent>
          <Box component="form" onSubmit={handleSubmit}>
            {error && (
              <Alert severity="error" sx={{ mb: 2 }}>
                {error}
              </Alert>
            )}

            <TextField
              fullWidth
              label="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              margin="normal"
              required
            />

            <TextField
              fullWidth
              label="Post Title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              margin="normal"
              required
            />

            <TextField
              fullWidth
              label="Content"
              value={content}
              onChange={(e) => setContent(e.target.value)}
              margin="normal"
              multiline
              rows={6}
              required
              helperText="Share your thoughts about the game..."
            />

            <Box display="flex" gap={2} mt={3}>
              <Button
                type="submit"
                variant="contained"
                disabled={loading}
                fullWidth
              >
                {loading ? 'Posting...' : 'Post'}
              </Button>
              <Button
                variant="outlined"
                onClick={() => navigate(`/game/${gameId}`)}
                fullWidth
              >
                Cancel
              </Button>
            </Box>
          </Box>
        </CardContent>
      </Card>
    </Container>
  );
};

export default CreatePost;
