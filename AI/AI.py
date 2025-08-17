from ollama import chat
from ollama import ChatResponse
import re
import logging
import time

logging.basicConfig(level=logging.INFO)

class Model:
    def __init__(self):
        self.model = "deepseek-r1:14b"

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


        logging.info(f"Context is: {self.context}\nPrompt is: {self.prompt}\nGenerating response..")
        start_time = time.time()

        response: ChatResponse = chat(model=self.model, messages=[

            {"role": "system", "content": self.context},
            {"role": "user", "content": self.prompt}
        ])
        response_text = response["message"]["content"]

        end_time = time.time()

        logging.info(f"Response generated in {end_time - start_time} seconds")

        think_text = re.findall(r'<think>(.*?)</think>', response_text, flags=re.DOTALL)
        think_text = "\n\n".join(think_text).strip()

        clean_response = re.sub(r'<think>.*?</think>', "", response_text, flags=re.DOTALL).strip()

        self.response = clean_response
        self.think = think_text
