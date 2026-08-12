from urbanflow.city import City
from urbanflow.router import Router


def create_test_city():

    city = City(
        adaptive_lights=True
    )

    city.generate_grid(
        rows=5,
        columns=5,
        spacing=100,
    )

    return city


def test_city_has_intersections():

    city = create_test_city()

    assert len(
        city.intersections
    ) == 25


def test_city_has_roads():

    city = create_test_city()

    # The current UrbanFlow network creates
    # two directed roads for each connection.
    assert len(
        city.roads
    ) == 80


def test_router_finds_route():

    city = create_test_city()

    router = Router(city)

    start = city.intersections[0]

    destination = city.intersections[-1]

    route = router.find_route(
        start,
        destination,
    )

    assert route

    assert len(route) > 0


def test_route_reaches_destination():

    city = create_test_city()

    router = Router(city)

    start = city.intersections[0]

    destination = city.intersections[-1]

    route = router.find_route(
        start,
        destination,
    )

    assert route[-1].end == destination