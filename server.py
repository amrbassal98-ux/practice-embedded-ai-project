"""Flask application for sentiment analysis using Watson NLP."""
import logging

from flask import Flask, render_template, request
from pydantic import BaseModel, Field

from config import settings
from SentimentAnalysis.sentiment_analysis import sentiment_analyzer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

app = Flask("Sentiment Analyzer")


class SentimentRequest(BaseModel):
    text_to_analyze: str = Field(..., min_length=1, description="Text to analyze")


@app.route("/sentimentAnalyzer")
def sent_analyzer():
    """Analyze sentiment of the provided text and return label and score."""
    text_to_analyze = request.args.get("textToAnalyze", "")
    if not text_to_analyze:
        logger.warning("Empty input received")
        return "No input provided! Try again."

    try:
        validated = SentimentRequest(text_to_analyze=text_to_analyze)
    except Exception as exc:
        logger.error("Input validation failed: %s", exc)
        return "Invalid input! Try again."

    response = sentiment_analyzer(validated.text_to_analyze)
    label = response["label"]
    score = response["score"]

    if label is None:
        logger.warning("No sentiment label returned for input")
        return "Invalid input! Try again."

    sentiment = label.split("_")[1]
    return f"The given text has been identified as {sentiment} with a score of {score}"


@app.route("/")
def render_index_page():
    """Render the main application page."""
    return render_template("index.html")


if __name__ == "__main__":
    logger.info(
        "Starting server on %s:%s (env=%s)",
        settings.flask_host,
        settings.flask_port,
        settings.flask_env,
    )
    app.run(
        host=settings.flask_host,
        port=settings.flask_port,
        debug=settings.flask_env == "development",
    )
