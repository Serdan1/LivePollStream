from src.models.encuesta import Poll
from src.models.voto import Vote
from src.repositories.encuesta_repository import EncuestaRepository
from datetime import datetime

class PollService:
    def __init__(self, encuesta_repository):
        self.encuesta_repository = encuesta_repository
        self.desempate_strategy = None  # Se asignará con el patrón Strategy más adelante

    def create_poll(self, question, options, duration_seconds, poll_type="simple"):
        """Crea una nueva encuesta y la guarda."""
        poll = Poll(None, question, options, duration_seconds, poll_type)
        self.encuesta_repository.save_poll(poll)
        return poll

    def vote(self, poll_id, username, option):
        """Registra un voto en una encuesta."""
        poll = self.encuesta_repository.get_poll(poll_id)
        if not poll:
            raise ValueError("Encuesta no encontrada.")
        if not poll.is_active():
            raise ValueError("La encuesta está cerrada.")
        if self.encuesta_repository.has_user_voted(poll_id, username):
            raise ValueError("El usuario ya ha votado.")
        poll.add_vote(username, option)
        vote = Vote(poll_id, username, option)
        self.encuesta_repository.save_vote(vote)
        self.encuesta_repository.save_poll(poll)
        return vote

    def close_poll(self, poll_id):
        """Cierra una encuesta manualmente."""
        poll = self.encuesta_repository.get_poll(poll_id)
        if not poll:
            raise ValueError("Encuesta no encontrada.")
        poll.close()
        self.encuesta_repository.save_poll(poll)
        return poll

    def _check_and_close_expired_polls(self):
        """Verifica y cierra encuestas expiradas."""
        polls = self.encuesta_repository.get_all_polls()
        for poll in polls:
            if poll.is_active():
                if (datetime.now() - poll.timestamp_start).total_seconds() >= poll.duration_seconds:
                    poll.close()
                    self.encuesta_repository.save_poll(poll)

    def get_partial_results(self, poll_id):
        """Devuelve los resultados parciales de una encuesta."""
        poll = self.encuesta_repository.get_poll(poll_id)
        if not poll:
            raise ValueError("Encuesta no encontrada.")
        self._check_and_close_expired_polls()  # Verificar si se debe cerrar
        results = poll.get_results()
        total_votes = sum(results.values())
        percentages = {
            option: (count / total_votes * 100) if total_votes > 0 else 0
            for option, count in results.items()
        }
        return {"counts": results, "percentages": percentages}

    def get_final_results(self, poll_id):
        """Devuelve los resultados finales de una encuesta cerrada."""
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
        # Determinar ganador (se usará desempate si es necesario)
        max_votes = max(results.values())
        winners = [option for option, count in results.items() if count == max_votes]
        if len(winners) > 1 and self.desempate_strategy:
            winner = self.desempate_strategy.resolve(poll)
        else:
            winner = winners[0] if winners else None
        return {"counts": results, "percentages": percentages, "winner": winner}