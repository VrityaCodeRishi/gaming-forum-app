from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from database import engine, Base
from routers import games, posts
from prometheus_metrics import metrics_endpoint
from sentiment import sentiment_analyzer

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Gaming Forum API...")
    
    Base.metadata.create_all(bind=engine)
    logger.info("✓ Database tables verified")
    
    try:
        sentiment_analyzer.analyze("test")
        logger.info("Sentiment analyzer ready")
    except Exception as e:
        logger.error(f"Failed to initialize sentiment analyzer: {e}")
    
    logger.info("Gaming Forum API is ready!")
    
    yield
    
    logger.info("Shutting down Gaming Forum API...")


app = FastAPI(
    title="Gaming Forum Sentiment Analysis API",
    description="API for gaming forum with ML-powered sentiment analysis",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(games.router)
app.include_router(posts.router)

@app.get("/metrics")
def metrics():
    return metrics_endpoint()

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "gaming-forum-api",
        "version": "1.0.0"
    }

@app.get("/")
def root():
    return {
        "message": "Gaming Forum Sentiment Analysis API",
        "docs": "/docs",
        "health": "/health",
        "metrics": "/metrics"
    }
