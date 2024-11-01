from MathExpression.MathRelation import MathRelation
from MathExpression.MathEquality import MathEquality, LinearEquality, SquareEquality


class LinearInequality(LinearEquality):
    """Класс решения псевдо-линейных неравенств."""



# class LinearInequality2Var(LinearInequality):
#     """Класс решения псевдо-линейных неравенств с 2 переменными."""



class SquareInequality(SquareEquality):
    """Класс решения псевдо-квадратных неравенств."""



class MathInequality(MathEquality, LinearInequality, SquareInequality):
    """Класс неравенств."""

    def __init__(self, str_expression: str, sign: str, variable: str):
        MathRelation.__init__(self, str_expression, sign, variable)


    def solving_inequation(self):
        """Решение неравенства"""
        pass
