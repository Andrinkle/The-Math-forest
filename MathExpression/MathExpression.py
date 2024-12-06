from .MathRelation import EnteringExpressionError, MathEquality, MathInequality



class MathExpression(MathInequality):
    """Класс решения уравнений, неравенств и их систем."""

    equality = 'e'
    inequality = 'i'
    system = 's'


    def __init__(self, expression: str, variable: str):
        sign = MathExpression.define_expression_type(expression)
        if (sign == '='):
            MathEquality.__init__(self, expression, variable)
            self.__type_expression = MathExpression.equality
        else:
            MathInequality.__init__(self, expression, sign, variable)
            self.__type_expression = MathExpression.inequality



    def define_expression_type(str_expression: str) -> str:
        """Определяет тип задачи."""
        if ('!=' in str_expression):
            return '!='
        elif ('<=' in str_expression):
            return '<='
        elif ('>=' in str_expression):
            return '>='
        elif ('<' in str_expression):
            return '<'
        elif ('>' in str_expression):
            return '>'
        elif ('=' in str_expression):
            return '='
        else:
            raise EnteringExpressionError("Неопределённый знак отношения.")



    def solving_expression(self):
        """Решение задачи."""
        if (self.__type_expression == MathExpression.equality):
            self.solving_equation()
        elif (self.__type_expression == MathExpression.inequality):
            self.solving_inequation()



    def print_answer(self):
        """Вывод решения задачи."""
        if (self.__type_expression == MathExpression.equality):
            self.print_answer_equation()

        elif (self.__type_expression == MathExpression.inequality):
            pass

        elif (self.__type_expression == MathExpression.system):
            pass

