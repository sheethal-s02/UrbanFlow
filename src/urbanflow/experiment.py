from dataclasses import dataclass
import statistics

from .city import City
from .simulation import Simulation


@dataclass
class ExperimentResult:

    adaptive_lights: bool

    seed: int

    duration: float

    average_speed: float

    average_wait_time: float

    completed_trips: int

    throughput: float

    maximum_congestion: int

    total_reroutes: int


@dataclass
class BenchmarkSummary:

    fixed_wait_mean: float
    fixed_wait_std: float

    adaptive_wait_mean: float
    adaptive_wait_std: float

    fixed_speed_mean: float
    fixed_speed_std: float

    adaptive_speed_mean: float
    adaptive_speed_std: float

    fixed_throughput_mean: float
    adaptive_throughput_mean: float

    wait_improvement: float
    speed_improvement: float
    throughput_improvement: float


class ExperimentRunner:

    def __init__(
        self,
        duration: float = 180.0,
        seeds: list[int] | None = None,
    ) -> None:

        self.duration = duration

        if seeds is None:

            self.seeds = list(
                range(1, 11)
            )

        else:

            self.seeds = seeds

    # ========================================================
    # CREATE SIMULATION
    # ========================================================

    def _create_simulation(
        self,
        adaptive_lights: bool,
        seed: int,
    ) -> Simulation:

        city = City(
            adaptive_lights=adaptive_lights
        )

        city.generate_grid(
            rows=5,
            columns=5,
            spacing=100,
        )

        return Simulation(
            city,
            traffic_generation=True,
            seed=seed,
        )

    # ========================================================
    # RUN ONE EXPERIMENT
    # ========================================================

    def run(
        self,
        adaptive_lights: bool,
        seed: int,
    ) -> ExperimentResult:

        simulation = (
            self._create_simulation(
                adaptive_lights,
                seed,
            )
        )

        elapsed = 0.0

        dt = 1.0 / 30.0

        while elapsed < self.duration:

            simulation.update(dt)

            elapsed += dt

        total_reroutes = sum(
            vehicle.reroutes
            for vehicle
            in simulation.vehicles
        )

        return ExperimentResult(
            adaptive_lights=adaptive_lights,
            seed=seed,
            duration=simulation.time,
            average_speed=(
                simulation.analytics
                .get_average_speed(
                    simulation
                )
            ),
            average_wait_time=(
                simulation.analytics
                .get_average_wait_time(
                    simulation
                )
            ),
            completed_trips=(
                simulation.analytics
                .get_completed_trips(
                    simulation
                )
            ),
            throughput=(
                simulation.analytics
                .get_throughput(
                    simulation
                )
            ),
            maximum_congestion=(
                simulation.analytics
                .get_maximum_congestion()
            ),
            total_reroutes=(
                total_reroutes
            ),
        )

    # ========================================================
    # RUN BENCHMARK
    # ========================================================

    def benchmark(
        self,
    ) -> tuple[
        list[ExperimentResult],
        list[ExperimentResult],
        BenchmarkSummary,
    ]:

        fixed_results = []

        adaptive_results = []

        for seed in self.seeds:

            print(
                f"Running seed {seed}..."
            )

            fixed = self.run(
                adaptive_lights=False,
                seed=seed,
            )

            adaptive = self.run(
                adaptive_lights=True,
                seed=seed,
            )

            fixed_results.append(
                fixed
            )

            adaptive_results.append(
                adaptive
            )

        summary = (
            self._build_summary(
                fixed_results,
                adaptive_results,
            )
        )

        return (
            fixed_results,
            adaptive_results,
            summary,
        )

    # ========================================================
    # SUMMARY
    # ========================================================

    def _build_summary(
        self,
        fixed_results,
        adaptive_results,
    ) -> BenchmarkSummary:

        fixed_wait = [
            result.average_wait_time
            for result in fixed_results
        ]

        adaptive_wait = [
            result.average_wait_time
            for result in adaptive_results
        ]

        fixed_speed = [
            result.average_speed
            for result in fixed_results
        ]

        adaptive_speed = [
            result.average_speed
            for result in adaptive_results
        ]

        fixed_throughput = [
            result.throughput
            for result in fixed_results
        ]

        adaptive_throughput = [
            result.throughput
            for result in adaptive_results
        ]

        fixed_wait_mean = (
            statistics.mean(
                fixed_wait
            )
        )

        adaptive_wait_mean = (
            statistics.mean(
                adaptive_wait
            )
        )

        fixed_speed_mean = (
            statistics.mean(
                fixed_speed
            )
        )

        adaptive_speed_mean = (
            statistics.mean(
                adaptive_speed
            )
        )

        fixed_throughput_mean = (
            statistics.mean(
                fixed_throughput
            )
        )

        adaptive_throughput_mean = (
            statistics.mean(
                adaptive_throughput
            )
        )

        fixed_wait_std = (
            statistics.stdev(
                fixed_wait
            )
            if len(fixed_wait) > 1
            else 0.0
        )

        adaptive_wait_std = (
            statistics.stdev(
                adaptive_wait
            )
            if len(adaptive_wait) > 1
            else 0.0
        )

        fixed_speed_std = (
            statistics.stdev(
                fixed_speed
            )
            if len(fixed_speed) > 1
            else 0.0
        )

        adaptive_speed_std = (
            statistics.stdev(
                adaptive_speed
            )
            if len(adaptive_speed) > 1
            else 0.0
        )

        wait_improvement = (
            self._lower_is_better_improvement(
                fixed_wait_mean,
                adaptive_wait_mean,
            )
        )

        speed_improvement = (
            self._higher_is_better_improvement(
                fixed_speed_mean,
                adaptive_speed_mean,
            )
        )

        throughput_improvement = (
            self._higher_is_better_improvement(
                fixed_throughput_mean,
                adaptive_throughput_mean,
            )
        )

        return BenchmarkSummary(
            fixed_wait_mean=fixed_wait_mean,
            fixed_wait_std=fixed_wait_std,
            adaptive_wait_mean=adaptive_wait_mean,
            adaptive_wait_std=adaptive_wait_std,
            fixed_speed_mean=fixed_speed_mean,
            fixed_speed_std=fixed_speed_std,
            adaptive_speed_mean=adaptive_speed_mean,
            adaptive_speed_std=adaptive_speed_std,
            fixed_throughput_mean=fixed_throughput_mean,
            adaptive_throughput_mean=adaptive_throughput_mean,
            wait_improvement=wait_improvement,
            speed_improvement=speed_improvement,
            throughput_improvement=throughput_improvement,
        )

    # ========================================================
    # IMPROVEMENT
    # ========================================================

    @staticmethod
    def _higher_is_better_improvement(
        baseline: float,
        improved: float,
    ) -> float:

        if baseline == 0:

            return 0.0

        return (
            (
                improved
                - baseline
            )
            / baseline
            * 100.0
        )

    @staticmethod
    def _lower_is_better_improvement(
        baseline: float,
        improved: float,
    ) -> float:

        if baseline == 0:

            return 0.0

        return (
            (
                baseline
                - improved
            )
            / baseline
            * 100.0
        )