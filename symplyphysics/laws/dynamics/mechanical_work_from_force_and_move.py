from sympy import (Eq, solve)
from sympy.vector import Dot
from symplyphysics import (units, Quantity, Symbol, print_expression, angle_type, Vector,
    validate_input, validate_output)
from symplyphysics.core.coordinate_systems.coordinate_systems import CoordinateSystem, coordinates_transform

# Description
## Work is measured result of force applied. Mechanical work is the only reason for the object energy to be changed.
## Work is scalar value equal to force multiplied by movement and by cosine of angle between force and movement vectors.
## Law: A = F * S, where
## A is mechanical work
## F is force vector applied to object
## S is movement vector caused by this force
## * is a scalar multiplication of vectors (dot product)

work = Symbol("work", units.energy)
force = Symbol("force", units.force)
distance = Symbol("distance", units.length)

law = Eq(work, Dot(force, distance))


def print_law() -> str:
    return print_expression(law)


@validate_input(force_=force, distance_=distance, force_angle=angle_type, distance_angle=angle_type)
@validate_output(work)
def calculate_work(force_: Quantity, distance_: Quantity, force_angle: Quantity | float,
    distance_angle: Quantity | float) -> Quantity:
    result_work_expr = solve(law, work, dict=True)[0][work]
    coordinates_polar = CoordinateSystem(CoordinateSystem.System.CYLINDRICAL)
    coordinates_cartesian = coordinates_transform(coordinates_polar,
        CoordinateSystem.System.CARTESIAN)
    #HACK: sympy angles are always in radians
    force_angle_radians = force_angle.scale_factor if isinstance(force_angle,
        Quantity) else force_angle
    distance_angle_radians = distance_angle.scale_factor if isinstance(distance_angle,
        Quantity) else distance_angle
    # Convert to Cartesian coordinates as Dot product does not work properly for Cylindrical coordinates
    force_vector = Vector([force_, force_angle_radians], coordinates_polar)
    distance_vector = Vector([distance_, distance_angle_radians], coordinates_polar)
    force_vector_cartesian = force_vector.rebase(coordinates_cartesian)
    distance_vector_cartesian = distance_vector.rebase(coordinates_cartesian)
    force_vector_cartesian_sympy = force_vector_cartesian.to_sympy_vector()
    distance_vector_cartesian_sympy = distance_vector_cartesian.to_sympy_vector()
    result_expr = result_work_expr.subs({
        force: force_vector_cartesian_sympy,
        distance: distance_vector_cartesian_sympy
    }).doit()
    return Quantity(result_expr)
