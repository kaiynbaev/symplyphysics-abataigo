from sympy import (Eq, solve)
from sympy.physics.units import Dimension
from sympy.physics.units import meter, kilogram, second
from symplyphysics import (units, Quantity, Symbol, print_expression, validate_input,
    validate_output)

# The momentum of a body is a vector quantity 
# equal to the product of the mass of a body and its velocity:
#               p = m * v
# There are no special pulse measurement units. 
# The momentum dimension is simply the conversion of the mass 
# dimension to the velocity dimension: (kg * m / s) == (m * v)

impulse = Symbol("impulse", units.momentum)
mass = Symbol("mass", units.mass)
velocity = Symbol("velocity", units.velocity)

law = Eq(impulse, mass * velocity)

def print_law() -> str:
    return print_expression(law)

@validate_input(v = velocity,  m = mass)
@validate_output(impulse)
def calculate_impulse(v: Quantity, m: Quantity):
    result_expr = solve(law, impulse, dict=True)[0][impulse]
    impulse_applied = result_expr.subs({mass : m, velocity : v})
    return Quantity(impulse_applied)

print(impulse, mass, law)