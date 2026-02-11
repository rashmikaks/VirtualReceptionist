# from groq import Groq
# import os
# from dotenv import load_dotenv

# load_dotenv()  # Load API key from .env

# class ChatAgent:
#     def __init__(self, name, persona, knowledge=None):
#         self.name = name
#         self.persona = persona
#         self.knowledge = knowledge or ""
#         self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

#     def get_response(self, user_input):
#         prompt = f"""
# You are {self.name}, an AI-powered virtual receptionist for {self.persona['organization']}.
# Role: {self.persona['role']}
# Tone: {self.persona['tone']}

# Here’s some background knowledge (if any):
# {self.knowledge}

# User: {user_input}
# Receptionist:"""

#         try:
#             response = self.client.chat.completions.create(
#                 model="llama-3.1-8b-instant",
#                 messages=[{"role": "user", "content": prompt}],
#                 temperature=0.7,
#             )
#             return response.choices[0].message.content.strip()

#         except Exception as e:
#             return f"⚠️ Error while generating response: {e}"

from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

class ChatAgent:
    def __init__(self, name, persona, knowledge=None):
        self.name = name
        self.persona = persona
        self.knowledge = knowledge or ""
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def get_response(self, messages):
        """
        messages: list of {'role': 'user' or 'assistant', 'content': str}
        """
        # System instruction (acts like background setup)
        system_prompt = f"""
You are {self.name}, an AI-powered virtual receptionist for {self.persona['organization']}.
Role: {self.persona['role']}
Tone: {self.persona['tone']}

Background Knowledge (if any):
{self.knowledge}
"""

        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # ✅ Use a valid model
                messages=[{"role": "system", "content": system_prompt}] + messages,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()

        except Exception as e:
            return f"⚠️ Error while generating response: {e}"
