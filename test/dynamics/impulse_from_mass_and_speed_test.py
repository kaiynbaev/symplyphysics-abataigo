from collections import namedtuple
from pytest import approx, fixture, raises
from symplyphysics import (
    errors,
    units,
    convert_to,
    Quantity,
    SI,
)
from symplyphysics.laws.dynamics import impulse_from_mass_and_speed as impulse

# Description
# Calculate the impulse of a bus 
# with a mass of 2000 kg and a speed of 10m/s

@fixture(name="test_args")
def test_args_fixture():
    m = Quantity(2000 * units.kilogram)
    v = Quantity(10 * units.meter / units.second)
    Args = namedtuple("Args", ["m", "v"])
    return Args(m=m, v=v)


def test_basic_impulse(test_args):
    result = impulse.calculate_impulse(test_args.v, test_args.m)
    assert SI.get_dimension_system().equivalent_dims(result.dimension, units.momentum)
    result_impulse = convert_to(result, units.kilogram * units.meter / units.second).evalf(3)
    assert result_impulse == approx(2_000*10, 0.1)

def test_bad_mass(test_args):
    v = Quantity(1 * units.meter)
    with raises(errors.UnitsError):
        impulse.calculate_impulse(v, test_args.m)
    with raises(TypeError):
        impulse.calculate_impulse(100, test_args.m)
    
def test_bad_velocity(test_args):
    m = Quantity(1 * units.meter)
    with raises(errors.UnitsError):
        impulse.calculate_impulse(test_args.v, m)
    with raises(TypeError):
        impulse.calculate_impulse(test_args.v, 100)