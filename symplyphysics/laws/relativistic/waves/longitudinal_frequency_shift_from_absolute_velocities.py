from sympy import (Eq, solve, sqrt)
from sympy.physics.units import speed_of_light
from symplyphysics import (units, Quantity, Symbol, print_expression, validate_input,
    validate_output)

# Description
## General relativistic Doppler effect that is classical Doppler effect with relativistic coefficient. This law is not
## used for actual calculations because relativistic effects are not visible for acoustic waves. And for
## electromagnetic waves it is hard to define velocity relative to medium.
## This law is used to show the connection between classical and relativistic Doppler laws.

# Law: fo = fs * (1 - vo/v) / (1 + vs/v) * sqrt((1 - (vs/c)**2) / (1 - (vo/c)**2)), where
## fo is observed frequency,
## fs is source wave frequency,
## v is velocity of wave in this medium (speed of light for electromagnetic waves),
## vo is observer velocity (positive when moving away from source, negative when moving towards source),
## vs is source velocity (positive when moving away from observer, negative when moving towards observer),
## c is speed of light.

# Conditions:
## - Motion is in 1-D space.
## - System of coordinates is at rest with respect to the medium of the wave, or any coordinate system for electromagnetic wave
## in vacuum.
## - Medium is not moving - no wind.
## - Source and observer velocities are less or equal than wave velocity. Otherwise emitted waves are left behind the source or never
## reach the observer.
## - Source and observer are moving directly towards or away from each other (collinear motion).

# Note:
## Speed of light depends on medium, but in the law below we use a speed of light in vacuum constant. Use proper
## speed of light value for non-vacuum media.

# Note:
## I couldn't find the relativistic Doppler effect law with source and observer velocities and motion with angle to the line of sight
## between source and observer.

# Note:
## When wave velocity is getting close to speed of light, we are no longer having observer and source velocities, but relativistic relative
## velocity.

observed_frequency = Symbol("observed_frequency", units.frequency)
real_frequency = Symbol("real_frequency", units.frequency)
source_velocity = Symbol("source_velocity", units.velocity)
observer_velocity = Symbol("observer_velocity", units.velocity)
wave_velocity = Symbol("wave_velocity", units.velocity)

law = Eq(
    observed_frequency,
    real_frequency * (1 - observer_velocity / wave_velocity) /
    (1 + source_velocity / wave_velocity) * sqrt(
    (1 - (source_velocity / speed_of_light)**2) / (1 - (observer_velocity / speed_of_light)**2)))


def print_law() -> str:
    return print_expression(law)


@validate_input(real_frequency_=real_frequency,
    wave_velocity_=wave_velocity,
    source_velocity_=source_velocity,
    observer_velocity_=observer_velocity)
@validate_output(observed_frequency)
def calculate_observed_frequency(real_frequency_: Quantity, wave_velocity_: Quantity,
    source_velocity_: Quantity, observer_velocity_: Quantity) -> Quantity:

    result_expr = solve(law, observed_frequency, dict=True)[0][observed_frequency]
    frequency_applied = result_expr.subs({
        real_frequency: real_frequency_,
        wave_velocity: wave_velocity_,
        source_velocity: source_velocity_,
        observer_velocity: observer_velocity_
    })
    return Quantity(frequency_applied)
