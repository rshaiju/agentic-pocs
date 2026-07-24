from base_agent import BaseAgent 

system_msg = "You are a helpful assistant who can evaluate the answers provided by a human to questions. " \
"Your evaluations should be clear, concise, and accurate. " 

class Evaluator(BaseAgent):
    def __init__(self, system_msg: str = system_msg):
        super().__init__(system_msg)

    def evaluate_answer(self, question: str, answer: str):
        return self.chat(f"Please evaluate the following answer to the question '{question}': {answer}")