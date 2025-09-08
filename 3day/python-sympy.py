from fractions import Fraction
import sympy

x = sympy.symbols('x')  # x를 기호로 지정
f = sympy.Eq(x*Fraction('2/5'), 1760) # (2/5) * x = 1760 방정식
result = sympy.solve(f)  # 방정식의 해를 구함(x=4400)
#print(result)  

remains = result[0] - 1760
print(remains)  # 2640