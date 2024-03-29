from sympy.physics.units import speed_of_light
from sympy import (Eq, solve)
from symplyphysics import (units, Quantity, Symbol, print_expression, dimensionless, validate_input,
    validate_output)

# Description
## Wavespeed differs in different medium. Electromagnetic wave propagation speed depends on refraction factor of medium.
## Commonly refraction factor also depends on wave frequency.

# Law: Vmedium = C / n, where
## Vmedium is speed of electromagnetic wave in medium,
## C is speed of light in vacuum (it is a fundamental constant),
## n is refraction factor of medium.

wave_speed_in_medium = Symbol("wave_speed_in_medium", units.velocity)
refraction_factor = Symbol("refraction_factor", dimensionless)

law = Eq(wave_speed_in_medium, speed_of_light / refraction_factor)


def print_law() -> str:
    return print_expression(law)


@validate_input(refraction_factor_=refraction_factor)
@validate_output(wave_speed_in_medium)
def calculate_wavespeed(refraction_factor_: float) -> Quantity:
    result_expr = solve(law, wave_speed_in_medium, dict=True)[0][wave_speed_in_medium]
    wavespeed_applied = result_expr.subs(refraction_factor, refraction_factor_)
    return Quantity(wavespeed_applied)
