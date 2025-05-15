import pytest
import os
from datetime import datetime
from src.models.encuesta import Poll
from src.models.voto import Vote
from src.repositories.encuesta_repository import EncuestaRepository

@pytest.fixture
def encuesta_repo(tmpdir):
    """Crea un repositorio temporal para las pruebas."""
    storage_path = str(tmpdir)
    return EncuestaRepository(storage_path, "json")

def test_save_and_get_poll(encuesta_repo):
    """Prueba guardar y recuperar una encuesta."""
    poll = Poll(None, "Pregunta", ["Opción 1", "Opción 2"], 60, poll_type="simple")
    poll.add_vote("user1", "Opción 1")
    encuesta_repo.save_poll(poll)
    retrieved_poll = encuesta_repo.get_poll(poll.poll_id)
    assert retrieved_poll.poll_id == poll.poll_id
    assert retrieved_poll.question == poll.question
    assert retrieved_poll.options == poll.options
    assert retrieved_poll.votes == poll.votes
    assert retrieved_poll.poll_type == poll.poll_type
    assert retrieved_poll.status == poll.status
    assert retrieved_poll.duration_seconds == poll.duration_seconds
    assert retrieved_poll.timestamp_start == poll.timestamp_start

def test_save_and_get_vote(encuesta_repo):
    """Prueba guardar y recuperar un voto."""
    vote = Vote("poll1", "user1", "Opción 1")
    encuesta_repo.save_vote(vote)
    votes = encuesta_repo.get_votes_for_poll("poll1")
    assert len(votes) == 1
    assert votes[0].poll_id == "poll1"
    assert votes[0].username == "user1"
    assert votes[0].option == "Opción 1"
    assert votes[0].timestamp == vote.timestamp

def test_has_user_voted(encuesta_repo):
    """Prueba verificar si un usuario ha votado."""
    vote = Vote("poll1", "user1", "Opción 1")
    encuesta_repo.save_vote(vote)
    assert encuesta_repo.has_user_voted("poll1", "user1")
    assert not encuesta_repo.has_user_voted("poll1", "user2")

def test_get_all_polls(encuesta_repo):
    """Prueba recuperar todas las encuestas."""
    poll1 = Poll(None, "Pregunta 1", ["Opción 1", "Opción 2"], 60, poll_type="simple")
    poll2 = Poll(None, "Pregunta 2", ["Opción A", "Opción B"], 60, poll_type="multiple")
    encuesta_repo.save_poll(poll1)
    encuesta_repo.save_poll(poll2)
    polls = encuesta_repo.get_all_polls()
    assert len(polls) == 2
    assert any(poll.poll_id == poll1.poll_id for poll in polls)
    assert any(poll.poll_id == poll2.poll_id for poll in polls)