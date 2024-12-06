from typing import Any
from .MathRelation import MathRelation, EnteringExpressionError
import sympy



class MathEquality(MathRelation):
    """Класс уравнений."""

    def __init__(self, equality: str, variable: str):
        MathRelation.__init__(self, equality, '=', variable)
        # Корни уравнения
        self.__answer_of_equality: list[Any] = []



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
            self.__answer_of_equality.append(0)

        # Основное решение уравнения
        if (self.type_relation == MathEquality.linear):
            self.__answer_of_equality.append(self.solving_linear_equation())
        elif (self.type_relation == MathEquality.quadratic):
            for i in self.solving_square_equation():
                self.__answer_of_equality.append(i)
        elif (self.type_relation == MathEquality.undefined):
            raise EnteringExpressionError("Данная задача не решается.")



    def print_answer_equation(self) -> None:
        """Вывод решения уравнения."""
        print("Ответ:")
        if (len(self.__answer_of_equality) == 0):
            print("  Решения нет.")
        else:
            for i in self.__answer_of_equality:
                print(f"  {self.var} = {i}")



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
            if koefs[i].func.is_number:
                c = koefs[i]
            elif koefs[i].func == sympy.core.mul.Mul and koefs[i].args[0].func.is_number:
                if koefs[i].args[1] == self.var:
                    b = koefs[i].args[0]
                else:
                    if koefs[i].args[0] == -1:
                        a = -1
                    else:
                        a = koefs[i].args[0]

        self.app_stage("Достанем коэффиценты из уравнения", f"a = {a}, b = {b}, c = {c}")

        roots = []

        # print(c)
        d = b**2-4*a*c
        self.app_stage("Вычислим дискриминант по формуле D = b**2-4*a*c:",  f"D = {b}**2-4*{a}*{c} = {b**2} - ({4*a*c}) = {d}")

        if d > 0:
            self.app_stage("Так как дискриминант больше 0, то будет два корня", f"D = {d} > 0")
            sqrt_D = sympy.sqrt(d)
            self.app_stage("Корень дискриминанта:", f"sqrt(D) = {sqrt_D}")
            self.app_stage("Первый корень вчитываем по формуле: (-b+sqtr(D)) / 2*a", f"({-b}+{sqrt_D}) / 2 * {a}")
            root_1 = (-b + sqrt_D) / (2*a)
            self.app_stage("Первый корень:", f"{root_1}")
            roots.append(root_1)

            self.app_stage("Второй корень вчитываем по формуле: (-b-sqtr(D)) / 2*a", f"({-b}+{sqrt_D}) / 2 * {a}")
            root_2 = (-b - sqrt_D) / (2*a)
            self.app_stage("Воторой корень:", f"{root_2}")
            roots.append(root_2)

        elif d == 0:
            self.app_stage("Так как дискриминант равен 0, то будет один корень", f"D = {d}")
            sqrt_D = sympy.sqrt(d)
            self.app_stage("Корень дискриминанта:", f"sqrt(D) = {sqrt_D}")
            root = -b / (2*a)
            roots.append(root)

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


