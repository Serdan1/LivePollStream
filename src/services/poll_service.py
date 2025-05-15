from src.strategies.vote_strategy import DefaultVoteStrategy

class PollService:
    def __init__(self, encuesta_repository, poll_factory=None, vote_strategy=None, nft_service=None):
        self.encuesta_repository = encuesta_repository
        self.poll_factory = poll_factory
        self.vote_strategy = vote_strategy or DefaultVoteStrategy()
        self.nft_service = nft_service

    def create_poll(self, question, options, duration_seconds, poll_type="simple"):
        if not self.poll_factory:
            raise ValueError("Se requiere una fábrica de encuestas para crear una encuesta.")
        poll = self.poll_factory.create_poll(None, question, options, duration_seconds, poll_type)
        self.encuesta_repository.save_poll(poll)
        return poll

    def vote(self, poll_id, username, option):
        poll = self.encuesta_repository.get_poll(poll_id)
        if not poll:
            raise ValueError("Encuesta no encontrada.")
        if poll.status == "closed":
            raise ValueError("La encuesta está cerrada.")
        if self.encuesta_repository.has_user_voted(poll_id, username) and poll.poll_type == "simple":
            raise ValueError("El usuario ya ha votado.")
        if option not in poll.options:
            raise ValueError("Opción no válida.")
        vote = self.vote_strategy.vote(poll, username, option)
        self.encuesta_repository.save_vote(vote)
        if self.nft_service:
            token = self.nft_service.mint_token(username, poll_id, option)
            print(f"Token NFT generado: ID {token.token_id}")
        return vote

    def get_partial_results(self, poll_id):
        poll = self.encuesta_repository.get_poll(poll_id)
        if not poll:
            raise ValueError("Encuesta no encontrada.")
        vote_counts = {option: 0 for option in poll.options}
        total_votes = len(poll.votes)
        for option in poll.votes.values():
            if option in vote_counts:
                vote_counts[option] += 1
        percentages = {
            option: (count / total_votes * 100) if total_votes > 0 else 0
            for option, count in vote_counts.items()
        }
        return {"counts": vote_counts, "percentages": percentages}

    def close_poll(self, poll_id):
        poll = self.encuesta_repository.get_poll(poll_id)
        if not poll:
            raise ValueError("Encuesta no encontrada.")
        poll.close()
        self.encuesta_repository.save_poll(poll)