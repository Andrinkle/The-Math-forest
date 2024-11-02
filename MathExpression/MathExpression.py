from .MathRelation import EnteringExpressionError
# from .MathRelation import MathRelation
from .MathEquality import MathEquality
from .MathInequality import MathInequality


class MathExpression(MathInequality):
    """Класс решения уравнений, неравенств и их систем."""

    equality = 'e'
    inequality = 'i'
    system = 's'

    def __init__(self, str_expression: str, variable: str):
        sign = MathExpression.define_expression_type(str_expression)
        if sign == '=':
            MathEquality.__init__(self, str_expression, variable)
            self.type_expression = MathExpression.equality
        else:
            MathInequality.__init__(self, str_expression, sign, variable)
            self.type_expression = MathExpression.inequality


    def define_expression_type(str_expression: str) -> str:
        """Определяет тип задачи."""
        if '!=' in str_expression:
            return '!='
        elif '<=' in str_expression:
            return '<='
        elif '>=' in str_expression:
            return '>='
        elif '<' in str_expression:
            return '<'
        elif '>' in str_expression:
            return '>'
        elif '=' in str_expression:
            return '='
        else:
            raise EnteringExpressionError("Неопределённый знак отношения.")


    def solving_expression(self):
        """Решение задачи."""
        if self.type_expression == MathExpression.equality:
            return self.solving_equation()
        elif self.type_expression == MathExpression.inequality:
            return self.solving_inequation()


    def print_answer(self):
        """Вывод решения задачи."""
        if self.type_expression == MathExpression.equality:
            self.print_answer_equation()

        elif self.type_expression == MathExpression.inequality:
            pass

        elif self.type_expression == MathExpression.system:
            pass

