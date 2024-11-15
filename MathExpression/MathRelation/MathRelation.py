from typing import Any
import sympy
import sympy.core.numbers
import sympy.core.add
import sympy.core.mul
import sympy.core.power


# Список всех типов чисел в sympy
SP_TYPES_NUMS = [sympy.core.numbers.Integer,
                 sympy.core.numbers.One,
                 sympy.core.numbers.NegativeOne,
                 sympy.core.numbers.Rational,
                 sympy.core.numbers.Float,
                 sympy.core.numbers.Half,
                 sympy.core.numbers.Pi,
                 sympy.exp]


# Класс для вызова ошибки
class EnteringExpressionError(Exception):
    pass



class MathRelation:
    """Класс математических отношений ({выражение} ~ {выражение})."""

    # Типы отношений
    linear = 'l'
    quadratic = 'q'
    undefined = 'u'



    def __init__(self,
                 # Отношение в виде строки
                 relation:str,
                 # Знак отношения
                 sign:str,
                 # Переменные, по которым решается задача
                 variable_1:str, variable_2:str = ''):

        # Переменная в данном оношении
        self.var: sympy.Symbol = sympy.Symbol(variable_1)
        # Вторая переменная в данном оношении
        if variable_2:
            self.var2: sympy.Symbol = sympy.Symbol(variable_2)
        exp_list = relation.split(sign)
        # Левая сторона
        self.left_side: Any = sympy.sympify(exp_list[0], evaluate=False)
        # Правая сторона
        self.right_side: Any = sympy.sympify(exp_list[1], evaluate=False)
        # Выражение, которое будет делить/умножать данное отношение
        self.common_divisor: Any = None
        # Выражение для замены
        self.replacement: Any = None
        # Тип отношения
        self.type_relation: str = self.__define_relation_type()

        # Знак отношения
        self.__sign: str = sign
        # Этапы решения задачи.
        # В каждом элементе списка хранится список,
        # в котором 1-й эл. - описание этапа, 2-й эл. - итог этапа.
        self.__stages_of_solving: list[list[str]] = []
        # Первый этап - сама задача
        self.app_stage("Начальная задача")



    def __define_relation_type(self) -> str:
        """Определяет тип отношения."""

        def __check_1(expression: Any) -> Any:
            """Если сумма двух слагаемых (!) имеет вид a*t(x)^2 + b*t(x). Возвращает t(x)."""

            def __discard_coef(expression: Any) -> list[Any]:
                """Если expression имеет вид a*t(x)^b, то возвращается [t(x), b]."""
                if (expression.func == sympy.core.mul.Mul) and (expression.args[0].func in SP_TYPES_NUMS):
                    expression = expression.args[1]
                if (expression.func == sympy.core.power.Pow) and (expression.args[1].func in SP_TYPES_NUMS):
                    return [expression.args[0], expression.args[1]]
                return [expression, 1]

            temp = [__discard_coef(expression.args[0]), __discard_coef(expression.args[1])]
            if (temp[0][0] == temp[1][0]) and (temp[0][1]*2 == temp[1][1] or temp[0][1] == temp[1][1]*2):
                return True, temp[0][0]
            return False, temp[0][0]

        # Временное выражение для текущей проверки
        temp_expr = sympy.powsimp(sympy.expand(self.left_side - self.right_side))

        # Вынесение и удаление общего делителя
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
                # Сохранение общего делителя для основного решения
                self.common_divisor = sympy.cancel(temp_expr / temp)
                temp_expr = temp

        # Если 0 слагаемых
        if temp_expr.func == sympy.core.numbers.Zero:
            return MathRelation.undefined

        # Если 1 слагаемое
        elif temp_expr.func != sympy.core.add.Add:
            # Если можно произвести замену
            if self.__is_there_replacement(temp_expr):
                return MathRelation.linear
            return MathRelation.undefined

        # Если 2 слагаемых
        elif temp_expr.func == sympy.core.add.Add and len(temp_expr.args) == 2:
            # Если одно из слагаемых - число
            if temp_expr.args[0].func in SP_TYPES_NUMS:
                # Если можно произвести замену
                if self.__is_there_replacement(temp_expr.args[1]):
                    return MathRelation.linear
            # Вариант квадратного уравнения не рассматривается, так как ранее было произведено деление на общий множитель
            # Если сумма имеет вид a*t(x)^2 + b*t(x)   КОММЕНТАРИИ НЕ УБИРАТЬ !!!
            # elif check_1(temp_expr):
            #     return MathRelation.quadratic
            return MathRelation.undefined

        # Если 3 слагаемых
        elif temp_expr.func == sympy.core.add.Add and len(temp_expr.args) == 3:
            # Если сумма имеет вид a*t(x)^2 + b*t(x) + c
            b, t_x = __check_1(temp_expr - temp_expr.args[0])
            if (temp_expr.args[0].func in SP_TYPES_NUMS) and b:
                # Если можно произвести замену
                if self.__is_there_replacement(t_x):
                    return MathRelation.quadratic
            return MathRelation.undefined

        # Если более 3 слагаемых
        return MathRelation.undefined



    def app_stage(self,
                  # Описание этапа
                  description: str,
                  # Результат этапа (по умолчанию - само отношение)
                  result: str = None) -> None:
        """Добавление нового этапа в решение."""

        if result == None:
            self.__stages_of_solving.append([description, str(self)])
        else:
            self.__stages_of_solving.append([description, result])



    def print_stages(self) -> None:
        """Вывод всех этапов решения."""
        for i in self.__stages_of_solving:
            print(i[0])
            print("  " + i[1])



    def reduction(self) -> None:
        """Раскрытие скобок и сокращение обеих сторон выражения."""
        self.left_side = sympy.powsimp(sympy.expand(self.left_side))
        self.right_side = sympy.powsimp(sympy.expand(self.right_side))



    def moving(self, side: str = "left") -> None:
        """Сдвиг выражения в одну из сторон, по умолчанию влево."""
        if side == "left":
            self.left_side -= self.right_side
            self.right_side = 0
        elif side == "right":
            self.right_side -= self.left_side
            self.left_side = 0



    def __str__(self) -> str:
        return f"{self.left_side} {self.__sign} {self.right_side}"



    def divide_by_common_divisor(self) -> bool:
        """Делит выражение на self.common_divisor, если оно не пусто.
           Возвращает True, если 0 является корнем уравнения (!)."""
        if not self.common_divisor:
            pass
        # Если в знаменателе есть переменная отношения
        elif self.common_divisor.subs(self.var, 0).func == sympy.core.numbers.ComplexInfinity:
            self.left_side = sympy.cancel(self.left_side / self.common_divisor)
            self.right_side = sympy.cancel(self.right_side / self.common_divisor)
            self.app_stage(f"Умножим обе стороны на {self.common_divisor ** -1}")
        # Если в числетеле есть переменная отношения
        elif self.common_divisor.subs(self.var, 0) == 0:
            self.left_side = sympy.cancel(self.left_side / self.common_divisor)
            self.right_side = sympy.cancel(self.right_side / self.common_divisor)
            self.app_stage(f"Разделим обе стороны на {self.common_divisor} (+ 0 к ответу)")
            return True
        else:
            raise EnteringExpressionError
        return False



    def __is_there_replacement(self, expression) -> bool:
        """Если expression не является переменной, то производится замена.
           Возвращает True, если expression - произведение числа на функцию, иначе False."""
        # Если выражение - произведение
        if (expression.func == sympy.core.mul.Mul):
            # Если произведение на число
            if expression.args[0].func in SP_TYPES_NUMS:
                # Если выражение для замены - не сама переменная
                if (expression.args[1] != self.var):
                    self.replacement = expression.args[1]
                return True
            else:
                return False
        # Если выражение для замены - не сама переменная
        if (expression != self.var):
            self.replacement = expression
        return True
