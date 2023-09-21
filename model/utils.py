import cmath
import math

def acosd(x):
    acos_result = cmath.acos(x)
    return complex(math.degrees(acos_result.real), math.degrees(acos_result.imag))
