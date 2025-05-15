from abc import ABC, abstractmethod
from src.models.encuesta import Encuesta
import random

class DesempateStrategy(ABC):
    @abstractmethod
    def resolve(self, encuesta: Encuesta) -> str:
        pass

class RandomDesempate(DesempateStrategy):
    def resolve(self, encuesta: Encuesta) -> str:
        max_votes = max(encuesta.votos.values())
        winners = [op for op, votes in encuesta.votos.items() if votes == max_votes]
        return random.choice(winners)