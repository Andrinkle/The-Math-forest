import sympy
import sympy.core.numbers
import sympy.core.add
import sympy.core.mul
import sympy.core.power



SP_TYPES_NUMS = [sympy.core.numbers.Integer,
                 sympy.core.numbers.One,
                 sympy.core.numbers.NegativeOne,
                 sympy.core.numbers.Rational,
                 sympy.core.numbers.Float,
                 sympy.core.numbers.Half,
                 sympy.core.numbers.Pi,
                 sympy.exp]


class Side:
    left = 'l'
    right = 'r'


class EnteringExpressionError(Exception):
    pass



class MathRelation:
    """Класс математических отношений."""

    # Типы отношений
    linear = 'l'
    quadratic = 'q'
    undefined = 'u'


    def __init__(self, expression: str, sign: str, variable_1: str, variable_2: str=''):
        # Переменная в данном оношении
        self.var = sympy.Symbol(variable_1)
        # Вторая переменная в данном оношении
        if variable_2:
            self.var2 = sympy.Symbol(variable_2)
        exp_list = expression.split(sign)
        # Левая сторона
        self.left_side = sympy.sympify(exp_list[0], evaluate=False)
        # Правая сторона
        self.right_side = sympy.sympify(exp_list[1], evaluate=False)
        # Тип отношения
        self.type_relation = self.define_relation_type()

        self.__sign = sign
        self.__stages_of_solving = []
        self.app_stage("Начальная задача")


    def define_relation_type(self) -> str:
        """Определяет тип отношения."""

        def check_1(expression) -> bool:
            """Если сумма двух слагаемых имеет вид a*t(x)^2 + b*t(x)"""

            temp = [self.discard_coef(expression.args[0]), self.discard_coef(expression.args[1])]
            if (temp[0][0] == temp[1][0]) and (temp[0][1]*2 == temp[1][1] or temp[0][1] == temp[1][1]*2):
                return True
            return False

        temp_expr = sympy.powsimp(self.left_side - self.right_side)

        # Если 0 слагаемых
        if temp_expr.func == sympy.core.numbers.Zero:
            return MathRelation.linear

        # Если 1 слагаемое
        elif temp_expr.func != sympy.core.add.Add:
            return MathRelation.linear

        # Если 2 слагаемых
        elif temp_expr.func == sympy.core.add.Add and len(temp_expr.args) == 2:
            # Если одно из слагаемых - число
            if temp_expr.args[0].func in SP_TYPES_NUMS or temp_expr.args[1].func in SP_TYPES_NUMS:
                return MathRelation.linear
            # Если сумма имеет вид a*t(x)^2 + b*t(x)
            elif check_1(temp_expr):
                return MathRelation.quadratic
            else:
                return MathRelation.undefined

        # Если 3 слагаемых
        elif temp_expr.func == sympy.core.add.Add and len(temp_expr.args) == 3:
            # Если сумма имеет вид a*t(x)^2 + b*t(x) + c
            if (temp_expr.args[0].func in SP_TYPES_NUMS) and (check_1(temp_expr - temp_expr.args[0])):
                    return MathRelation.quadratic
            else:
                return MathRelation.undefined

        # Если более 3 слагаемых
        else:
            return MathRelation.undefined


    def app_stage(self, description:str):
        """Добавление нового этапа в решение."""
        self.__stages_of_solving.append([description, str(self)])


    def print_stages(self):
        """Вывод всех этапов решения."""
        for i in self.__stages_of_solving:
            print(i[0])
            print("  " + i[1])


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
        return f"{self.left_side} {self.__sign} {self.right_side}"


    def discard_coef(self, expression):
        """Если expression имеет вид a*t(x)^b, то возвращается [t(x), b]"""
        if (expression.func == sympy.core.mul.Mul) and (expression.args[0].func in SP_TYPES_NUMS):
            expression = expression.args[1]
        if (expression.func == sympy.core.power.Pow) and (expression.args[1].func in SP_TYPES_NUMS):
            return [expression.args[0], expression.args[1]]
        return [expression, 1]
    
    def replacing(self, expression):
        pass
