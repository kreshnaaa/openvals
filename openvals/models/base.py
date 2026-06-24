from abc import ABC
from abc import abstractmethod

class BaseModel(ABC):

    @abstractmethod
    def generate(
        self,
        prompt
    ):
        pass

    @abstractmethod
    def provider(self):
        pass

    @abstractmethod
    def model_name(self):
        pass