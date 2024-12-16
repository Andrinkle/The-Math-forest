from typing import Any
import sympy



# Класс для вызова ошибки
class EnteringExpressionError(Exception):
    pass



class MathRelation:
    """Класс математических отношений ({выражение} ~ {выражение})."""

    # Типы отношений
    linear = 0
    quadratic = 1
    undefined = 2
    # Типы выражений, которые могут быть в замене
    exponential = 3
    power = 4
    trigonometric = 5



    def __init__(self,
                 # Отношение в виде строки
                 relation: str,
                 # Знак отношения
                 sign: str,
                 # Переменные, по которым решается задача
                 variable_1: str, variable_2: str = ''):

        # Переменная в данном оношении
        self.var: sympy.Symbol = sympy.Symbol(variable_1)
        # Вторая переменная в данном оношении
        if (variable_2):
            self.var2: sympy.Symbol = sympy.Symbol(variable_2)
        exp_list = relation.split(sign)
        # Левая сторона
        self.left_side: Any = sympy.sympify(exp_list[0], evaluate=False)
        # Правая сторона
        self.right_side: Any = sympy.sympify(exp_list[1], evaluate=False)
        # Выражение, которое будет делить/умножать данное отношение
        self.common_divisor: Any = None
        # Тип отношения
        self.type_relation: int = self.__define_relation_type()

        # Переменная для замены
        self.var_replace: sympy.Symbol
        # Выражение для замены (t(x))
        self.replacement: Any = None
        # Тип замены
        self.type_replace: int

        # Знак отношения
        self.__sign: str = sign
        # Этапы решения задачи.
        # В каждом элементе списка хранится список,
        # в котором 1-й эл. - описание этапа, 2-й эл. - итог этапа.
        self.__stages_of_solving: list[list[str]] = []
        # Первый этап - сама задача
        self.app_stage("Начальная задача")



    def __str__(self) -> str:
        return f"{self.left_side} {self.__sign} {self.right_side}"



    def __define_relation_type(self) -> str:
        """Определяет тип отношения."""

        def __check_1(expression: Any) -> tuple[bool, Any]:
            """Если сумма двух слагаемых (!) имеет вид a*t(x)^2 + b*t(x). Возвращает t(x)."""

            def __discard_coef(expression: Any) -> list[Any]:
                """Если expression имеет вид a*t(x)^b, то возвращается [t(x), b]."""
                if (expression.is_Mul and expression.args[0].is_number):
                    expression = expression.args[1]
                if (expression.is_Pow and expression.args[1].is_number):
                    return [expression.args[0], expression.args[1]]
                return [expression, 1]

            temp = [__discard_coef(expression.args[0]), __discard_coef(expression.args[1])]
            if ((temp[0][0] == temp[1][0]) and (temp[0][1]*2 == temp[1][1] or temp[0][1] == temp[1][1]*2)):
                return (True, temp[0][0])
            return (False, temp[0][0])

        # Временное выражение для текущей проверки
        temp_expr = sympy.powsimp(sympy.expand(self.left_side - self.right_side))

        # Вынесение и удаление общего делителя
        if (temp_expr != sympy.factor(temp_expr)):
            k = 0
            karetka = 0
            temp_list = sympy.factor(temp_expr).args
            for i in range(len(temp_list)):
                if (temp_list[i].is_Add):
                    k += 1
                    karetka = i

            if (k == 1):
                temp = temp_list[karetka]
                # Сохранение общего делителя для основного решения
                self.common_divisor = sympy.cancel(temp_expr / temp)
                temp_expr = temp

        # Если 0 слагаемых
        if (temp_expr == 0):
            return MathRelation.undefined

        # Если 1 слагаемое
        # elif temp_expr.func != sympy.core.add.Add:
        elif (not temp_expr.is_Add):
            # Если можно произвести замену
            if (self.__is_there_replacement(temp_expr)):
                return MathRelation.linear
            return MathRelation.undefined

        # Если 2 слагаемых
        elif (temp_expr.is_Add and len(temp_expr.args) == 2):
            # Если одно из слагаемых - число
            if (temp_expr.args[0].is_number):
                # Если можно произвести замену
                if (self.__is_there_replacement(temp_expr.args[1])):
                    return MathRelation.linear
            # Вариант квадратного уравнения не рассматривается, так как ранее было произведено деление на общий множитель
            # Если сумма имеет вид a*t(x)^2 + b*t(x)   КОММЕНТАРИИ НЕ УБИРАТЬ !!!
            # elif check_1(temp_expr):
            #     return MathRelation.quadratic
            return MathRelation.undefined

        # Если 3 слагаемых
        elif (temp_expr.is_Add and len(temp_expr.args) == 3):
            # Если сумма имеет вид a*t(x)^2 + b*t(x) + c
            b, t_x = __check_1(temp_expr - temp_expr.args[0])
            if (temp_expr.args[0].is_number and b):
                # Если можно произвести замену
                if (self.__is_there_replacement(t_x)):
                    return MathRelation.quadratic
            return MathRelation.undefined

        # Если более 3 слагаемых
        return MathRelation.undefined



    def __define_replace_type(expression: Any) -> int:
        pass



    def app_stage(self,
                  # Описание этапа
                  description: str,
                  # Результат этапа (по умолчанию - само отношение)
                  result: str = None) -> None:
        """Добавление нового этапа в решение."""

        if (result == None):
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
        if (side == "left"):
            self.left_side -= self.right_side
            self.right_side = 0
        elif (side == "right"):
            self.right_side -= self.left_side
            self.left_side = 0



    def divide_by_common_divisor(self) -> bool:
        """Делит выражение на self.common_divisor, если оно не пусто.
           Возвращает True, если 0 является корнем уравнения (!)."""
        if (not self.common_divisor):
            return False
        # Если common_divisor - число
        elif (self.common_divisor.is_number):
            self.left_side = sympy.cancel(self.left_side / self.common_divisor)
            self.right_side = sympy.cancel(self.right_side / self.common_divisor)
            self.app_stage(f"Разделим обе стороны на {self.common_divisor}")
        # Если в знаменателе есть переменная отношения
        elif (self.common_divisor.subs(self.var, 0).is_number):
            self.left_side = sympy.cancel(self.left_side / self.common_divisor)
            self.right_side = sympy.cancel(self.right_side / self.common_divisor)
            self.app_stage(f"Умножим обе стороны на {self.common_divisor ** -1}")
        # Если в числетеле есть переменная отношения
        elif (self.common_divisor.subs(self.var, 0) == 0):
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
        # Если выражение - произведение на число
        if (expression.is_Mul):
            # Если произведение на число
            if (expression.args[0].is_number):
                # Если выражение для замены - не сама переменная
                if (expression.args[1] != self.var):
                    self.replacement = expression.args[1]
                    self.type_replace = self.__define_replace_type(expression.args[1])
                return True
            else:
                return False
        # Если выражение для замены - не сама переменная
        if (expression != self.var):
            self.replacement = expression
            self.type_replace = self.__define_replace_type(expression)
        return True


