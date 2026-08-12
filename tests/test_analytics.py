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


def test_average_speed_is_non_negative():

    simulation = (
        create_simulation()
    )

    for _ in range(10):

        simulation.update(
            0.1
        )

    speed = (
        simulation.analytics
        .get_average_speed(
            simulation
        )
    )

    assert speed >= 0.0


def test_congestion_is_non_negative():

    simulation = (
        create_simulation()
    )

    for _ in range(10):

        simulation.update(
            0.1
        )

    congestion = (
        simulation.analytics
        .get_congestion(
            simulation
        )
    )

    assert congestion >= 0.0


def test_throughput_is_non_negative():

    simulation = (
        create_simulation()
    )

    for _ in range(10):

        simulation.update(
            0.1
        )

    throughput = (
        simulation.analytics
        .get_throughput(
            simulation
        )
    )

    assert throughput >= 0.0


def test_wait_time_is_non_negative():

    simulation = (
        create_simulation()
    )

    for _ in range(10):

        simulation.update(
            0.1
        )

    wait_time = (
        simulation.analytics
        .get_average_wait_time(
            simulation
        )
    )

    assert wait_time >= 0.0
