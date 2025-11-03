CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

DROP TABLE IF EXISTS comments CASCADE;
DROP TABLE IF EXISTS posts CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS games CASCADE;

CREATE TABLE games (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    genre VARCHAR(100),
    description TEXT,
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    game_id INTEGER REFERENCES games(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    sentiment_score FLOAT CHECK (sentiment_score >= -1 AND sentiment_score <= 1),
    sentiment_label VARCHAR(20),
    confidence FLOAT CHECK (confidence >= 0 AND confidence <= 1),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    post_id INTEGER REFERENCES posts(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    sentiment_score FLOAT CHECK (sentiment_score >= -1 AND sentiment_score <= 1),
    sentiment_label VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_posts_game_id ON posts(game_id);
CREATE INDEX idx_posts_user_id ON posts(user_id);
CREATE INDEX idx_posts_sentiment ON posts(sentiment_score) WHERE sentiment_score IS NOT NULL;
CREATE INDEX idx_posts_created_at ON posts(created_at DESC);
CREATE INDEX idx_comments_post_id ON comments(post_id);

INSERT INTO games (name, genre, description, image_url) VALUES
('The Last of Us Part II', 'Action-Adventure', 'Post-apocalyptic action-adventure game with stunning storytelling', 'https://placehold.co/300x400/21808d/ffffff?text=TLOU2'),
('Elden Ring', 'Action RPG', 'Open-world action role-playing game from FromSoftware', 'https://placehold.co/300x400/32b8c6/ffffff?text=Elden+Ring'),
('God of War Ragnarök', 'Action-Adventure', 'Norse mythology action game with Kratos and Atreus', 'https://placehold.co/300x400/21808d/ffffff?text=GoW'),
('Cyberpunk 2077', 'Action RPG', 'Open-world cyberpunk RPG in Night City', 'https://placehold.co/300x400/32b8c6/ffffff?text=Cyberpunk'),
('Baldurs Gate 3', 'RPG', 'Fantasy role-playing game based on D&D 5e', 'https://placehold.co/300x400/21808d/ffffff?text=BG3'),
('Starfield', 'Action RPG', 'Space exploration RPG from Bethesda', 'https://placehold.co/300x400/32b8c6/ffffff?text=Starfield'),
('Hogwarts Legacy', 'Action RPG', 'Harry Potter universe open-world RPG', 'https://placehold.co/300x400/21808d/ffffff?text=Hogwarts'),
('Spider-Man 2', 'Action-Adventure', 'Superhero action game featuring Peter Parker and Miles Morales', 'https://placehold.co/300x400/32b8c6/ffffff?text=Spider-Man'),
('Final Fantasy XVI', 'Action RPG', 'Fantasy action RPG with real-time combat', 'https://placehold.co/300x400/21808d/ffffff?text=FF16'),
('Zelda: Tears of the Kingdom', 'Action-Adventure', 'Open-world adventure game sequel to Breath of the Wild', 'https://placehold.co/300x400/32b8c6/ffffff?text=Zelda');

INSERT INTO users (username, email) VALUES
('gamer_pro', 'gamer.pro@example.com'),
('rpg_fanatic', 'rpg.fan@example.com'),
('casual_player', 'casual@example.com'),
('speedrunner', 'speedrun@example.com'),
('reviewer_alex', 'alex@example.com');

INSERT INTO posts (user_id, game_id, title, content) VALUES
(1, 2, 'Elden Ring is a masterpiece!', 'Just finished my first playthrough and I am blown away. The open world design is incredible and every boss fight feels rewarding.'),
(2, 5, 'Baldurs Gate 3 - Best RPG of the decade', 'The storytelling, character development, and choices actually matter. This is what RPGs should be!'),
(3, 4, 'Cyberpunk 2077 disappointed me', 'Even after all the patches, the game still feels empty. The story is okay but the world feels lifeless.'),
(4, 1, 'TLOU2 has the best graphics I have ever seen', 'The attention to detail is insane. Every environment feels real and lived in.'),
(5, 6, 'Starfield is boring and repetitive', 'I wanted to love this game but the procedural generation makes everything feel samey. Lost interest after 20 hours.');

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_posts_updated_at BEFORE UPDATE ON posts
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres;
