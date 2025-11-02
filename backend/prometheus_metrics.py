from prometheus_client import Counter, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response

sentiment_analysis_total = Counter(
    'sentiment_analysis_total',
    'Total number of sentiment analyses performed',
    ['game_name', 'sentiment_label']
)

posts_created_total = Counter(
    'posts_created_total',
    'Total number of posts created',
    ['game_name']
)

game_sentiment_score = Gauge(
    'game_sentiment_score',
    'Current average sentiment score per game',
    ['game_name']
)

api_request_duration = Histogram(
    'api_request_duration_seconds',
    'API request duration in seconds',
    ['method', 'endpoint']
)

sentiment_analysis_duration = Histogram(
    'sentiment_analysis_duration_seconds',
    'Sentiment analysis duration in seconds'
)


def metrics_endpoint():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )
