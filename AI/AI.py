from ollama import chat
from ollama import ChatResponse
import re

class Model:
    def __init__(self):
        self.context = None
        self.prompt = ""

        self.response = ""
        self.think = ""

    def set_context(self, context):
        self.context = context

    def set_prompt(self, prompt):
        self.prompt = prompt

    def ask_deepseek(self):
        if not self.context:
            return None

        response: ChatResponse = chat(model='deepseek-r1:14b', messages=[

            {"role": "system", "content": self.context},
            {"role": "user", "content": self.prompt}
        ])
        response_text = response["message"]["content"]

        think_text = re.findall(r'<think>(.*?)</think>', response_text, flags=re.DOTALL)
        think_text = "\n\n".join(think_text).strip()

        clean_response = re.sub(r'<think>.*?</think>', "", response_text, flags=re.DOTALL).strip()

        self.response = clean_response
        self.think = think_text
