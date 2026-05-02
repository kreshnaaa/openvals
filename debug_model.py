# debug_model.py
from openvals.models.ollama_model import OllamaModel

model = OllamaModel("llama2")

output = model.generate("Say hello")

print("MODEL OUTPUT:", output)
print("TYPE:", type(output))