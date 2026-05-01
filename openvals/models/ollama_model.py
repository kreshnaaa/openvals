
import requests
from .base import BaseModel


class OllamaModel(BaseModel):
    """
    Ollama model adapter for OpenVals.
    Connects to an Ollama server (defaults to http://localhost:11434).
    """

    def __init__(self, model_name: str, base_url: str):
        self.model_name = model_name
        self.base_url = base_url
        self.generate_url = f"{self.base_url}/api/generate"
        self._verify_model_availability()

    def _verify_model_availability(self):
        """Check if the model is actually available on the Ollama server."""
        try:
            response = requests.post(f"{self.base_url}/api/show", json={"name": self.model_name})
            if response.status_code != 200:
                raise ValueError(f"Model '{self.model_name}' is not available on the Ollama server at {self.base_url}. Please pull it first.")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Could not connect to Ollama server at {self.base_url}. Error: {e}")

    def generate(self, prompt: str) -> str:
        """Send a prompt to Ollama and return the response text."""
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False        # get full response at once (not streamed)
        }
        try:
            response = requests.post(self.generate_url, json=payload, timeout=60)
            response.raise_for_status()
            return response.json().get("response", "").strip()
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                f"Cannot connect to Ollama at {self.base_url}. "
                "Make sure Ollama is running: `ollama serve`"
            )
        except requests.exceptions.Timeout:
            raise TimeoutError(f"Ollama took too long to respond for model: {self.model_name}")
