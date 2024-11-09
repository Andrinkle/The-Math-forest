from MathExpression.MathRelation import MathRelation
import sympy


class SquareEquality(MathRelation):
    """Класс решения псевдо-квадратных уравнений."""

    def solving_square_equation(self):
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

        a = koefs[1].args[0]
        b = koefs[2].args[0]
        c = koefs[0]
        
        # Проверка на равность чисто х, если так, то коэф перед ним равен 1
        if (a == self.var):
            a = 1
        if (b == self.var):
            b = 1
        print(f"Достанем коэфиценты \n  a = {a}\n  b = {b}\n  c = {c}")
        roots = []
        
        d = b**2-4*a*c
        print(f"Вычислим дискриминант по формуле b**2-4*a*c: \n  {b}**2-4*{a}*{c} = {b**2} - {4*a*c} = {d}")
        
        if d > 0:
            sqrt_D = sympy.sqrt(d)
            print(f"Корень дискриминанта равен {sqrt_D}")
            root_1 = (-b + sqrt_D) / (2*a)
            roots.append(root_1)
            root_2 = (-b - sqrt_D) / (2*a)
            roots.append(root_2)

        elif d == 0:
            sqrt_D = sympy.sqrt(d)
            print(f"Корень дискриминанта равен {sqrt_D}")
            root = -b / (2*a)
            roots.append(root)

        else:
            roots = []

        return roots

