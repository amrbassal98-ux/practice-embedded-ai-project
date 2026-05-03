"""This module provides a function to analyze emotions using Watson NLP."""
import requests
import json

def sentiment_analyzer(text_to_analyse):
    """Analyzes the given text and returns emotion scores."""
    url = (
        "https://sn-watson-sentiment-bert.labs.skills.network"
        "/v1/watson.runtime.nlp.v1/NlpService/SentimentPredict"
        )
    header = {"grpc-metadata-mm-model-id": "sentiment_aggregated-bert-workflow_lang_multi_stock"}
    json_input = {"raw_document": {"text": text_to_analyse}}
    response = requests.post(url, json = json_input, headers = header, timeout=10)
    if response.status_code == 200:
        formatted_response = json.loads(response.text)
        label = formatted_response['documentSentiment']['label']
        score = formatted_response['documentSentiment']['score']
    elif response.status_code == 500:
        label = None
        score = None
    else:
        label = None
        score = None
    return ({"label": label, "score":score})
