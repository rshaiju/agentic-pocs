from questioner import Questioner
from answerer import Answerer
from evaluator import Evaluator

questioner = Questioner()
question = questioner.ask_question("Please provide a challenging GK question to test the IQ of a human.")
print("Question:", question)

answerer = Answerer()
answer = answerer.provide_answer(question)
print("Answer:", answer)

evaluator = Evaluator()
evaluation = evaluator.evaluate_answer(question, answer)
print("Evaluation:", evaluation)