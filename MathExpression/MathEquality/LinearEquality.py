from MathExpression.MathRelation import MathRelation
import sympy


class LinearEquality(MathRelation):
    """Класс решения псевдо-линейных уравнений."""

    def solving_linear_equation(self):
        """Решение линейного уравнения."""

        if self.left_side != sympy.powsimp(self.left_side) or self.right_side != sympy.powsimp(self.right_side):
            print("Сокращаем обе стороны:")
            self.reduction()
            print("  ", self)

        if self.right_side.subs(self.var, 0) != self.right_side:
            print(f"Переносим члены, содержащие переменную {self.var}, влево:")
            self.left_side = sympy.powsimp(self.left_side - (self.right_side - self.right_side.subs(self.var, 0)))
            self.right_side = self.right_side.subs(self.var, 0)
            print("  ", self)

        if self.left_side.subs(self.var, 0) != 0:
            print(f"Переносим члены, не содержащие переменную {self.var}, вправо:")
            self.right_side = sympy.powsimp(self.right_side - self.left_side.subs(self.var, 0))
            self.left_side = sympy.powsimp(self.left_side - self.left_side.subs(self.var, 0))
            print("  ", self)

        divisor = self.left_side.subs(self.var, 1)
        if divisor != 1:
            print(f"Делим обе стороны на {divisor}:")
            self.right_side /= divisor
            self.left_side /= divisor
            print("  ", self)

        return self.right_side

