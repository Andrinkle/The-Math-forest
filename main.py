from MathExpression import *

y = MathExpression('32*sin(x)**3 - sin(x)**2 = 0', 'x')
# y = MathExpression('32*sin(x)**3 - sin(x)**2 = 0', 'x')
# y = MathExpression('6*(3*x)^2 = 23*(3*x)', 'x')
y.solving_expression()
print()
y.print_stages()
print()
y.print_answer()
print()
