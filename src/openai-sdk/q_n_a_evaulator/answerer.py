from base_agent import BaseAgent

system_msg = "You are a helpful assistant who can provide answers to questions. " \
"Your answers should be clear, concise, and accurate. " 

class Answerer(BaseAgent):
    def __init__(self, system_msg: str = system_msg):
        super().__init__(system_msg)

    def provide_answer(self, question: str):
        return self.chat(question)
