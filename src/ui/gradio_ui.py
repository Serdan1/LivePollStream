import gradio as gr
from src.services.poll_service import PollService
from src.services.user_service import UserService
from src.services.nft_service import NFTService
from src.services.chatbot_service import ChatbotService

class GradioUI:
    def __init__(self, poll_service, user_service, nft_service, chatbot_service, port):
        self.poll_service = poll_service
        self.user_service = user_service
        self.nft_service = nft_service
        self.chatbot_service = chatbot_service
        self.port = port

    def launch(self):
        """Inicia la interfaz web con Gradio."""
        with gr.Blocks() as app:
            gr.Markdown("# Plataforma de Votaciones en Vivo para Streamers")

            # Sección de autenticación (simple)
            gr.Markdown("## Autenticación")
            login_username = gr.Textbox(label="Usuario")
            login_password = gr.Textbox(label="Contraseña", type="password")
            login_button = gr.Button("Iniciar Sesión")
            login_output = gr.Textbox(label="Resultado")

            # Sección de encuestas
            gr.Markdown("## Encuestas Activas")
            poll_list = gr.Dropdown(label="Seleccionar Encuesta", choices=self._get_active_polls())
            option_input = gr.Dropdown(label="Opción", choices=[])
            weight_input = gr.Number(label="Peso del Voto (solo para encuestas ponderadas)", value=1)
            vote_button = gr.Button("Votar")
            vote_output = gr.Textbox(label="Resultado del Voto")

            # Sección de chatbot
            gr.Markdown("## Chatbot")
            chatbot_input = gr.Textbox(label="Pregunta")
            chatbot_output = gr.Textbox(label="Respuesta")
            chatbot_button = gr.Button("Enviar Pregunta")

            # Sección de tokens
            gr.Markdown("## Tus Tokens NFT")
            token_list = gr.Dataframe(label="Tus Tokens", headers=["Token ID", "Encuesta", "Opción"])
            transfer_token_id = gr.Textbox(label="ID del Token a Transferir")
            transfer_new_owner = gr.Textbox(label="Nuevo Propietario")
            transfer_button = gr.Button("Transferir Token")
            transfer_output = gr.Textbox(label="Resultado de la Transferencia")

            # Funcionalidad
            def login(username, password):
                try:
                    session_token = self.user_service.login(username, password)
                    return f"Sesión iniciada con éxito. Token: {session_token}"
                except ValueError as e:
                    return f"Error: {e}"

            login_button.click(login, inputs=[login_username, login_password], outputs=login_output)

            def update_options(poll_id):
                poll = self.poll_service.encuesta_repository.get_poll(poll_id)
                return gr.update(choices=poll.options if poll else [])

            poll_list.change(update_options, inputs=poll_list, outputs=option_input)

            def vote(poll_id, username, option, weight, login_output):
                if not login_output.startswith("Sesión iniciada"):
                    return "Debes iniciar sesión primero."
                try:
                    self.user_service.verify_session(username, login_output.split("Token: ")[1])
                    self.poll_service.vote(poll_id, username, option, weight)
                    return f"Voto registrado para {username} en la encuesta {poll_id}."
                except (ValueError, IndexError) as e:
                    return f"Error: {e}"

            vote_button.click(vote, inputs=[poll_list, login_username, option_input, weight_input, login_output], outputs=vote_output)

            def chat(message, username, login_output):
                if not login_output.startswith("Sesión iniciada"):
                    return "Debes iniciar sesión primero."
                try:
                    self.user_service.verify_session(username, login_output.split("Token: ")[1])
                    return self.chatbot_service.respond(message, username)
                except (ValueError, IndexError) as e:
                    return f"Error: {e}"

            chatbot_button.click(chat, inputs=[chatbot_input, login_username, login_output], outputs=chatbot_output)

            def view_tokens(username, login_output):
                if not login_output.startswith("Sesión iniciada"):
                    return []
                try:
                    self.user_service.verify_session(username, login_output.split("Token: ")[1])
                    tokens = self.nft_service.get_user_tokens(username)
                    return [[token.token_id, token.poll_id, token.option] for token in tokens]
                except (ValueError, IndexError):
                    return []

            login_username.change(view_tokens, inputs=[login_username, login_output], outputs=token_list)

            def transfer(token_id, new_owner, username, login_output):
                if not login_output.startswith("Sesión iniciada"):
                    return "Debes iniciar sesión primero."
                try:
                    self.user_service.verify_session(username, login_output.split("Token: ")[1])
                    self.nft_service.transfer_token(token_id, username, new_owner)
                    tokens = self.nft_service.get_user_tokens(username)
                    return f"Token {token_id} transferido a {new_owner}.", [[token.token_id, token.poll_id, token.option] for token in tokens]
                except (ValueError, IndexError) as e:
                    return f"Error: {e}", []

            transfer_button.click(transfer, inputs=[transfer_token_id, transfer_new_owner, login_username, login_output], outputs=[transfer_output, token_list])

        app.launch(server_port=self.port)

    def _get_active_polls(self):
        """Devuelve una lista de IDs de encuestas activas."""
        polls = self.poll_service.encuesta_repository.get_all_polls()
        return [poll.poll_id for poll in polls if poll.is_active()]