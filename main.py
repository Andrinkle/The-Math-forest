from MathExpression import *

# y = MathExpression('2*x^2 - 6*x = 4', 'x')
y = MathExpression('sin(x)-4 = 0', 'x')
y.solving_expression()
print()
y.print_stages()
print()
y.print_answer()
print()



# Начальная задача
#   3*x**2 = 4
# Произведём замену t = x**2
#   3*t = 4
# Делим обе стороны на 3
#   t = 4/3

# Ответ:
#   t = 4/3

#     Решим замену t = t_n, где t_n - корни
#     1) x**2 = 4/3
#        Возведём обе сторны в степень 1/2
#          x = sqrt(4/3)
#        Так как 2 - чётное, то
#          x = -sqrt(4/3)

# Ответ:
#   x = sqrt(4/3)
#   x = -sqrt(4/3)


