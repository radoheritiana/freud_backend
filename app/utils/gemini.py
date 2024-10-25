import os
import google.generativeai as genai

class GeminiApi:
    def __init__(self):
        os.environ['GOOGLE_API_KEY'] = "AIzaSyAWBU58WEPq9JkwWFhr-q9aGniUIfrXlJE"
        genai.configure(api_key = os.environ['GOOGLE_API_KEY'])
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.chat = None
    
    def to_markdown(self, text):
        pass
    
    def generate(self, prompt):
        response = self.model.generate_content(prompt)
        return response.text
    
    def start_chat(self, initial_history):
        """
        Start a new chat session with the provided initial history.
        History should be in the format: [{"role": "user", "parts": "Hello"}, {"role": "model", "parts": "Response"}]
        """
        self.chat = self.model.start_chat(history=initial_history)

    def send_message(self, message):
        """
        Send a message to the chat and return the model's response.
        """
        if not self.chat:
            raise Exception("Chat not started. Call start_chat() first.")
        response = self.chat.send_message(message)
        return response.text