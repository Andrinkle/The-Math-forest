from MathExpression.MathRelation import MathRelation, EnteringExpressionError
from .LinearEquality import LinearEquality
from .SquareEquality import SquareEquality
from sympy import Symbol



class MathEquality(LinearEquality, SquareEquality):
    """Класс уравнений."""

    def __init__(self, str_expression: str, variable: str):
        MathRelation.__init__(self, str_expression, '=', variable)


    def solving_equation(self):
        """Решение уравнения."""

        if self.replacement:
            old_var = self.var
            self.var = Symbol('t')
            self.left_side = self.left_side.subs(self.replacement, self.var)
            self.right_side = self.right_side.subs(self.replacement, self.var)
            self.common_divisor = self.common_divisor.subs(self.replacement, self.var)
            self.app_stage(f"Заменяем {self.replacement} на {self.var}")

        temp = [self.left_side, self.right_side]
        self.reduction()
        if str(temp[0]) != str(self.left_side) or str(temp[1]) != str(self.right_side):
            self.app_stage("Сокращаем обе стороны")

        self.divide_by_common_divisor()

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

