import pytest
from datetime import datetime
from src.models.voto import Vote

def test_create_vote():
    """Prueba la creación de un voto."""
    vote = Vote("poll1", "user1", "Opción 1")
    assert vote.poll_id == "poll1"
    assert vote.username == "user1"
    assert vote.option == "Opción 1"
    assert isinstance(vote.timestamp, datetime)

def test_create_vote_with_timestamp():
    """Prueba la creación de un voto con un timestamp específico."""
    timestamp = datetime(2025, 1, 1)
    vote = Vote("poll1", "user1", "Opción 1", timestamp=timestamp)
    assert vote.timestamp == timestamp

def test_vote_repr():
    """Prueba la representación del voto."""
    vote = Vote("poll1", "user1", "Opción 1")
    assert "Vote(poll_id=poll1, username=user1, option=Opción 1" in str(vote)