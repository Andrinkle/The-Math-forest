from MathExpression import *

y = MathExpression('x^2+1 = 0', 'x')
# y = MathExpression('6*(3*x)^2 = 23*(3*x)', 'x')
y.solving_expression()
y.print_stages()
print()
y.print_answer()
