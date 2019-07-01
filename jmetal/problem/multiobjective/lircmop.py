from math import sin, pi

from jmetal.core.problem import FloatProblem
from jmetal.core.solution import FloatSolution
from jmetal.util.constraint_handling import set_overall_constraint_violation_degree


class LIRCMOP1(FloatProblem):
    """ Class representing problem LIR-CMOP1, defined in: An Improved epsilon-constrained Method in MOEA/D
    for CMOPs with Large Infeasible Regions. Fan, Z., Li, W., Cai, X. et al. Soft Comput (2019).
    https://doi.org/10.1007/s00500-019-03794-x
 */ """

    def __init__(self, number_of_variables: int = 2):
        super(LIRCMOP1, self).__init__()
        self.number_of_variables = number_of_variables
        self.number_of_objectives = 2
        self.number_of_constraints = 2

        self.obj_directions = [self.MINIMIZE, self.MINIMIZE]
        self.obj_labels = ['f(x)', 'f(y)']

        self.lower_bound = [0.0 for _ in range(self.number_of_variables)]
        self.upper_bound = [1.0 for _ in range(self.number_of_variables)]

        FloatSolution.lower_bound = self.lower_bound
        FloatSolution.upper_bound = self.upper_bound

    def evaluate(self, solution: FloatSolution) -> FloatSolution:
        x = solution.variables

        solution.objectives[0] = x[0] + self._g1(x)
        solution.objectives[1] = 1 - x[0]*x[0] + self._g2(x) ;

        self.__evaluate_constraints(solution)

        return solution

    def __evaluate_constraints(self, solution: FloatSolution) -> None:
        x: [float] = solution.variables
        a = 0.51
        b = 0.5
        solution.constraints[0] = (a - self._g1(x)) * (self._g1(x) - b)
        solution.constraints[1] = (a - self._g2(x)) * (self._g2(x) - b)

        set_overall_constraint_violation_degree(solution)

    def _g1(self, x: [float]) -> float:
        result = 0
        for i in range(2, self.number_of_variables, 2):
            result += pow(x[i] - sin(0.5 * pi * x[0]), 2.0)

        return result

    def _g2(self, x: [float]) -> float:
        result = 0
        for i in range(1, self.number_of_variables - 12, 2):
            result += pow(x[i] - sin(0.5 * pi * x[0]), 2.0)

        return result

    def get_name(self):
        return 'LIR-CMOP1'
