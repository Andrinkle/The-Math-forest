import sympy
import sympy.core.numbers


SP_TYPES_NUMS = [sympy.core.numbers.Integer,
                 sympy.core.numbers.One,
                 sympy.core.numbers.NegativeOne,
                 sympy.core.numbers.Rational,
                 sympy.core.numbers.Float,
                 sympy.core.numbers.Half,
                #  sympy.core.numbers.Exp1,
                 sympy.core.numbers.Pi,
                 sympy.exp]


class Side:
    left = 'l'
    right = 'r'


class EnteringExpressionError(Exception):
    pass



class MathRelation:
    """Класс математических отношений."""

    def __init__(self, expression: str, sign: str, variable_1: str, variable_2: str=''):
        self.var = sympy.Symbol(variable_1)
        if variable_2:
            self.var2 = sympy.Symbol(variable_2)
        exp_list = expression.split(sign)
        self.left_side = sympy.sympify(exp_list[0], evaluate=False)
        self.right_side = sympy.sympify(exp_list[1], evaluate=False)
        self.sign = sign


    def reduction(self):
        """Сокращение обеих сторон выражения."""
        self.left_side = sympy.powsimp(self.left_side)
        self.right_side = sympy.powsimp(self.right_side)


    def moving(self, side: Side = Side.left):
        """Сдвиг выражения в одну из сторон, по умолчанию влево."""
        if side==Side.left:
            self.left_side -= self.right_side
            self.right_side = 0
        elif side==Side.right:
            self.right_side -= self.left_side
            self.left_side = 0


    def __str__(self):
        return f"{self.left_side} {self.sign} {self.right_side}"


    def replacing(self, expression):
        pass
