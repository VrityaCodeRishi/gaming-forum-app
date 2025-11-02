from transformers import pipeline
import logging

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    
    _instance = None
    _analyzer = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SentimentAnalyzer, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        try:
            logger.info("Loading Twitter-RoBERTa sentiment model...")
            self._analyzer = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                device=-1
            )
            logger.info("✓ Twitter-RoBERTa model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load sentiment model: {e}")
            raise
    
    def analyze(self, text: str) -> dict:
        try:
            text = text[:512]
            result = self._analyzer(text)[0]
            raw_label = result['label'].lower()
            confidence = result['score']
            if raw_label == 'positive':
                label = 'POSITIVE'
                sentiment_score = confidence
            elif raw_label == 'negative':
                label = 'NEGATIVE'
                sentiment_score = -confidence
            elif raw_label == 'neutral':
                label = 'NEUTRAL'
                sentiment_score = 0.0
            else:
                logger.warning(f"Unexpected label: {raw_label}")
                label = 'NEUTRAL'
                sentiment_score = 0.0
            
            logger.info(f"Sentiment: {label} (score: {sentiment_score:.3f}, confidence: {confidence:.3f})")
            
            return {
                'label': label,
                'confidence': confidence,
                'sentiment_score': sentiment_score
            }
        
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {e}")
            return {
                'label': 'NEUTRAL',
                'confidence': 0.0,
                'sentiment_score': 0.0
            }


sentiment_analyzer = SentimentAnalyzer()
