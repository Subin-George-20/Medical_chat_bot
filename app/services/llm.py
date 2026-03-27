from groq import Groq
import os
from config.settings import GROQ_API_KEY


class LLMService:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def stream(self, context, query, history=[]):
        
        messages = [
            {"role": "system", "content": "You are a helpful AI assistant."
            " Use provided context only.reply to the user's question based on the provided context."
            " If you don't know the answer, say you don't know. Always use all available context to answer."
            " If the question is not related to the context, politely say that you can only answer questions related to the provided context."
            " Always provide a concise answer. If the context contains multiple pieces of information, try to synthesize them into a coherent answer."
            "if seen hi or hello in the question, greet back in the answer."
            "if asked hi or hello in the chat greet back and ask how can you help in the answer."
            "dont start every aswer with greting, only greet if the user has greeted in the question."}
            
        ]

        # ✅ Add history
        for msg in history:
            messages.append({
                "role": msg.role,
                "content": msg.content
            })

        # ✅ Add current context + question
        messages.append({
            "role": "user",
            "content": f"""
Context:
{context}

Question:
{query}
"""
        })

        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.3,
            stream=True
        )

        for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content