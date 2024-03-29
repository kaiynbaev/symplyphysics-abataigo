from sympy import (Eq, solve)
from symplyphysics import (units, Quantity, Symbol, print_expression, validate_input,
    validate_output)

# Description
## Current flowing through the resistor is proportional to applied voltage and reversly proportional to impedance of that resistor
## Ohm's law: I = U / R
## Where I is the current flowing through element
## U - is voltage drop on this element
## R is impedance of this element

current = Symbol("current", units.current)
voltage = Symbol("voltage", units.voltage)
resistance = Symbol("resistance", units.impedance)

law = Eq(current, voltage / resistance)


def print_law() -> str:
    return print_expression(law)


@validate_input(voltage_=voltage, resistance_=resistance)
@validate_output(current)
def calculate_current(voltage_: Quantity, resistance_: Quantity) -> Quantity:
    result_current_expr = solve(law, current, dict=True)[0][current]
    result_expr = result_current_expr.subs({voltage: voltage_, resistance: resistance_})
    return Quantity(result_expr)
