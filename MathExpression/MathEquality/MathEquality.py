from MathExpression.MathRelation import MathRelation, EnteringExpressionError
from .LinearEquality import LinearEquality
from .SquareEquality import SquareEquality



class MathEquality(LinearEquality, SquareEquality):
    """Класс уравнений."""

    def __init__(self, str_expression: str, variable: str):
        MathRelation.__init__(self, str_expression, '=', variable)


    def solving_equation(self):
        """Решение уравнения."""
        if self.type_relation == MathEquality.linear:
            self.answer.append(self.solving_linear_equation())
        elif self.type_relation == MathEquality.quadratic:
            for i in self.solving_square_equation():
                self.answer.append(i)
        elif self.type_relation == MathEquality.undefined:
            raise EnteringExpressionError("Данная задача не решается.")


    def print_answer_equation(self):
        """Вывод решения задачи."""
        print("Ответ:")
        if len(self.answer) == 0:
            print("  Решения нет.")
        else:
            for i in self.answer:
                print(f"  {self.var} = {i}")

