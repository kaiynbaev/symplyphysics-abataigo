from collections import namedtuple
from pytest import approx, fixture, raises
from symplyphysics import (
    errors,
    units,
    convert_to,
    Quantity,
    SI,
)
from symplyphysics.laws.nuclear.buckling import geometric_buckling_for_uniform_slab as buckling


@fixture(name="test_args")
def test_args_fixture():
    slab_width = Quantity(200 * units.centimeter)
    Args = namedtuple("Args", ["A"])
    return Args(A=slab_width)


def test_basic_geometric_buckling(test_args):
    result = buckling.calculate_geometric_buckling_squared(test_args.A)
    assert SI.get_dimension_system().equivalent_dims(result.dimension, 1 / units.area)
    result_geometric_buckling = convert_to(result, 1 / units.centimeter**2).evalf(2)
    assert result_geometric_buckling == approx(0.000246, 0.01)


def test_bad_slab_width():
    Ab = Quantity(1 * units.coulomb)
    with raises(errors.UnitsError):
        buckling.calculate_geometric_buckling_squared(Ab)
    with raises(TypeError):
        buckling.calculate_geometric_buckling_squared(100)
