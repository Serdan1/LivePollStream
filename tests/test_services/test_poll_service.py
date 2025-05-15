import pytest
from datetime import datetime, timedelta
from src.models.encuesta import Poll
from src.models.voto import Vote
from src.repositories.encuesta_repository import EncuestaRepository
from src.services.poll_service import PollService
from src.patterns.factory import SimplePollFactory

@pytest.fixture
def poll_service(tmpdir):
    """Crea un servicio de encuestas con un repositorio temporal y una fábrica."""
    storage_path = str(tmpdir)
    repo = EncuestaRepository(storage_path, "json")
    factory = SimplePollFactory()
    return PollService(repo, poll_factory=factory)

def test_create_poll(poll_service):
    """Prueba crear una encuesta."""
    poll = poll_service.create_poll("Pregunta", ["Opción 1", "Opción 2"], 60, poll_type="simple")
    assert poll.question == "Pregunta"
    assert poll.options == ["Opción 1", "Opción 2"]
    assert poll.poll_type == "simple"
    assert poll.duration_seconds == 60

def test_vote(poll_service):
    """Prueba registrar un voto."""
    poll = poll_service.create_poll("Pregunta", ["Opción 1", "Opción 2"], 60, poll_type="simple")
    vote = poll_service.vote(poll.poll_id, "user1", "Opción 1")
    assert vote.poll_id == poll.poll_id
    assert vote.username == "user1"
    assert vote.option == "Opción 1"
    # Recuperar el objeto poll actualizado del repositorio
    updated_poll = poll_service.encuesta_repository.get_poll(poll.poll_id)
    assert updated_poll.votes["user1"] == "Opción 1"

def test_vote_already_voted(poll_service):
    """Prueba que un usuario no pueda votar dos veces en una encuesta simple."""
    poll = poll_service.create_poll("Pregunta", ["Opción 1", "Opción 2"], 60, poll_type="simple")
    poll_service.vote(poll.poll_id, "user1", "Opción 1")
    with pytest.raises(ValueError, match="El usuario ya ha votado"):
        poll_service.vote(poll.poll_id, "user1", "Opción 2")

def test_close_poll(poll_service):
    """Prueba cerrar una encuesta."""
    poll = poll_service.create_poll("Pregunta", ["Opción 1", "Opción 2"], 60, poll_type="simple")
    poll_service.close_poll(poll.poll_id)
    retrieved_poll = poll_service.encuesta_repository.get_poll(poll.poll_id)
    assert retrieved_poll.status == "closed"

def test_get_partial_results(poll_service):
    """Prueba obtener resultados parciales."""
    poll = poll_service.create_poll("Pregunta", ["Opción 1", "Opción 2"], 60, poll_type="simple")
    poll_service.vote(poll.poll_id, "user1", "Opción 1")
    poll_service.vote(poll.poll_id, "user2", "Opción 1")
    poll_service.vote(poll.poll_id, "user3", "Opción 2")
    results = poll_service.get_partial_results(poll.poll_id)
    assert results["counts"]["Opción 1"] == 2
    assert results["counts"]["Opción 2"] == 1
    assert results["percentages"]["Opción 1"] == 66.66666666666666
    assert results["percentages"]["Opción 2"] == 33.33333333333333