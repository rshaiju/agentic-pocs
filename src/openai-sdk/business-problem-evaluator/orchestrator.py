from proposer import BusinessDomainProposer
from answerer import Answerer
from solutioner import Solutioner

problem_proposer = BusinessDomainProposer()
problem_answerer = Answerer()
solution_proposer = Solutioner()

problem = problem_proposer.propose("Please propose a business domain")
print("Business Domain:", problem)
pain_point = problem_answerer.answer(problem)
print("Pain Point:", pain_point)
solution = solution_proposer.propose_solution(f"Business Domain: {problem}, Pain Point: {pain_point}")
print("Proposed Solution:", solution)
