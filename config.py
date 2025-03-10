
import os

# API keys 
OPENAI_API_KEY = "enter your api key here"
SERPAPI_API_KEY = "enter your api key here"
OPENWHETHER_API_KEY = "enter your api key here"

# Load from environment variables if set
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", OPENAI_API_KEY)
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY", SERPAPI_API_KEY)
OPENWEATHER_API_KEY = os.getenv("OPENWHETHER_API_KEY", OPENWHETHER_API_KEY)
