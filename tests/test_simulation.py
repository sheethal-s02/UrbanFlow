from urbanflow.city import City
from urbanflow.simulation import Simulation


def create_simulation():

    city = City(
        adaptive_lights=True
    )

    city.generate_grid(
        rows=5,
        columns=5,
        spacing=100,
    )

    return Simulation(
        city,
        traffic_generation=True,
        seed=1,
    )


def test_simulation_starts():

    simulation = (
        create_simulation()
    )

    assert simulation.time == 0.0

    assert (
        simulation.city
        is not None
    )


def test_simulation_advances():

    simulation = (
        create_simulation()
    )

    simulation.update(
        1.0
    )

    assert (
        simulation.time
        > 0.0
    )


def test_simulation_generates_vehicles():

    simulation = (
        create_simulation()
    )

    for _ in range(10):

        simulation.update(
            1.0
        )

    assert len(
        simulation.vehicles
    ) > 0


def test_simulation_has_analytics():

    simulation = (
        create_simulation()
    )

    assert (
        simulation.analytics
        is not None
    )


def test_simulation_is_reproducible():

    simulation_a = (
        create_simulation()
    )

    simulation_b = (
        create_simulation()
    )

    for _ in range(20):

        simulation_a.update(
            0.1
        )

        simulation_b.update(
            0.1
        )

    assert len(
        simulation_a.vehicles
    ) == len(
        simulation_b.vehicles
    )
