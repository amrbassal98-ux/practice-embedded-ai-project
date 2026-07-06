from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    flask_host: str = Field(default="0.0.0.0", description="Flask server host")
    flask_port: int = Field(default=5000, description="Flask server port")
    flask_env: str = Field(default="production", description="Flask environment")

    watson_api_url: str = Field(
        default="https://sn-watson-sentiment-bert.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/SentimentPredict",
        description="Watson NLP API endpoint",
    )
    watson_model_id: str = Field(
        default="sentiment_aggregated-bert-workflow_lang_multi_stock",
        description="Watson NLP model ID",
    )
    watson_api_timeout: int = Field(default=10, description="Watson API timeout in seconds")

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
