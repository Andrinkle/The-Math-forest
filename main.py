from MathExpression import *

y = MathExpression('2*x^2 - 6*x = 4', 'x')
y.solving_expression()
print()
y.print_stages()
print()
y.print_answer()
print()

# Начальная задача
#   x**2 = 4
# Заменяем x**2 на t
#   t = 4

# Ответ:
#   t = 4

#     Решим замену t = t_n, где t_n in [4]
#     1) x**2 = 4
#       ...

# Ответ:
#   x = -2
#   x = 2
