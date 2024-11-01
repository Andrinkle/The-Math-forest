from .MathRelation import EnteringExpressionError
from .MathRelation import MathRelation
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
            print("Ответ:")
            if self.type_relation == MathRelation.linear:
                print(f"  {self.var} = {self.answer[0]}")
            if self.type_relation == MathRelation.quadratic:
                if len(self.answer) == 0:
                    print("  Решения нет.")
                elif len(self.answer) == 1:
                    print(f"  {self.var} = {self.answer[0]}")
                elif len(self.answer) == 2:
                    print(f"  {self.var}_1 = {self.answer[0]}")
                    print(f"  {self.var}_2 = {self.answer[1]}")

        elif self.type_expression == MathExpression.inequality:
            pass

        elif self.type_expression == MathExpression.system:
            pass

