from typing import Any
from ..MathRelation import MathRelation, EnteringExpressionError
from .LinearEquality import LinearEquality
from .SquareEquality import SquareEquality
from sympy import Symbol



class MathEquality(LinearEquality, SquareEquality):
    """Класс уравнений."""

    def __init__(self, equality: str, variable: str):
        MathRelation.__init__(self, equality, '=', variable)
        # Корни уравнения
        self.__answer_of_equality: list[Any] = []


    def solving_equation(self) -> None:
        """Решение уравнения."""

        # Произвести замену, если необходимо
        if self.replacement:
            # old_var = self.var
            self.var = Symbol('t')
            self.left_side = self.left_side.subs(self.replacement, self.var)
            self.right_side = self.right_side.subs(self.replacement, self.var)
            self.common_divisor = self.common_divisor.subs(self.replacement, self.var)
            self.app_stage(f"Заменяем {self.replacement} на {self.var}")

        # Сокращение уравнения
        temp = [self.left_side, self.right_side]
        self.reduction()
        if (str(temp[0]) != str(self.left_side)) or (str(temp[1]) != str(self.right_side)):
            self.app_stage("Сокращаем обе стороны")

        # Деление на общий делитель
        if self.divide_by_common_divisor():
            self.__answer_of_equality.append(0)

        # Основное решение уравнения
        if self.type_relation == MathEquality.linear:
            self.__answer_of_equality.append(self.solving_linear_equation())
        elif self.type_relation == MathEquality.quadratic:
            for i in self.solving_square_equation():
                self.__answer_of_equality.append(i)
        elif self.type_relation == MathEquality.undefined:
            raise EnteringExpressionError("Данная задача не решается.")


    def print_answer_equation(self) -> None:
        """Вывод решения уравнения."""
        print("Ответ:")
        if len(self.__answer_of_equality) == 0:
            print("  Решения нет.")
        else:
            for i in self.__answer_of_equality:
                print(f"  {self.var} = {i}")

