from urbanflow.city import City
from urbanflow.router import Router
from urbanflow.vehicle import Vehicle


def create_vehicle():

    city = City(
        adaptive_lights=True
    )

    city.generate_grid(
        rows=5,
        columns=5,
        spacing=100,
    )

    router = Router(city)

    start = city.intersections[0]

    destination = city.intersections[-1]

    route = router.find_route(
        start,
        destination,
    )

    return Vehicle(
        id=1,
        route=route,
        speed=40.0,
    )


def test_vehicle_has_route():

    vehicle = create_vehicle()

    assert vehicle.route

    assert len(
        vehicle.route
    ) > 0


def test_vehicle_has_current_road():

    vehicle = create_vehicle()

    assert (
        vehicle.current_road
        is not None
    )


def test_vehicle_has_position():

    vehicle = create_vehicle()

    x, y = (
        vehicle.get_position()
    )

    assert isinstance(
        x,
        float,
    )

    assert isinstance(
        y,
        float,
    )


def test_vehicle_moves():

    vehicle = create_vehicle()

    initial_progress = (
        vehicle.progress
    )

    vehicle.update(
        0.5
    )

    assert (
        vehicle.progress
        > initial_progress
    )


def test_vehicle_not_finished_initially():

    vehicle = create_vehicle()

    assert (
        vehicle.finished
        is False
    )
