from transformers import pipeline

class ChatbotService:
    def __init__(self):
        print("ChatbotService: Inicializando chatbot con modelo DeepESP/gpt2-spanish")
        try:
            self.chatbot = pipeline(
                "text-generation",
                model="DeepESP/gpt2-spanish",
                device=-1
            )
            print("ChatbotService: Modelo inicializado correctamente")
        except Exception as e:
            print(f"ChatbotService: Error al inicializar el modelo: {e}")
            raise

    def respond(self, message, username):
        print(f"ChatbotService: respond - Procesando mensaje de {username}: '{message}'")
        if not message or not isinstance(message, str):
            print("ChatbotService: respond - Mensaje inválido, devolviendo respuesta genérica")
            return f"{username}, por favor escribe un mensaje válido."
        
        try:
            prompt = f"Eres un asistente amigable que responde únicamente en español de manera natural y conversacional. Pregunta de {username}: {message}"
            response = self.chatbot(
                prompt,
                max_new_tokens=50,
                do_sample=True,
                num_return_sequences=1,
                temperature=0.9,
                top_p=0.95,
                pad_token_id=self.chatbot.tokenizer.eos_token_id if self.chatbot.tokenizer else None
            )[0]['generated_text']
            print(f"ChatbotService: respond - Respuesta cruda del modelo: '{response}'")
            
            response = response.strip()
            if prompt in response:
                response = response.replace(prompt, "").strip()
            if response.startswith(f"{username},"):
                response = response[len(f"{username},"):].strip()
            if not response or len(response) < 3:
                response = "Lo siento, no entendí bien. ¿Puedes repetir, por favor?"
            response = response.replace("\n", " ").strip()
            print(f"ChatbotService: respond - Respuesta limpia: '{response}'")
            return f"{username}, {response}"
        except Exception as e:
            print(f"ChatbotService: respond - Error al generar respuesta: {e}")
            return f"{username}, lo siento, ocurrió un error al procesar tu mensaje."