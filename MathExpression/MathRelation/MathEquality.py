from typing import Any
from .MathRelation import MathRelation, EnteringExpressionError
import sympy



class MathEquality(MathRelation):
    """Класс уравнений."""

    def __init__(self, equality: str, variable: str):
        MathRelation.__init__(self, equality, '=', variable)
        # Корни уравнения
        self.__answer_of_equality: list[Any] = []
        # Корни уравнения, если была произведена замена
        self.__answer_of_replacement: list[Any] = []



    def print_answer_equation(self) -> None:
        """Вывод решения уравнения."""
        print("Ответ:")
        if (len(self.__answer_of_equality) == 0):
            print("  Решения нет.")
        else:
            for i in self.__answer_of_equality:
                print(f"  {self.var} = {i}")



    def __app_answer(self, expr: Any) -> None:
        """Добавление корня в решение."""
        if (self.replacement):
            self.__answer_of_replacement.append(expr)
        else:
            self.__answer_of_equality.append(expr)



    def solving_equation(self) -> None:
        """Решение уравнения."""

        # Произвести замену, если необходимо
        if (self.replacement):
            old_var = self.var
            self.var = sympy.Symbol('t')
            self.left_side = self.left_side.subs(self.replacement, self.var)
            self.right_side = self.right_side.subs(self.replacement, self.var)
            if (self.common_divisor != None):
                self.common_divisor = self.common_divisor.subs(self.replacement, self.var)
            self.app_stage(f"Заменяем {self.replacement} на {self.var}")
            f"{self.replacement} = {old_var}"

        # Сокращение уравнения
        temp = [self.left_side, self.right_side]
        self.reduction()
        if (str(temp[0]) != str(self.left_side)) or (str(temp[1]) != str(self.right_side)):
            self.app_stage("Сокращаем обе стороны")

        # Деление на общий делитель
        if (self.divide_by_common_divisor()):
            self.__app_answer(0)

        # Основное решение уравнения
        if (self.type_relation == MathEquality.linear):
            self.__app_answer(self.solving_linear_equation())
        elif (self.type_relation == MathEquality.quadratic):
            for i in self.solving_square_equation():
                self.__app_answer(i)
        elif (self.type_relation == MathEquality.undefined):
            raise EnteringExpressionError("Данная задача не решается.")



    def solving_exponential(self, base, degree):
        """Функция решения обратной замены a^(bx^c+d) = y."""
        for root in self.__answer_of_equality:
            cdegree = degree
            if (base > 0) and (base != 1):
                resh = sympy.log(root, base) # left_part

                # Поиск коэфицента d
                degree_args = cdegree.args
                for i in degree_args:
                    if i.is_number:
                        d = i
                resh = resh - d # left_part
                cdegree = cdegree - d # right_part

                # Поиск коэфицента b
                degree_args = cdegree.args
                b = 1
                for i in degree_args:
                    if i.is_number:
                        b = i
                resh = resh / b # left_part
                cdegree = cdegree / b # right_part

                # Поиск коэфицента c
                degree_args = cdegree.args
                c = 1
                for i in degree_args:
                    if i.is_number:
                        c = i
                resh = pow(resh, 1/c) # left_part
                cdegree = pow(cdegree, 1/c) # right_part



    def solving_power(self, degree):
        """Метод решения уравнения x^a = y."""
        for root in self.__answer_of_equality:
            if root >= 0:
                self.resheniya.append(pow(root, 1/degree))
                if degree % 2 == 0: # Проверка на чётность
                    self.resheniya.append(-(pow(root, 1/degree))) # Добавление в ответ -x



    def solving_square_equation(self) -> list[Any]:
        """Решение квадратного уравнения, возвращает массив корней."""

        if self.right_side.subs(self.var, 0) != self.right_side:
            self.left_side = sympy.powsimp(self.left_side - (self.right_side - self.right_side.subs(self.var, 0)))
            self.right_side = self.right_side.subs(self.var, 0)
            self.app_stage(f"Переносим члены, содержащие переменную {self.var}, влево")

        if self.left_side.subs(self.var, 0) != 0:
            self.right_side = sympy.powsimp(self.right_side - self.left_side.subs(self.var, 0))
            self.left_side = sympy.powsimp(self.left_side - self.left_side.subs(self.var, 0))

        if self.right_side != 0:
            self.moving()
            self.app_stage("Перемещаем всё в левую сторону")

        # Решение
        koefs = (self.left_side).args # Выделение коэфицентов

        # Начальные значения коэфицентов
        a = 1
        b = 1

        # Распределение коэфицетов по буквам
        for i in range(len(koefs)):
            if koefs[i].is_number:
                c = koefs[i]
            elif koefs[i].is_Mul and koefs[i].args[0].is_number:
                if koefs[i].args[1] == self.var:
                    b = koefs[i].args[0]
                else:
                    if koefs[i].args[0] == -1:
                        a = -1
                    else:
                        a = koefs[i].args[0]

        self.app_stage("Достанем коэффиценты из уравнения", f"a = {a}, b = {b}, c = {c}")

        roots = []

        d = b**2-4*a*c
        self.app_stage("Вычислим дискриминант по формуле D = b**2-4*a*c:",  f"D = {b}**2-4*{a}*{c} = {d}")

        if d > 0:
            self.app_stage(f"Так как D = {d} > 0, то будет два корня")
            sqrt_D = sympy.sqrt(d)
            root_1 = (-b + sqrt_D) / (2*a)
            roots.append(root_1)
            self.app_stage("Первый корень вчитываем по формуле: (-b+sqtr(D)) / 2*a", f"({-b}+{sqrt_D}) / 2 * {a} = {root_1}")

            root_2 = (-b - sqrt_D) / (2*a)
            roots.append(root_2)
            self.app_stage("Второй корень вчитываем по формуле: (-b-sqtr(D)) / 2*a", f"({-b}+{sqrt_D}) / 2 * {a} = {root_2}")

        elif d == 0:
            self.app_stage("Так как D = 0, то будет один корень")
            root = -b / (2*a)
            roots.append(root)
            self.app_stage("Второй корень вчитываем по формуле: -b / 2*a", f"{-b} / 2 * {a} = {root}")

        return roots



    def solving_linear_equation(self) -> Any:
        """Решение линейного уравнения, возвращает корень."""

        if (self.right_side.subs(self.var, 0) != self.right_side):
            self.left_side = sympy.powsimp(self.left_side - (self.right_side - self.right_side.subs(self.var, 0)))
            self.right_side = self.right_side.subs(self.var, 0)
            self.app_stage(f"Переносим члены, содержащие переменную {self.var}, влево")

        if (self.left_side.subs(self.var, 0) != 0):
            self.right_side = sympy.powsimp(self.right_side - self.left_side.subs(self.var, 0))
            self.left_side = sympy.powsimp(self.left_side - self.left_side.subs(self.var, 0))
            self.app_stage(f"Переносим члены, не содержащие переменную {self.var}, вправо")

        divisor = self.left_side.subs(self.var, 1)
        if (divisor != 1):
            self.right_side /= divisor
            self.left_side /= divisor
            self.app_stage(f"Разделим обе стороны на {divisor}")

        return self.right_side


