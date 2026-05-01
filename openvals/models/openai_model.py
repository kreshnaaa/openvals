import requests
from .base import BaseModel

class OpenAIModel(BaseModel):
    """
    OpenAI model adapter for OpenVals.
    """
    def __init__(self, api_key: str, model_name: str, base_url: str = "https://api.openai.com/v1"):
        self.api_key = api_key
        self.model_name = model_name
        self.base_url = base_url.rstrip("/")
        self.url = f"{self.base_url}/chat/completions"
        self._verify_model_availability()

    def _verify_model_availability(self):
        """Check if the model is available on the OpenAI-compatible server."""
        headers = {"Authorization": f"Bearer {self.api_key}"}
        try:
            response = requests.get(f"{self.base_url}/models/{self.model_name}", headers=headers)
            if response.status_code != 200:
                raise ValueError(f"Model '{self.model_name}' is not available at {self.base_url}. Error: {response.text}")
        except Exception as e:
            raise ConnectionError(f"Could not connect to OpenAI-compatible server at {self.base_url}. Error: {e}")

    def generate(self, prompt: str) -> str:
        """Send a prompt to OpenAI and return the response text."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }
        
        try:
            response = requests.post(self.url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error calling OpenAI API: {str(e)}"
