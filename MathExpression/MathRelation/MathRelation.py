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
        # Разделить, если необходимо
        self.common_divisor = None
        # Выражение для замены
        self.replacement = None
        # Тип отношения
        self.type_relation = self.__define_relation_type()
        # Корни уравнения (!)
        self.answer = []

        self.__sign = sign
        self.__stages_of_solving = []
        self.app_stage("Начальная задача")


    def __define_relation_type(self) -> str:
        """Определяет тип отношения."""

        def __check_1(expression):
            """Если сумма двух слагаемых имеет вид a*t(x)^2 + b*t(x). Возвращает t(x)."""

            def discard_coef(expression):
                """Если expression имеет вид a*t(x)^b, то возвращается [t(x), b]."""
                if (expression.func == sympy.core.mul.Mul) and (expression.args[0].func in SP_TYPES_NUMS):
                    expression = expression.args[1]
                if (expression.func == sympy.core.power.Pow) and (expression.args[1].func in SP_TYPES_NUMS):
                    return [expression.args[0], expression.args[1]]
                return [expression, 1]

            temp = [discard_coef(expression.args[0]), discard_coef(expression.args[1])]
            if (temp[0][0] == temp[1][0]) and (temp[0][1]*2 == temp[1][1] or temp[0][1] == temp[1][1]*2):
                return True, temp[0][0]
            return False, temp[0][0]

        # Временное выражение для проверки
        temp_expr = sympy.powsimp(sympy.expand(self.left_side - self.right_side))

        # Вынесение и удаление общих делителей
        if (temp_expr != sympy.factor(temp_expr)):
            k = 0
            karetka = 0
            temp_list = sympy.factor(temp_expr).args
            for i in range(len(temp_list)):
                if temp_list[i].func == sympy.core.add.Add:
                    k += 1
                    karetka = i

            if k == 1:
                temp = temp_list[karetka]
                self.common_divisor = sympy.cancel(temp_expr / temp)
                temp_expr = temp

        # Если 0 слагаемых
        if temp_expr.func == sympy.core.numbers.Zero:
            return MathRelation.undefined

        # Если 1 слагаемое
        elif temp_expr.func != sympy.core.add.Add:
            if self.__is_there_replacement(temp_expr):
                return MathRelation.linear
            else:
                return MathRelation.undefined

        # Если 2 слагаемых
        elif temp_expr.func == sympy.core.add.Add and len(temp_expr.args) == 2:
            # Если одно из слагаемых - число
            if temp_expr.args[0].func in SP_TYPES_NUMS:
                if self.__is_there_replacement(temp_expr.args[1]):
                    return MathRelation.linear
                else:
                    return MathRelation.undefined
            # Если сумма имеет вид a*t(x)^2 + b*t(x)   КОММЕНТАРИИ НЕ УБИРАТЬ !!!
            # elif check_1(temp_expr):
            #     return MathRelation.quadratic
            else:
                return MathRelation.undefined

        # Если 3 слагаемых
        elif temp_expr.func == sympy.core.add.Add and len(temp_expr.args) == 3:
            # Если сумма имеет вид a*t(x)^2 + b*t(x) + c
            b, t_x = __check_1(temp_expr - temp_expr.args[0])
            if (temp_expr.args[0].func in SP_TYPES_NUMS) and b:
                if self.__is_there_replacement(t_x):
                    return MathRelation.quadratic
                else:
                    return MathRelation.undefined
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
        """Раскрытие скобок и сокращение обеих сторон выражения."""
        self.left_side = sympy.powsimp(sympy.expand(self.left_side))
        self.right_side = sympy.powsimp(sympy.expand(self.right_side))


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


    def divide_by_common_divisor(self):
        """Делит выражение на self.common_divisor, если оно не пусто."""
        if not self.common_divisor:
            pass
        elif self.common_divisor.subs(self.var, 0).func == sympy.core.numbers.ComplexInfinity:
            self.left_side = sympy.cancel(self.left_side / self.common_divisor)
            self.right_side = sympy.cancel(self.right_side / self.common_divisor)
            self.app_stage(f"Умножим обе стороны на {self.common_divisor ** -1}")
        elif self.common_divisor.subs(self.var, 0) == 0:
            self.left_side = sympy.cancel(self.left_side / self.common_divisor)
            self.right_side = sympy.cancel(self.right_side / self.common_divisor)
            self.app_stage(f"Разделим обе стороны на {self.common_divisor} (+ 0 к ответу)")
            self.answer.append(0)


    def __is_there_replacement(self, expression) -> bool:
        """Если expression не является переменной, то производится замена.
           Возвращает True, если expression - произведение числа на функцию, иначе False."""
        # Если выражение - произведение
        if (expression.func == sympy.core.mul.Mul):
            # Если произведение на число
            if expression.args[0].func in SP_TYPES_NUMS:
                if (expression.args[1] != self.var):
                    self.replacement = expression.args[1]
                return True
            else:
                return False
        if (expression != self.var):
            self.replacement = expression
        return True
