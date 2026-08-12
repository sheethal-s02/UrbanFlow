import csv
from pathlib import Path

import matplotlib.pyplot as plt

from src.urbanflow.experiment import ExperimentRunner


# ============================================================
# CONFIGURATION
# ============================================================

RESULTS_DIR = Path("results")

CSV_FILE = (
    RESULTS_DIR
    / "benchmark_results.csv"
)

WAIT_GRAPH = (
    RESULTS_DIR
    / "waiting_time_comparison.png"
)

SPEED_GRAPH = (
    RESULTS_DIR
    / "speed_comparison.png"
)

THROUGHPUT_GRAPH = (
    RESULTS_DIR
    / "throughput_comparison.png"
)

NUMBER_OF_SEEDS = 10

SIMULATION_DURATION = 180.0


# ============================================================
# SAVE CSV
# ============================================================

def save_results(
    fixed_results,
    adaptive_results,
) -> None:

    RESULTS_DIR.mkdir(
        exist_ok=True
    )

    with CSV_FILE.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "seed",

            "fixed_wait",
            "adaptive_wait",

            "fixed_speed",
            "adaptive_speed",

            "fixed_completed",
            "adaptive_completed",

            "fixed_throughput",
            "adaptive_throughput",

            "fixed_max_congestion",
            "adaptive_max_congestion",

            "fixed_reroutes",
            "adaptive_reroutes",
        ])

        for fixed, adaptive in zip(
            fixed_results,
            adaptive_results,
        ):

            writer.writerow([
                fixed.seed,

                f"{fixed.average_wait_time:.6f}",
                f"{adaptive.average_wait_time:.6f}",

                f"{fixed.average_speed:.6f}",
                f"{adaptive.average_speed:.6f}",

                fixed.completed_trips,
                adaptive.completed_trips,

                f"{fixed.throughput:.8f}",
                f"{adaptive.throughput:.8f}",

                fixed.maximum_congestion,
                adaptive.maximum_congestion,

                fixed.total_reroutes,
                adaptive.total_reroutes,
            ])

    print()
    print(
        f"CSV saved:"
    )

    print(
        f"  {CSV_FILE}"
    )


# ============================================================
# GRAPH 1 — WAITING TIME
# ============================================================

def create_waiting_time_graph(
    fixed_results,
    adaptive_results,
) -> None:

    seeds = [
        result.seed
        for result in fixed_results
    ]

    fixed_wait = [
        result.average_wait_time
        for result in fixed_results
    ]

    adaptive_wait = [
        result.average_wait_time
        for result in adaptive_results
    ]

    plt.figure(
        figsize=(10, 6)
    )

    plt.plot(
        seeds,
        fixed_wait,
        marker="o",
        label="Fixed lights",
    )

    plt.plot(
        seeds,
        adaptive_wait,
        marker="o",
        label="Adaptive lights",
    )

    plt.xlabel(
        "Traffic scenario seed"
    )

    plt.ylabel(
        "Average waiting time (s)"
    )

    plt.title(
        "UrbanFlow — Waiting Time Comparison"
    )

    plt.xticks(
        seeds
    )

    plt.legend()

    plt.grid(
        True,
        alpha=0.3,
    )

    plt.tight_layout()

    plt.savefig(
        WAIT_GRAPH,
        dpi=150,
    )

    plt.close()

    print(
        f"Graph saved: {WAIT_GRAPH}"
    )


# ============================================================
# GRAPH 2 — SPEED
# ============================================================

def create_speed_graph(
    fixed_results,
    adaptive_results,
) -> None:

    seeds = [
        result.seed
        for result in fixed_results
    ]

    fixed_speed = [
        result.average_speed
        for result in fixed_results
    ]

    adaptive_speed = [
        result.average_speed
        for result in adaptive_results
    ]

    plt.figure(
        figsize=(10, 6)
    )

    plt.plot(
        seeds,
        fixed_speed,
        marker="o",
        label="Fixed lights",
    )

    plt.plot(
        seeds,
        adaptive_speed,
        marker="o",
        label="Adaptive lights",
    )

    plt.xlabel(
        "Traffic scenario seed"
    )

    plt.ylabel(
        "Average speed"
    )

    plt.title(
        "UrbanFlow — Average Speed Comparison"
    )

    plt.xticks(
        seeds
    )

    plt.legend()

    plt.grid(
        True,
        alpha=0.3,
    )

    plt.tight_layout()

    plt.savefig(
        SPEED_GRAPH,
        dpi=150,
    )

    plt.close()

    print(
        f"Graph saved: {SPEED_GRAPH}"
    )


# ============================================================
# GRAPH 3 — THROUGHPUT
# ============================================================

def create_throughput_graph(
    fixed_results,
    adaptive_results,
) -> None:

    seeds = [
        result.seed
        for result in fixed_results
    ]

    fixed_throughput = [
        result.throughput
        for result in fixed_results
    ]

    adaptive_throughput = [
        result.throughput
        for result in adaptive_results
    ]

    plt.figure(
        figsize=(10, 6)
    )

    plt.plot(
        seeds,
        fixed_throughput,
        marker="o",
        label="Fixed lights",
    )

    plt.plot(
        seeds,
        adaptive_throughput,
        marker="o",
        label="Adaptive lights",
    )

    plt.xlabel(
        "Traffic scenario seed"
    )

    plt.ylabel(
        "Completed trips / second"
    )

    plt.title(
        "UrbanFlow — Traffic Throughput Comparison"
    )

    plt.xticks(
        seeds
    )

    plt.legend()

    plt.grid(
        True,
        alpha=0.3,
    )

    plt.tight_layout()

    plt.savefig(
        THROUGHPUT_GRAPH,
        dpi=150,
    )

    plt.close()

    print(
        f"Graph saved: {THROUGHPUT_GRAPH}"
    )


# ============================================================
# PRINT RESULTS
# ============================================================

def print_results(
    fixed_results,
    adaptive_results,
    summary,
) -> None:

    print()
    print("=" * 78)
    print("URBANFLOW — FINAL 180-SECOND BENCHMARK")
    print("=" * 78)

    print()

    print(
        f"{'Seed':<8}"
        f"{'Fixed Wait':>15}"
        f"{'Adaptive Wait':>18}"
        f"{'Fixed Speed':>15}"
        f"{'Adaptive Speed':>18}"
    )

    print("-" * 78)

    for fixed, adaptive in zip(
        fixed_results,
        adaptive_results,
    ):

        print(
            f"{fixed.seed:<8}"
            f"{fixed.average_wait_time:>15.2f}"
            f"{adaptive.average_wait_time:>18.2f}"
            f"{fixed.average_speed:>15.2f}"
            f"{adaptive.average_speed:>18.2f}"
        )

    print()
    print("=" * 78)
    print("FINAL AVERAGES")
    print("=" * 78)

    print()

    print(
        f"Fixed average wait:      "
        f"{summary.fixed_wait_mean:.2f}s"
    )

    print(
        f"Adaptive average wait:   "
        f"{summary.adaptive_wait_mean:.2f}s"
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
        f"{summary.fixed_throughput_mean:.6f}"
    )

    print(
        f"Adaptive throughput:     "
        f"{summary.adaptive_throughput_mean:.6f}"
    )

    print()
    print("=" * 78)
    print("IMPROVEMENT")
    print("=" * 78)

    print()

    print(
        f"Waiting time improvement: "
        f"{summary.wait_improvement:.2f}%"
    )

    print(
        f"Average speed improvement: "
        f"{summary.speed_improvement:.2f}%"
    )

    print(
        f"Throughput improvement: "
        f"{summary.throughput_improvement:.2f}%"
    )

    print()

    print(
        "Positive waiting-time improvement = less waiting."
    )

    print(
        "Positive speed/throughput improvement = better performance."
    )

    print()


# ============================================================
# MAIN
# ============================================================

def main():

    RESULTS_DIR.mkdir(
        exist_ok=True
    )

    print()
    print("=" * 78)
    print("URBANFLOW FINAL BENCHMARK")
    print("=" * 78)

    print()

    print(
        f"Traffic scenarios: "
        f"{NUMBER_OF_SEEDS}"
    )

    print(
        f"Simulation duration: "
        f"{SIMULATION_DURATION:.0f} seconds"
    )

    print(
        "Comparison: Fixed lights vs Adaptive lights"
    )

    print()

    runner = ExperimentRunner(
        duration=SIMULATION_DURATION,
        seeds=list(
            range(
                1,
                NUMBER_OF_SEEDS + 1,
            )
        ),
    )

    fixed_results = []

    adaptive_results = []

    # --------------------------------------------------------
    # RUN EXPERIMENTS
    # --------------------------------------------------------

    for seed in runner.seeds:

        print(
            f"[Seed {seed}/{NUMBER_OF_SEEDS}] "
            f"Running fixed lights...",
            flush=True,
        )

        fixed = runner.run(
            adaptive_lights=False,
            seed=seed,
        )

        print(
            f"[Seed {seed}/{NUMBER_OF_SEEDS}] "
            f"Running adaptive lights...",
            flush=True,
        )

        adaptive = runner.run(
            adaptive_lights=True,
            seed=seed,
        )

        fixed_results.append(
            fixed
        )

        adaptive_results.append(
            adaptive
        )

        print(
            f"[Seed {seed}/{NUMBER_OF_SEEDS}] "
            f"Complete.",
            flush=True,
        )

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    summary = runner._build_summary(
        fixed_results,
        adaptive_results,
    )

    # --------------------------------------------------------
    # SAVE DATA
    # --------------------------------------------------------

    save_results(
        fixed_results,
        adaptive_results,
    )

    # --------------------------------------------------------
    # CREATE GRAPHS
    # --------------------------------------------------------

    create_waiting_time_graph(
        fixed_results,
        adaptive_results,
    )

    create_speed_graph(
        fixed_results,
        adaptive_results,
    )

    create_throughput_graph(
        fixed_results,
        adaptive_results,
    )

    # --------------------------------------------------------
    # PRINT RESULTS
    # --------------------------------------------------------

    print_results(
        fixed_results,
        adaptive_results,
        summary,
    )

    print("=" * 78)
    print("FINAL BENCHMARK COMPLETE")
    print("=" * 78)

    print()

    print(
        "Files created:"
    )

    print(
        f"  {CSV_FILE}"
    )

    print(
        f"  {WAIT_GRAPH}"
    )

    print(
        f"  {SPEED_GRAPH}"
    )

    print(
        f"  {THROUGHPUT_GRAPH}"
    )

    print()


if __name__ == "__main__":

    main()