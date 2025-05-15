from abc import ABC, abstractmethod
from src.models.encuesta import Encuesta

class PollFactory(ABC):
    @abstractmethod
    def create_poll(self, pregunta: str, opciones: list, duracion_segundos: int) -> Encuesta:
        pass

class SimplePollFactory(PollFactory):
    def create_poll(self, pregunta: str, opciones: list, duracion_segundos: int) -> Encuesta:
        return Encuesta(pregunta, opciones, duracion_segundos, tipo="simple")

class MultiplePollFactory(PollFactory):
    def create_poll(self, pregunta: str, opciones: list, duracion_segundos: int) -> Encuesta:
        return Encuesta(pregunta, opciones, duracion_segundos, tipo="multiple")