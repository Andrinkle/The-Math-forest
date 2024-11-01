from MathExpression.MathRelation import MathRelation, EnteringExpressionError, SP_TYPES_NUMS
from .LinearEquality import LinearEquality
from .SquareEquality import SquareEquality



class MathEquality(LinearEquality, SquareEquality):
    """Класс уравнений."""

    def __init__(self, str_expression: str, variable: str):
        MathRelation.__init__(self, str_expression, '=', variable)
        self.answer = []


    def solving_equation(self):
        """Решение уравнения."""
        if self.type_relation == MathEquality.linear:
            self.answer = self.solving_linear_equation()
        elif self.type_relation == MathEquality.quadratic:
            self.answer = self.solving_square_equation()
        elif self.type_relation == MathEquality.undefined:
            raise EnteringExpressionError("Данная задача не решается.")

