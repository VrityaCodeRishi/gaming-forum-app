from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from typing import List, Optional
import logging
import time

from database import get_db
from models import Post, User, Game
from schemas import Post as PostSchema, PostCreate
from sentiment import sentiment_analyzer
from prometheus_metrics import (
    sentiment_analysis_total,
    posts_created_total,
    game_sentiment_score,
    sentiment_analysis_duration
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/posts", tags=["posts"])


@router.get("", response_model=List[PostSchema])
def get_posts(
    game_id: Optional[int] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    try:
        query = (
            db.query(Post, User.username, Game.name.label("game_name"))
            .join(User, Post.user_id == User.id)
            .join(Game, Post.game_id == Game.id)
        )
        
        if game_id:
            query = query.filter(Post.game_id == game_id)
        
        posts = query.order_by(Post.created_at.desc()).limit(limit).all()
        
        result = []
        for post, username, game_name in posts:
            post_dict = {
                "id": post.id,
                "user_id": post.user_id,
                "game_id": post.game_id,
                "title": post.title,
                "content": post.content,
                "sentiment_score": post.sentiment_score,
                "sentiment_label": post.sentiment_label,
                "confidence": post.confidence,
                "created_at": post.created_at,
                "updated_at": post.updated_at,
                "username": username,
                "game_name": game_name
            }
            result.append(post_dict)
        
        logger.info(f"Retrieved {len(result)} posts")
        return result
    
    except Exception as e:
        logger.error(f"Error fetching posts: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=PostSchema)
def create_post(post_data: PostCreate, db: Session = Depends(get_db)):
    try:
        game = db.query(Game).filter(Game.id == post_data.game_id).first()
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
        
        user = db.query(User).filter(User.username == post_data.username).first()
        if not user:
            user = User(username=post_data.username)
            db.add(user)
            db.flush()
        
        start_time = time.time()
        sentiment_result = sentiment_analyzer.analyze(post_data.content)
        duration = time.time() - start_time
        
        sentiment_analysis_duration.observe(duration)
        sentiment_analysis_total.labels(
            game_name=game.name,
            sentiment_label=sentiment_result['label']
        ).inc()
        posts_created_total.labels(game_name=game.name).inc()
        
        new_post = Post(
            user_id=user.id,
            game_id=post_data.game_id,
            title=post_data.title,
            content=post_data.content,
            sentiment_score=sentiment_result['sentiment_score'],
            sentiment_label=sentiment_result['label'],
            confidence=sentiment_result['confidence']
        )
        
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        
        avg_sentiment = (
            db.query(func.avg(Post.sentiment_score))
            .filter(Post.game_id == post_data.game_id)
            .scalar()
        )
        game_sentiment_score.labels(game_name=game.name).set(float(avg_sentiment or 0))
        
        post_dict = {
            "id": new_post.id,
            "user_id": new_post.user_id,
            "game_id": new_post.game_id,
            "title": new_post.title,
            "content": new_post.content,
            "sentiment_score": new_post.sentiment_score,
            "sentiment_label": new_post.sentiment_label,
            "confidence": new_post.confidence,
            "created_at": new_post.created_at,
            "updated_at": new_post.updated_at,
            "username": user.username,
            "game_name": game.name
        }
        
        logger.info(f"Created post {new_post.id} with sentiment: {sentiment_result['label']}")
        return post_dict
    
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating post: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics/top-games")
def get_top_games(limit: int = Query(10, ge=1, le=50), db: Session = Depends(get_db)):
    try:
        top_games = (
            db.query(
                Game.id,
                Game.name,
                func.avg(Post.sentiment_score).label("avg_sentiment"),
                func.count(Post.id).label("post_count"),
                func.sum(case((Post.sentiment_label == 'POSITIVE', 1), else_=0)).label("positive_count"),
                func.sum(case((Post.sentiment_label == 'NEGATIVE', 1), else_=0)).label("negative_count")
            )
            .join(Post, Game.id == Post.game_id)
            .group_by(Game.id, Game.name)
            .having(func.count(Post.id) >= 1)  # At least 1 post
            .order_by(func.avg(Post.sentiment_score).desc())
            .limit(limit)
            .all()
        )
        
        result = [
            {
                "game_id": game_id,
                "game_name": name,
                "avg_sentiment": float(avg_sentiment),
                "post_count": post_count,
                "positive_count": positive_count,
                "negative_count": negative_count
            }
            for game_id, name, avg_sentiment, post_count, positive_count, negative_count in top_games
        ]
        
        return result
    
    except Exception as e:
        logger.error(f"Error fetching top games: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics/worst-games")
def get_worst_games(limit: int = Query(10, ge=1, le=50), db: Session = Depends(get_db)):
    try:
        worst_games = (
            db.query(
                Game.id,
                Game.name,
                func.avg(Post.sentiment_score).label("avg_sentiment"),
                func.count(Post.id).label("post_count"),
                func.sum(case((Post.sentiment_label == 'POSITIVE', 1), else_=0)).label("positive_count"),
                func.sum(case((Post.sentiment_label == 'NEGATIVE', 1), else_=0)).label("negative_count")
            )
            .join(Post, Game.id == Post.game_id)
            .group_by(Game.id, Game.name)
            .having(func.count(Post.id) >= 1)
            .order_by(func.avg(Post.sentiment_score).asc())
            .limit(limit)
            .all()
        )
        
        result = [
            {
                "game_id": game_id,
                "game_name": name,
                "avg_sentiment": float(avg_sentiment),
                "post_count": post_count,
                "positive_count": positive_count,
                "negative_count": negative_count
            }
            for game_id, name, avg_sentiment, post_count, positive_count, negative_count in worst_games
        ]
        
        return result
    
    except Exception as e:
        logger.error(f"Error fetching worst games: {e}")
        raise HTTPException(status_code=500, detail=str(e))
