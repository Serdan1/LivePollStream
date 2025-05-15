import pytest
import os
from datetime import datetime
from src.models.token_nft import TokenNFT
from src.repositories.nft_repository import NFTRepository

@pytest.fixture
def nft_repo(tmpdir):
    """Crea un repositorio temporal para las pruebas."""
    storage_path = str(tmpdir)
    return NFTRepository(storage_path, "json")

def test_save_and_get_nft(nft_repo):
    """Prueba guardar y recuperar un token NFT."""
    token = TokenNFT("poll1", "Opción 1", "user1")
    nft_repo.save_nft(token)
    retrieved_token = nft_repo.get_nft(token.token_id)
    assert retrieved_token.token_id == token.token_id
    assert retrieved_token.poll_id == token.poll_id
    assert retrieved_token.option == token.option
    assert retrieved_token.owner == token.owner
    assert retrieved_token.issued_at == token.issued_at

def test_get_nfts_by_owner(nft_repo):
    """Prueba recuperar tokens NFT por propietario."""
    token1 = TokenNFT("poll1", "Opción 1", "user1")
    token2 = TokenNFT("poll2", "Opción 2", "user1")
    token3 = TokenNFT("poll3", "Opción 3", "user2")
    nft_repo.save_nft(token1)
    nft_repo.save_nft(token2)
    nft_repo.save_nft(token3)
    user1_tokens = nft_repo.get_nfts_by_owner("user1")
    assert len(user1_tokens) == 2
    assert any(token.token_id == token1.token_id for token in user1_tokens)
    assert any(token.token_id == token2.token_id for token in user1_tokens)

def test_transfer_nft(nft_repo):
    """Prueba transferir un token NFT a otro usuario."""
    token = TokenNFT("poll1", "Opción 1", "user1")
    nft_repo.save_nft(token)
    nft_repo.transfer_nft(token.token_id, "user2")
    retrieved_token = nft_repo.get_nft(token.token_id)
    assert retrieved_token.owner == "user2"

def test_get_all_nfts(nft_repo):
    """Prueba recuperar todos los tokens NFT."""
    token1 = TokenNFT("poll1", "Opción 1", "user1")
    token2 = TokenNFT("poll2", "Opción 2", "user2")
    nft_repo.save_nft(token1)
    nft_repo.save_nft(token2)
    tokens = nft_repo.get_all_nfts()
    assert len(tokens) == 2
    assert any(token.token_id == token1.token_id for token in tokens)
    assert any(token.token_id == token2.token_id for token in tokens)