import gradio as gr
from src.services.poll_service import PollService
from src.services.chatbot_service import ChatbotService
from src.services.nft_service import NFTService
from src.config import Config

def launch_gradio(config: Config):
    poll_service = PollService(config.encuesta_repository)
    chatbot_service = ChatbotService(config)
    nft_service = NFTService(config.nft_repository)

    def vote(poll_id, username, opcion):
        poll_service.vote(poll_id, username, opcion)
        return "Voto registrado"

    def chat(message, username):
        return chatbot_service.respond(message, username)

    def get_tokens(username):
        tokens = nft_service.get_user_tokens(username)
        return "\n".join([f"Token {t.token_id}: {t.opcion}" for t in tokens])

    with gr.Blocks() as demo:
        gr.Markdown("# LivePollStream")
        
        with gr.Tab("Encuestas"):
            poll_id = gr.Textbox(label="ID de Encuesta")
            username = gr.Textbox(label="Usuario")
            opcion = gr.Textbox(label="Opción")
            vote_btn = gr.Button("Votar")
            vote_output = gr.Textbox()
            vote_btn.click(vote, inputs=[poll_id, username, opcion], outputs=vote_output)
        
        with gr.Tab("Chatbot"):
            chatbot = gr.ChatInterface(chat, additional_inputs=[gr.Textbox(label="Usuario")])
        
        with gr.Tab("Tokens"):
            username_tokens = gr.Textbox(label="Usuario")
            tokens_btn = gr.Button("Ver Tokens")
            tokens_output = gr.Textbox()
            tokens_btn.click(get_tokens, inputs=username_tokens, outputs=tokens_output)

    demo.launch(server_port=config.port)