"""Watson NLP sentiment analysis module."""
import json
import logging

import requests

from config import settings

logger = logging.getLogger(__name__)


def sentiment_analyzer(text_to_analyse: str) -> dict:
    """Analyze the given text and return emotion scores.

    Args:
        text_to_analyse: The text to perform sentiment analysis on.

    Returns:
        A dict with 'label' and 'score' keys.
    """
    header = {"grpc-metadata-mm-model-id": settings.watson_model_id}
    json_input = {"raw_document": {"text": text_to_analyse}}

    try:
        response = requests.post(
            settings.watson_api_url,
            json=json_input,
            headers=header,
            timeout=settings.watson_api_timeout,
        )
        response.raise_for_status()
        formatted_response = json.loads(response.text)
        label = formatted_response["documentSentiment"]["label"]
        score = formatted_response["documentSentiment"]["score"]
        logger.info("Sentiment analysis succeeded: label=%s, score=%s", label, score)
    except requests.exceptions.Timeout:
        logger.error("Watson API request timed out")
        label, score = None, None
    except requests.exceptions.HTTPError as exc:
        logger.error("Watson API HTTP error %s: %s", exc.response.status_code, exc)
        label, score = None, None
    except requests.exceptions.ConnectionError:
        logger.error("Failed to connect to Watson API")
        label, score = None, None
    except (KeyError, json.JSONDecodeError) as exc:
        logger.error("Failed to parse Watson API response: %s", exc)
        label, score = None, None

    return {"label": label, "score": score}
