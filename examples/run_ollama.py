# test_ollama.py
from openvals.models.ollama_model import OllamaModel
model = OllamaModel(model="llama2")
output = model.predict("Explain AI in one sentence")
print(output)