import requests

class OllamaModel:
    def __init__(self, model="llama2", base_url="http://localhost:11434"):
        self.model = model
        self.base_url = base_url

    def generate(self, input_text: str) -> str:   # ✅ FIXED
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": input_text,
                "stream": False
            }
        )

        if response.status_code != 200:
            raise Exception(f"Ollama error: {response.text}")

        return response.json()["response"].strip()