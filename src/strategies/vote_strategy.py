from src.models.voto import Vote
from datetime import datetime

class DefaultVoteStrategy:
    def vote(self, poll, username, option):
        """
        Registra un voto en la encuesta.

        Args:
            poll: Instancia de Poll donde se registra el voto.
            username (str): Nombre del usuario que vota.
            option (str): Opción seleccionada por el usuario.

        Returns:
            Vote: Instancia del voto registrado.
        """
        vote = Vote(poll.poll_id, username, option, timestamp=datetime.now())
        poll.add_vote(username, option)
        return vote