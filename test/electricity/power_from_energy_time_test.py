from collections import namedtuple
from pytest import approx, fixture, raises

from symplyphysics import (
    units, convert_to, SI, errors
)
from symplyphysics.laws.electricity import power_from_energy_time as power_def
# How much power did the heater use if it is known that it gave off 20,000 joules
# of energy in 35 seconds? Consider that all energy consumed equals energy given up.
@fixture
def test_args():
    Q = units.Quantity('Q')
    SI.set_quantity_dimension(Q, units.energy)
    SI.set_quantity_scale_factor(Q, 20000 * units.joule)
    t = units.Quantity('t')
    SI.set_quantity_dimension(t, units.time)
    SI.set_quantity_scale_factor(t, 35 * units.second)
    Args = namedtuple('Args', ['Q', 't'])
    return Args(Q=Q, t=t)

def test_basic_power(test_args):
    result = power_def.calculate_power(test_args.Q, test_args.t)
    assert SI.get_dimension_system().equivalent_dims(result.dimension, units.power)
    result_power = convert_to(result, units.watt).subs(units.watt, 1).evalf(5)
    assert result_power == approx(571, 0.001)

def test_bad_energy(test_args):
    bQ = units.Quantity('bQ')
    SI.set_quantity_dimension(bQ, units.time)
    SI.set_quantity_scale_factor(bQ, 1 * units.second)

    with raises(errors.UnitsError):
        power_def.calculate_power(bQ, test_args.t)

    with raises(TypeError):
        power_def.calculate_power(100, test_args.t)

def test_bad_time(test_args):
    bt = units.Quantity('bt')
    SI.set_quantity_dimension(bt, units.energy)
    SI.set_quantity_scale_factor(bt, 1 * units.joules)

    with raises(errors.UnitsError):
        power_def.calculate_power(test_args.Q, bt)

    with raises(TypeError):
        power_def.calculate_power(test_args.Q, 100)