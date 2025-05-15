from src.models.encuesta import Poll
from src.models.voto import Vote
from src.repositories.encuesta_repository import EncuestaRepository
from src.services.nft_service import NFTService
from src.patterns.observer import PollServiceSubject
from src.patterns.strategy import DesempateStrategy
from src.patterns.factory import PollFactory
from datetime import datetime

class PollService:
    def __init__(self, encuesta_repository, poll_factory=None, nft_service=None, desempate_strategy=None):
        self.encuesta_repository = encuesta_repository
        self.poll_factory = poll_factory
        self.nft_service = nft_service
        self.desempate_strategy = desempate_strategy
        self.subject = PollServiceSubject()

    def add_observer(self, observer):
        self.subject.add_observer(observer)

    def create_poll(self, question, options, duration_seconds, poll_type="simple"):
        if not self.poll_factory:
            raise ValueError("Se requiere una fábrica de encuestas para crear una encuesta.")
        if poll_type not in ["simple", "multiple", "weighted"]:
            raise ValueError("Tipo de encuesta no válido. Use 'simple', 'multiple' o 'weighted'.")
        poll = self.poll_factory.create_poll(None, question, options, duration_seconds)
        self.encuesta_repository.save_poll(poll)
        return poll

    def vote(self, poll_id, username, option, weight=1):
        """Registra un voto, soportando un peso para encuestas ponderadas."""
        poll = self.encuesta_repository.get_poll(poll_id)
        if not poll:
            raise ValueError("Encuesta no encontrada.")
        if not poll.is_active():
            raise ValueError("La encuesta está cerrada.")
        if poll.poll_type != "multiple" and self.encuesta_repository.has_user_voted(poll_id, username):
            raise ValueError("El usuario ya ha votado.")
        poll.add_vote(username, option, weight)
        vote = Vote(poll_id, username, option)
        self.encuesta_repository.save_vote(vote)
        self.encuesta_repository.save_poll(poll)
        if self.nft_service:
            token = self.nft_service.mint_token(username, poll_id, option)
        return vote

    def close_poll(self, poll_id):
        poll = self.encuesta_repository.get_poll(poll_id)
        if not poll:
            raise ValueError("Encuesta no encontrada.")
        poll.close()
        self.encuesta_repository.save_poll(poll)
        self.subject.notify_observers(poll)
        return poll

    def _check_and_close_expired_polls(self):
        polls = self.encuesta_repository.get_all_polls()
        for poll in polls:
            if poll.is_active():
                if (datetime.now() - poll.timestamp_start).total_seconds() >= poll.duration_seconds:
                    poll.close()
                    self.encuesta_repository.save_poll(poll)
                    self.subject.notify_observers(poll)

    def get_partial_results(self, poll_id):
        poll = self.encuesta_repository.get_poll(poll_id)
        if not poll:
            raise ValueError("Encuesta no encontrada.")
        self._check_and_close_expired_polls()
        results = poll.get_results()
        total_votes = sum(results.values())
        percentages = {
            option: (count / total_votes * 100) if total_votes > 0 else 0
            for option, count in results.items()
        }
        return {"counts": results, "percentages": percentages}

    def get_final_results(self, poll_id):
        poll = self.encuesta_repository.get_poll(poll_id)
        if not poll:
            raise ValueError("Encuesta no encontrada.")
        if poll.is_active():
            raise ValueError("La encuesta aún está activa.")
        results = poll.get_results()
        total_votes = sum(results.values())
        percentages = {
            option: (count / total_votes * 100) if total_votes > 0 else 0
            for option, count in results.items()
        }
        max_votes = max(results.values())
        winners = [option for option, count in results.items() if count == max_votes]
        if len(winners) > 1 and self.desempate_strategy:
            winner = self.desempate_strategy.resolve(poll)
            if winner is None:
                self.encuesta_repository.save_poll(poll)
                return {"counts": results, "percentages": percentages, "winner": None, "extended": True}
        else:
            winner = winners[0] if winners else None
        return {"counts": results, "percentages": percentages, "winner": winner, "extended": False}