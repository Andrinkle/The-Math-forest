from MathExpression.MathRelation import MathRelation, EnteringExpressionError, SP_TYPES_NUMS
from .LinearEquality import LinearEquality
from .SquareEquality import SquareEquality
import sympy
import sympy.core.add
import sympy.core.mul
import sympy.core.power


class MathEquality(LinearEquality, SquareEquality):
    """Класс уравнений."""

    linear = 'l'
    quadratic = 'q'
    undefined = 'u'


    def __init__(self, str_expression: str, variable: str):
        MathRelation.__init__(self, str_expression, '=', variable)
        self.type_equality = self.define_equality_type()


    def define_equality_type(self) -> str:
        """Определяет тип уравнения."""

        def check_1(expression) -> bool:
            """Если сумма двух слагаемых имеет вид a*t(x)^2 + b*t(x)"""

            def discard_coef(expression):
                """Если expression имеет вид a*t(x)^b, то возвращается [t(x), b]"""
                if (expression.func == sympy.core.mul.Mul) and (expression.args[0].func in SP_TYPES_NUMS):
                    expression = expression.args[1]
                if (expression.func == sympy.core.power.Pow) and (expression.args[1].func in SP_TYPES_NUMS):
                    return [expression.args[0], expression.args[1]]
                return [expression, 1]

            temp = [discard_coef(expression.args[0]), discard_coef(expression.args[1])]
            if (temp[0][0] == temp[1][0]) and (temp[0][1]*2 == temp[1][1] or temp[0][1] == temp[1][1]*2):
                return True
            return False

        temp_expr = sympy.powsimp(self.left_side - self.right_side)

        # Если 0 слагаемых
        if temp_expr.func == sympy.core.numbers.Zero:
            return MathEquality.linear

        # Если 1 слагаемое
        elif temp_expr.func != sympy.core.add.Add:
            return MathEquality.linear

        # Если 2 слагаемых
        elif temp_expr.func == sympy.core.add.Add and len(temp_expr.args) == 2:
            # Если одно из слагаемых - число
            if temp_expr.args[0].func in SP_TYPES_NUMS or temp_expr.args[1].func in SP_TYPES_NUMS:
                return MathEquality.linear
            # Если сумма имеет вид a*t(x)^2 + b*t(x)
            elif check_1(temp_expr):
                return MathEquality.quadratic
            else:
                return MathEquality.undefined

        # Если 3 слагаемых
        elif temp_expr.func == sympy.core.add.Add and len(temp_expr.args) == 3:
            # Если сумма имеет вид a*t(x)^2 + b*t(x) + c
            if (temp_expr.args[0].func in SP_TYPES_NUMS) and (check_1(temp_expr - temp_expr.args[0])):
                    return MathEquality.quadratic
            else:
                return MathEquality.undefined

        # Если более 3 слагаемых
        else:
            return MathEquality.undefined


    def solving_equation(self):
        """Решение уравнения."""
        if self.type_equality == MathEquality.linear:
            return self.solving_linear_equation()
        elif self.type_equality == MathEquality.quadratic:
            return self.solving_square_equation()
        elif self.type_equality == MathEquality.undefined:
            raise EnteringExpressionError("Данная задача не решается.")

