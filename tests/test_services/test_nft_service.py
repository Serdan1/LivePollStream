import pytest
from src.models.token_nft import TokenNFT
from src.repositories.nft_repository import NFTRepository
from src.repositories.usuario_repository import UsuarioRepository
from src.services.nft_service import NFTService
from src.services.user_service import UserService

@pytest.fixture
def nft_service(tmpdir):
    """Crea un servicio de NFTs con repositorios temporales y un servicio de usuarios."""
    storage_path = str(tmpdir)
    nft_repo = NFTRepository(storage_path, "json")
    user_repo = UsuarioRepository(storage_path, "json")
    user_service = UserService(user_repo)  # Crear un UserService
    return NFTService(nft_repo, user_repo), user_service  # Devolver ambos

def test_mint_token(nft_service):
    """Prueba generar un token NFT al votar."""
    nft_service, user_service = nft_service  # Desempaquetar el servicio
    user_service.register("user1", "password123")
    token = nft_service.mint_token("user1", "poll1", "Opción 1")
    assert token.poll_id == "poll1"
    assert token.option == "Opción 1"
    assert token.owner == "user1"
    retrieved_user = user_service.usuario_repository.get_user("user1")
    assert token.token_id in retrieved_user.tokens

def test_transfer_token(nft_service):
    """Prueba transferir un token NFT a otro usuario."""
    nft_service, user_service = nft_service  # Desempaquetar el servicio
    user_service.register("user1", "password123")
    user_service.register("user2", "password456")
    token = nft_service.mint_token("user1", "poll1", "Opción 1")
    nft_service.transfer_token(token.token_id, "user1", "user2")
    retrieved_token = nft_service.nft_repository.get_nft(token.token_id)
    assert retrieved_token.owner == "user2"
    user1 = user_service.usuario_repository.get_user("user1")
    user2 = user_service.usuario_repository.get_user("user2")
    assert token.token_id not in user1.tokens
    assert token.token_id in user2.tokens

def test_get_user_tokens(nft_service):
    """Prueba obtener los tokens NFT de un usuario."""
    nft_service, user_service = nft_service  # Desempaquetar el servicio
    user_service.register("user1", "password123")
    token1 = nft_service.mint_token("user1", "poll1", "Opción 1")
    token2 = nft_service.mint_token("user1", "poll2", "Opción 2")
    tokens = nft_service.get_user_tokens("user1")
    assert len(tokens) == 2
    assert any(token.token_id == token1.token_id for token in tokens)
    assert any(token.token_id == token2.token_id for token in tokens)