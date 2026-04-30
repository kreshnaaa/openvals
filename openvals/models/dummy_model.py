
from .base import BaseModel

class DummyModel(BaseModel):
    def generate(self, prompt: str) -> str:
        return prompt[::-1]
