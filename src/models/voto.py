from src.services.poll_service import PollService
from src.services.user_service import UserService
from src.services.nft_service import NFTService
from src.services.chatbot_service import ChatbotService

class CLIController:
    def __init__(self, poll_service, user_service, nft_service, chatbot_service):
        self.poll_service = poll_service
        self.user_service = user_service
        self.nft_service = nft_service
        self.chatbot_service = chatbot_service
        self.commands = {
            "crear_encuesta": self.create_poll,
            "listar_encuestas": self.list_polls,
            "cerrar_encuesta": self.close_poll,
            "ver_resultados": self.view_results,
            "mis_tokens": self.view_tokens,
            "transferir_token": self.transfer_token,
            "salir": self.exit
        }

    def start(self):
        """Inicia el bucle interactivo de la CLI."""
        print("Bienvenido al sistema de votaciones en vivo para streamers.")
        while True:
            command = input("Ingrese un comando (crear_encuesta, listar_encuestas, cerrar_encuesta, ver_resultados, mis_tokens, transferir_token, salir): ")
            if command in self.commands:
                self.commands[command]()
            else:
                print("Comando no válido.")

    def create_poll(self):
        """Crea una nueva encuesta."""
        try:
            question = input("Ingrese la pregunta: ")
            options = input("Ingrese las opciones (separadas por comas): ").split(",")
            options = [opt.strip() for opt in options]
            duration = int(input("Ingrese la duración en segundos: "))
            poll_type = input("Ingrese el tipo de encuesta (simple, multiple, weighted): ")
            poll = self.poll_service.create_poll(question, options, duration, poll_type)
            print(f"Encuesta creada con ID: {poll.poll_id}")
        except ValueError as e:
            print(f"Error: {e}")

    def list_polls(self):
        """Lista todas las encuestas."""
        polls = self.poll_service.encuesta_repository.get_all_polls()
        if not polls:
            print("No hay encuestas disponibles.")
            return
        for poll in polls:
            status = "Activa" if poll.is_active() else "Cerrada"
            print(f"ID: {poll.poll_id}, Pregunta: {poll.question}, Estado: {status}")

    def close_poll(self):
        """Cierra una encuesta existente."""
        try:
            poll_id = input("Ingrese el ID de la encuesta a cerrar: ")
            poll = self.poll_service.close_poll(poll_id)
            print(f"Encuesta {poll_id} cerrada.")
        except ValueError as e:
            print(f"Error: {e}")

    def view_results(self):
        """Muestra los resultados de una encuesta."""
        try:
            poll_id = input("Ingrese el ID de la encuesta para ver resultados: ")
            results = self.poll_service.get_final_results(poll_id)
            print(f"Resultados de la encuesta {poll_id}:")
            for option, count in results["counts"].items():
                print(f"{option}: {count} votos ({results['percentages'][option]:.1f}%)")
            if results.get("extended"):
                print("La encuesta se ha extendido debido a un empate.")
            else:
                print(f"Ganador: {results['winner']}")
        except ValueError as e:
            print(f"Error: {e}")

    def view_tokens(self):
        """Muestra los tokens NFT de un usuario."""
        username = input("Ingrese el nombre de usuario: ")
        try:
            tokens = self.nft_service.get_user_tokens(username)
            if not tokens:
                print("El usuario no tiene tokens NFT.")
                return
            for token in tokens:
                print(f"Token ID: {token.token_id}, Encuesta: {token.poll_id}, Opción: {token.option}")
        except ValueError as e:
            print(f"Error: {e}")

    def transfer_token(self):
        """Transfiere un token NFT a otro usuario."""
        try:
            token_id = input("Ingrese el ID del token a transferir: ")
            current_owner = input("Ingrese el nombre del propietario actual: ")
            new_owner = input("Ingrese el nombre del nuevo propietario: ")
            self.nft_service.transfer_token(token_id, current_owner, new_owner)
            print(f"Token {token_id} transferido de {current_owner} a {new_owner}.")
        except ValueError as e:
            print(f"Error: {e}")

    def exit(self):
        """Sale del sistema."""
        print("Saliendo del sistema...")
        exit()