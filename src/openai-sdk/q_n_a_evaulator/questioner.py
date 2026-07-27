from base_agent import BaseAgent

system_msg = (
    "You are a helpful assistant who can come up with ramndom questions to test the IQ of a human."
    " You can ask questions from various domains like mathematics, science, history, literature, and general knowledge. "
    "The questions should be challenging but not impossible to answer. "
    "Avoid asking questions that are too easy or too obscure. Make sure the questions are clear and concise. "
    "Respond with only the question and do not provide any hints or answers. "
)


class Questioner(BaseAgent):
    def __init__(self, system_msg: str = system_msg):
        super().__init__(system_msg)

    def ask_question(self, question: str):
        return self.chat(question)
