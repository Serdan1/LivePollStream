import pytest
from datetime import datetime
from src.models.token_nft import TokenNFT

def test_create_token_nft():
    """Prueba la creación de un token NFT."""
    token = TokenNFT("poll1", "Opción 1", "user1")
    assert token.poll_id == "poll1"
    assert token.option == "Opción 1"
    assert token.owner == "user1"
    assert isinstance(token.token_id, str)
    assert isinstance(token.issued_at, datetime)

def test_create_token_nft_with_issued_at():
    """Prueba la creación de un token NFT con una fecha específica."""
    issued_at = datetime(2025, 1, 1)
    token = TokenNFT("poll1", "Opción 1", "user1", issued_at=issued_at)
    assert token.issued_at == issued_at

def test_token_nft_repr():
    """Prueba la representación del token NFT."""
    token = TokenNFT("poll1", "Opción 1", "user1")
    assert "TokenNFT(token_id=" in str(token)
    assert "poll_id=poll1, option=Opción 1, owner=user1" in str(token)