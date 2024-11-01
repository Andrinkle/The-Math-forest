from MathExpression.MathRelation import MathRelation
import sympy


class SquareEquality(MathRelation):
    """Класс решения квадратных* уравнений."""

    def solving_square_equation(self):
        """Решение квадратного уравнения."""

        if self.right_side != 0:
            self.moving()
            self.app_stage("Перемещаем всё в левую сторону")
        
        if self.left_side != sympy.powsimp(self.left_side) or self.right_side != sympy.powsimp(self.right_side):
            self.reduction()
            self.app_stage("Сокращаем обе стороны")

        if self.right_side.subs(self.var, 0) != self.right_side:
            self.left_side = sympy.powsimp(self.left_side - (self.right_side - self.right_side.subs(self.var, 0)))
            self.right_side = self.right_side.subs(self.var, 0)
            self.app_stage(f"Переносим члены, содержащие переменную {self.var}, влево")

        if self.left_side.subs(self.var, 0) != 0:
            self.right_side = sympy.powsimp(self.right_side - self.left_side.subs(self.var, 0))
            self.left_side = sympy.powsimp(self.left_side - self.left_side.subs(self.var, 0))

        # Решение
        koefs = (self.left_side).args # Выделение коэфицентов
        print(koefs)
        if (str(koefs[0].args[1]) == self.var): # Расстановка по местам, чтобы a для x^2, а b для x
            a = koefs[1].args[0]
            b = koefs[0].args[0]
        else:
            a = koefs[0].args[0]
            b = koefs[1].args[0]
        c = -(self.right_side) #
        # Проверка на равность чисто х, если так, то коэф перед ним равен 1
        if (a == self.var):
            a = 1
        if (b == self.var):
            b = 1
        print(f"Коэффициенты: a = {a}, b = {b}, c = {c}")

        roots = []
        d = b**2-4*a*c
        print(f"\nДискриминант находится по формуле:b**2-4*a*c и равно {d} ")

        if d > 0:
            sqrt_D = sympy.sqrt(d)
            print(f"Корень дискриминанта равен {sqrt_D}")
            root_1 = (-b + sqrt_D) / (2*a)
            roots.append(root_1)
            root_2 = (-b - sqrt_D) / (2*a)
            roots.append(root_2)
            print(f"x1 = {root_1}, \nx2 = {root_2}\n")
        elif d == 0:
            sqrt_D = sympy.sqrt(d)
            print(f"Корень дискриминанта равен {sqrt_D}")
            root = -b / (2*a)
            roots.append(root)
            print(f"x = {root}\n")
        else:
            print("Корней нет")

        return roots

