from transformers import pipeline

class ChatbotService:
    def __init__(self):
        print("ChatbotService: Inicializando chatbot con modelo datificate/gpt2-small-spanish")
        try:
            # Cargar el modelo de generación de texto
            self.chatbot = pipeline(
                "text-generation",
                model="datificate/gpt2-small-spanish",
                device=-1  # Usa CPU
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
        
        # Generar la respuesta con el modelo
        try:
            # Prompt optimizado para respuestas en español
            prompt = f"Responde en español de manera clara y concisa: {username}, {message}"
            # Generar respuesta
            response = self.chatbot(
                prompt,
                max_new_tokens=50,  # Limitar tokens generados
                do_sample=True,
                num_return_sequences=1,
                temperature=0.6,
                top_p=0.85
            )[0]['generated_text']
            print(f"ChatbotService: respond - Respuesta cruda del modelo: '{response}'")
            
            # Limpiar la respuesta
            response = response.strip()
            if prompt in response:
                response = response.replace(prompt, "").strip()
            if not response or len(response) < 3:
                response = "Lo siento, no pude generar una respuesta clara. Intenta de nuevo."
            response = response.replace("\n", " ").strip()
            print(f"ChatbotService: respond - Respuesta limpia: '{response}'")
            return f"{username}, {response}"
        except Exception as e:
            print(f"ChatbotService: respond - Error al generar respuesta: {e}")
            return f"{username}, lo siento, ocurrió un error al procesar tu mensaje."