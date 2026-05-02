import requests

def sentiment_analyzer(test_to_analyse):
    url = 'https://sn-watson-sentiment-bert.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/SentimentPredict'
    header = {"grpc-metadata-mm-model-id": "sentiment_aggregated-bert-workflow_lang_multi_stock"}
    json_input = {"raw_document": {"text": test_to_analyse}}
    response = requests.post(url, json = json_input, headers = header)
    return response.text