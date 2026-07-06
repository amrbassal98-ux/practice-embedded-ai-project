# Watson BERT Sentiment Analysis Service with Flask Microservice Architecture

A Python Flask web application that performs real-time sentiment classification on user-submitted text using the IBM Watson NLP Sentiment BERT API. Implements a token-driven NLP classification pipeline with HTTP status code branching and three-class sentiment labeling (POSITIVE / NEGATIVE / NEUTRAL).

---

## Architecture Overview

### NLP Classification Pipeline

```
User Input (text)
  |
  v
[Flask Route Handler]         -- /sentimentAnalyzer, query param extraction
  |
  v
[SentimentAnalysis Package]   -- sentiment_analyzer() function
  |
  v
[Watson NLP REST API]         -- POST to sn-watson-sentiment-bert.labs.skills.network
  |
  v
[Status Code Router]          -- 200: parse label+score, 500/other: null fallback
  |
  v
[Label Parser]                -- Split "SENT_POSITIVE" -> "POSITIVE"
  |
  v
[Formatted String Response]   -- "identified as {sentiment} with a score of {score}"
```

### Package Decomposition

```
SentimentAnalysis/
  __init__.py                 # Package marker
  sentiment_analysis.py       # Core NLP function: Watson BERT API integration
server.py                     # Flask application, route definitions
test_sentiment_analysis.py    # Unit test suite (3 sentiment scenarios)
templates/
  index.html                  # Web interface for text input
static/
  mywebscript.js              # Client-side AJAX call handler
```

### Watson NLP Integration Details

- **Endpoint**: `https://sn-watson-sentiment-bert.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/SentimentPredict`
- **Model Header**: `grpc-metadata-mm-model-id: sentiment_aggregated-bert-workflow_lang_multi_stock`
- **Input Format**: `{ "raw_document": { "text": "..." } }`
- **Response Shape**: `{ "documentSentiment": { "label": "SENT_POSITIVE", "score": 0.95 } }`
- **Error Handling**: HTTP 200 parses label/score; HTTP 500 or other returns `{ "label": null, "score": null }`

### Status Code Branching Logic

```python
if response.status_code == 200:
    # Parse documentSentiment.label and .score
elif response.status_code == 500:
    # Return null label/score (server-side processing error)
else:
    # Return null label/score (unexpected upstream failure)
```

---

## Technical Stack Matrix

| Component | Technology | Role |
|:---|:---|:---|
| Runtime | Python 3.9+ | Application execution |
| Web Framework | Flask | HTTP routing, template rendering |
| NLP Backend | Watson NLP Sentiment BERT | Cloud-hosted sentiment classification |
| HTTP Client | requests | Watson API communication |
| Testing | unittest | Automated sentiment scenario validation |
| Frontend | HTML + JavaScript | Text input form, AJAX submission |

---

## Operational Blueprint

### Prerequisites

- Python 3.9+
- Watson NLP API access (IBM Cloud credentials or Skills Network Lab)

### Local Setup

```bash
# Clone the repository
git clone https://github.com/amrbassal98-ux/practice-embedded-ai-project.git
cd practice-embedded-ai-project

# Create isolated virtual environment (user-space, no sudo)
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install flask requests

# Run the application
python server.py
```

The server boots on `http://localhost:5000`.

### API Endpoints

| Method | Path | Parameters | Description |
|:---|:---|:---|:---|
| `GET` | `/` | - | Render main application page |
| `GET` | `/sentimentAnalyzer` | `?textToAnalyze=...` | Analyze text, return sentiment label + score |

### Running Tests

```bash
python -m unittest test_sentiment_analysis -v
```

### Example Response

```
Input: "I love working with Python"
Output: The given text has been identified as POSITIVE with a score of 0.97
```

---

## Architectural Modernization Roadmap

### 1. Structured Python Logging Matrix

Replace implicit error handling with Python's `logging` module at three severity tiers: `DEBUG` for Watson API request/response payloads, `INFO` for route invocations and sentiment results, and `ERROR` for upstream API failures (HTTP 500, timeouts). Implement `RotatingFileHandler` for persistent audit logs and `StreamHandler` for real-time console output during development.

### 2. Containerized Runtime for Cloud-Native Deployment

Build a multi-stage `Dockerfile`: Stage 1 uses `python:3.11-slim` to install dependencies into a virtualenv; Stage 2 copies only the virtualenv and application code. Add a `.dockerignore` to exclude `.git/`, `__pycache__/`, and `.venv/`. Expose port 5000 and set `CMD ["python", "server.py"]`. This produces a sub-80MB image suitable for Kubernetes pods or Cloud Foundry deployment.

### 3. Environment-Driven Configuration System

Extract the Watson API URL, model ID header, Flask host/port, and debug flag into a `.env` file loaded via `python-dotenv`. Replace hardcoded values in `sentiment_analysis.py` and `server.py` with `os.environ.get()` calls. This enables per-environment configuration (dev/staging/prod) without code modifications and prevents sensitive endpoint URLs from being committed to version control.

---

*Part of the IBM Full-Stack Cloud Developer Professional Certificate portfolio.*
