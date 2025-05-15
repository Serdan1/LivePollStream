from abc import ABC, abstractmethod
from src.models.encuesta import Poll

class PollFactory(ABC):
    """Interfaz para las fábricas de encuestas."""
    @abstractmethod
    def create_poll(self, poll_id, question, options, duration_seconds):
        pass

class SimplePollFactory(PollFactory):
    """Fábrica para encuestas simples (un voto por usuario)."""
    def create_poll(self, poll_id, question, options, duration_seconds):
        return Poll(poll_id, question, options, duration_seconds, poll_type="simple")

class MultiplePollFactory(PollFactory):
    """Fábrica para encuestas múltiples (varios votos por usuario)."""
    def create_poll(self, poll_id, question, options, duration_seconds):
        return Poll(poll_id, question, options, duration_seconds, poll_type="multiple")

class WeightedPollFactory(PollFactory):
    """Fábrica para encuestas ponderadas (votos con peso)."""
    def create_poll(self, poll_id, question, options, duration_seconds):
        return Poll(poll_id, question, options, duration_seconds, poll_type="weighted")