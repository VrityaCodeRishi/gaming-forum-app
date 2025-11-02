from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
import logging

from database import get_db
from models import Game, Post
from schemas import Game as GameSchema

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/games", tags=["games"])


@router.get("", response_model=List[GameSchema])
def get_games(db: Session = Depends(get_db)):
    try:
        games_with_sentiment = (
            db.query(
                Game,
                func.avg(Post.sentiment_score).label("avg_sentiment"),
                func.count(Post.id).label("post_count")
            )
            .outerjoin(Post, Game.id == Post.game_id)
            .group_by(Game.id)
            .all()
        )
        
        result = []
        for game, avg_sentiment, post_count in games_with_sentiment:
            game_dict = {
                "id": game.id,
                "name": game.name,
                "genre": game.genre,
                "description": game.description,
                "image_url": game.image_url,
                "created_at": game.created_at,
                "avg_sentiment": float(avg_sentiment) if avg_sentiment else None,
                "post_count": post_count
            }
            result.append(game_dict)
        
        logger.info(f"Retrieved {len(result)} games")
        return result
    
    except Exception as e:
        logger.error(f"Error fetching games: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{game_id}", response_model=GameSchema)
def get_game(game_id: int, db: Session = Depends(get_db)):
    try:
        game = db.query(Game).filter(Game.id == game_id).first()
        
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
        
        sentiment_stats = (
            db.query(
                func.avg(Post.sentiment_score).label("avg_sentiment"),
                func.count(Post.id).label("post_count")
            )
            .filter(Post.game_id == game_id)
            .first()
        )
        
        game_dict = {
            "id": game.id,
            "name": game.name,
            "genre": game.genre,
            "description": game.description,
            "image_url": game.image_url,
            "created_at": game.created_at,
            "avg_sentiment": float(sentiment_stats[0]) if sentiment_stats[0] else None,
            "post_count": sentiment_stats[1]
        }
        
        return game_dict
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching game {game_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
