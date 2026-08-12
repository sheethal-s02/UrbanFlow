import pygame
import config

from src.urbanflow.city import City
from src.urbanflow.simulation import Simulation
from src.urbanflow.experiment import ExperimentRunner


WIDTH = 800
HEIGHT = 600

BACKGROUND = (30, 30, 30)
ROAD_COLOR = (80, 80, 80)
INTERSECTION_COLOR = (220, 220, 220)

RED = (220, 50, 50)
GREEN = (50, 220, 80)
WHITE = (240, 240, 240)

PANEL = (20, 20, 20)

HEAT_LOW = (50, 200, 80)
HEAT_MODERATE = (220, 220, 50)
HEAT_HEAVY = (240, 140, 40)
HEAT_SEVERE = (230, 50, 50)

VEHICLE_COLORS = [
    (220, 60, 60),
    (60, 180, 80),
    (60, 120, 220),
    (220, 180, 50),
    (180, 70, 200),
]


# ============================================================
# CREATE SIMULATION
# ============================================================

def create_simulation() -> Simulation:

    city = City(
        adaptive_lights=True
    )

    city.generate_grid(
    rows=config.CITY_ROWS,
    columns=config.CITY_COLUMNS,
    spacing=config.ROAD_SPACING,
)

    return Simulation(
    city,
    traffic_generation=True,
    seed=config.DEFAULT_RANDOM_SEED,
)


# ============================================================
# DRAW CITY
# ============================================================

def draw_city(
    screen,
    city,
) -> None:

    for road in city.roads:

        start = (
            int(road.start.x),
            int(road.start.y),
        )

        end = (
            int(road.end.x),
            int(road.end.y),
        )

        pygame.draw.line(
            screen,
            ROAD_COLOR,
            start,
            end,
            12,
        )

    for intersection in city.intersections:

        pygame.draw.circle(
            screen,
            INTERSECTION_COLOR,
            (
                int(intersection.x),
                int(intersection.y),
            ),
            6,
        )


# ============================================================
# HEATMAP
# ============================================================

def get_heat_color(
    vehicle_count: int,
):

    if vehicle_count == 0:
        return HEAT_LOW

    if vehicle_count <= 2:
        return HEAT_MODERATE

    if vehicle_count <= 4:
        return HEAT_HEAVY

    return HEAT_SEVERE


def draw_heatmap(
    screen,
    simulation,
) -> None:

    analytics = simulation.analytics

    for intersection in simulation.city.intersections:

        count = (
            analytics
            .get_intersection_congestion(
                simulation,
                intersection,
            )
        )

        pygame.draw.circle(
            screen,
            get_heat_color(count),
            (
                int(intersection.x),
                int(intersection.y),
            ),
            15,
            3,
        )


# ============================================================
# BOTTLENECK
# ============================================================

def draw_bottleneck(
    screen,
    simulation,
) -> None:

    (
        intersection,
        vehicle_count,
        level,
    ) = (
        simulation.analytics
        .get_worst_intersection(
            simulation
        )
    )

    if intersection is None:
        return

    pygame.draw.circle(
        screen,
        WHITE,
        (
            int(intersection.x),
            int(intersection.y),
        ),
        22,
        3,
    )


# ============================================================
# TRAFFIC LIGHTS
# ============================================================

def draw_traffic_lights(
    screen,
    city,
) -> None:

    for intersection in city.intersections:

        light = city.get_traffic_light(
            intersection
        )

        x = int(intersection.x)
        y = int(intersection.y)

        pygame.draw.circle(
            screen,
            (
                GREEN
                if light.allows_horizontal()
                else RED
            ),
            (
                x - 10,
                y - 10,
            ),
            5,
        )

        pygame.draw.circle(
            screen,
            (
                GREEN
                if light.allows_vertical()
                else RED
            ),
            (
                x + 10,
                y + 10,
            ),
            5,
        )


# ============================================================
# VEHICLES
# ============================================================

def draw_vehicles(
    screen,
    simulation,
) -> None:

    for index, vehicle in enumerate(
        simulation.vehicles
    ):

        if vehicle.finished:
            continue

        x, y = vehicle.get_position()

        color = VEHICLE_COLORS[
            index % len(VEHICLE_COLORS)
        ]

        pygame.draw.circle(
            screen,
            color,
            (
                int(x),
                int(y),
            ),
            8,
        )


# ============================================================
# DASHBOARD
# ============================================================

def draw_dashboard(
    screen,
    simulation,
    paused,
    simulation_speed,
    experiment_status,
) -> None:

    font = pygame.font.Font(
        None,
        22,
    )

    small_font = pygame.font.Font(
        None,
        17,
    )

    analytics = simulation.analytics

    active = analytics.get_active_vehicles(
        simulation
    )

    stopped = analytics.get_stopped_vehicles(
        simulation
    )

    average_speed = analytics.get_average_speed(
        simulation
    )

    congestion = analytics.get_congestion(
        simulation
    )

    horizontal, vertical = (
        analytics.get_total_demand(
            simulation
        )
    )

    total_reroutes = sum(
        vehicle.reroutes
        for vehicle in simulation.vehicles
    )

    (
        worst_intersection,
        worst_count,
        worst_level,
    ) = analytics.get_worst_intersection(
        simulation
    )

    period = "Unknown"

    if simulation.traffic_generator is not None:

        period = (
            simulation
            .traffic_generator
            .get_period(
                simulation.time
            )
        )

    width = 300
    height = 430

    x = WIDTH - width - 15
    y = HEIGHT - height - 15

    pygame.draw.rect(
        screen,
        PANEL,
        (
            x,
            y,
            width,
            height,
        ),
    )

    title = font.render(
        "URBANFLOW",
        True,
        WHITE,
    )

    screen.blit(
        title,
        (
            x + 15,
            y + 10,
        ),
    )

    state = (
        "PAUSED"
        if paused
        else "RUNNING"
    )

    metrics = [
        f"State: {state}",
        f"Speed: {simulation_speed:.1f}x",
        f"Traffic: {period}",
        f"Active vehicles: {active}",
        f"Stopped vehicles: {stopped}",
        f"Average speed: {average_speed:.1f}",
        f"Congestion: {congestion:.1f}%",
        f"Horizontal demand: {horizontal}",
        f"Vertical demand: {vertical}",
        f"Reroutes: {total_reroutes}",
        f"Time: {simulation.time:.1f}s",
    ]

    text_y = y + 48

    for metric in metrics:

        text = small_font.render(
            metric,
            True,
            WHITE,
        )

        screen.blit(
            text,
            (
                x + 15,
                text_y,
            ),
        )

        text_y += 19

    text_y += 3

    if worst_intersection is not None:

        text = small_font.render(
            "BOTTLENECK",
            True,
            WHITE,
        )

        screen.blit(
            text,
            (
                x + 15,
                text_y,
            ),
        )

        text_y += 20

        lines = [
            f"Intersection: #{worst_intersection.id}",
            f"Vehicles: {worst_count}",
            f"Level: {worst_level}",
        ]

        for line in lines:

            text = small_font.render(
                line,
                True,
                WHITE,
            )

            screen.blit(
                text,
                (
                    x + 15,
                    text_y,
                ),
            )

            text_y += 19

    text_y += 3

    text = small_font.render(
        experiment_status,
        True,
        WHITE,
    )

    screen.blit(
        text,
        (
            x + 15,
            text_y,
        ),
    )

    controls = small_font.render(
        "SPACE Pause  1/2/5 Speed  R Reset  E Benchmark",
        True,
        WHITE,
    )

    screen.blit(
        controls,
        (
            x + 15,
            y + height - 32,
        ),
    )


# ============================================================
# LEGEND
# ============================================================

def draw_legend(
    screen,
) -> None:

    font = pygame.font.Font(
        None,
        17,
    )

    items = [
        ("LOW", HEAT_LOW),
        ("MODERATE", HEAT_MODERATE),
        ("HEAVY", HEAT_HEAVY),
        ("SEVERE", HEAT_SEVERE),
    ]

    x = WIDTH - 180
    y = 20

    for label, color in items:

        pygame.draw.circle(
            screen,
            color,
            (
                x,
                y + 5,
            ),
            6,
        )

        text = font.render(
            label,
            True,
            WHITE,
        )

        screen.blit(
            text,
            (
                x + 12,
                y,
            ),
        )

        y += 24


# ============================================================
# PRINT BENCHMARK RESULTS
# ============================================================

def print_benchmark_results(
    fixed_results,
    adaptive_results,
    summary,
) -> None:

    print()
    print()
    print("=" * 72)
    print("URBANFLOW REPRODUCIBLE BENCHMARK")
    print("=" * 72)

    print()
    print(
        f"{'Seed':<8}"
        f"{'Fixed Wait':>15}"
        f"{'Adaptive Wait':>18}"
    )

    print("-" * 72)

    for fixed, adaptive in zip(
        fixed_results,
        adaptive_results,
    ):

        print(
            f"{fixed.seed:<8}"
            f"{fixed.average_wait_time:>15.2f}"
            f"{adaptive.average_wait_time:>18.2f}"
        )

    print()
    print("=" * 72)
    print("AVERAGE RESULTS")
    print("=" * 72)

    print()

    print(
        f"Fixed average wait:      "
        f"{summary.fixed_wait_mean:.2f}s "
        f"+/- {summary.fixed_wait_std:.2f}"
    )

    print(
        f"Adaptive average wait:   "
        f"{summary.adaptive_wait_mean:.2f}s "
        f"+/- {summary.adaptive_wait_std:.2f}"
    )

    print()

    print(
        f"Fixed average speed:     "
        f"{summary.fixed_speed_mean:.2f}"
    )

    print(
        f"Adaptive average speed:  "
        f"{summary.adaptive_speed_mean:.2f}"
    )

    print()

    print(
        f"Fixed throughput:        "
        f"{summary.fixed_throughput_mean:.4f}"
    )

    print(
        f"Adaptive throughput:     "
        f"{summary.adaptive_throughput_mean:.4f}"
    )

    print()
    print("-" * 72)

    print(
        f"Waiting-time improvement: "
        f"{summary.wait_improvement:.2f}%"
    )

    print(
        f"Speed improvement:         "
        f"{summary.speed_improvement:.2f}%"
    )

    print(
        f"Throughput improvement:    "
        f"{summary.throughput_improvement:.2f}%"
    )

    print("=" * 72)
    print()


# ============================================================
# MAIN
# ============================================================

def main() -> None:

    pygame.init()

    screen = pygame.display.set_mode(
        (
            WIDTH,
            HEIGHT,
        )
    )

    pygame.display.set_caption(
        "UrbanFlow - Traffic Optimization Lab"
    )

    clock = pygame.time.Clock()

    simulation = create_simulation()

    paused = False

    simulation_speed = 1.0

    experiment_status = (
        "E = Run 10-seed benchmark"
    )

    running = True

    print()
    print("=" * 55)
    print("URBANFLOW")
    print("=" * 55)

    print(
        f"Intersections: "
        f"{len(simulation.city.intersections)}"
    )

    print(
        f"Roads: "
        f"{len(simulation.city.roads)}"
    )

    print(
        "Adaptive traffic lights: ON"
    )

    print(
        "Traffic-aware routing: ON"
    )

    print(
        "Reproducible benchmark: ON"
    )

    print()
    print("CONTROLS")
    print("SPACE = Pause / Resume")
    print("1 = 1x")
    print("2 = 2x")
    print("5 = 5x")
    print("R = Reset")
    print("E = Run 10-seed benchmark")
    print("ESC = Exit")
    print()

    while running:

        real_dt = (
            clock.tick(60)
            / 1000.0
        )

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                running = False

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    running = False

                elif event.key == pygame.K_SPACE:

                    paused = not paused

                elif event.key == pygame.K_1:

                    simulation_speed = 1.0

                elif event.key == pygame.K_2:

                    simulation_speed = 2.0

                elif event.key == pygame.K_5:

                    simulation_speed = 5.0

                elif event.key == pygame.K_r:

                    simulation = (
                        create_simulation()
                    )

                    paused = False

                    experiment_status = (
                        "E = Run 10-seed benchmark"
                    )

                elif event.key == pygame.K_e:

                    experiment_status = (
                        "Running 10 benchmarks..."
                    )

                    pygame.display.flip()

                    print()
                    print(
                        "Starting reproducible "
                        "10-seed benchmark..."
                    )

                    runner = ExperimentRunner(
                        duration=180.0,
                        seeds=list(
                            range(1, 11)
                        ),
                    )

                    (
                        fixed_results,
                        adaptive_results,
                        summary,
                    ) = runner.benchmark()

                    print_benchmark_results(
                        fixed_results,
                        adaptive_results,
                        summary,
                    )

                    experiment_status = (
                        "Benchmark complete"
                    )

        if not paused:

            simulation.update(
                real_dt
                * simulation_speed
            )

        screen.fill(
            BACKGROUND
        )

        draw_city(
            screen,
            simulation.city,
        )

        draw_heatmap(
            screen,
            simulation,
        )

        draw_bottleneck(
            screen,
            simulation,
        )

        draw_traffic_lights(
            screen,
            simulation.city,
        )

        draw_vehicles(
            screen,
            simulation,
        )

        draw_legend(
            screen,
        )

        draw_dashboard(
            screen,
            simulation,
            paused,
            simulation_speed,
            experiment_status,
        )

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()