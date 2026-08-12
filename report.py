import csv
from pathlib import Path
import statistics


RESULTS_FILE = Path(
    "results/benchmark_results.csv"
)

REPORT_FILE = Path(
    "results/benchmark_report.txt"
)


def load_results():

    rows = []

    with RESULTS_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            rows.append({
                "seed": int(row["seed"]),

                "fixed_wait": float(
                    row["fixed_wait"]
                ),

                "adaptive_wait": float(
                    row["adaptive_wait"]
                ),

                "fixed_speed": float(
                    row["fixed_speed"]
                ),

                "adaptive_speed": float(
                    row["adaptive_speed"]
                ),

                "fixed_throughput": float(
                    row["fixed_throughput"]
                ),

                "adaptive_throughput": float(
                    row["adaptive_throughput"]
                ),

                "fixed_completed": int(
                    row["fixed_completed"]
                ),

                "adaptive_completed": int(
                    row["adaptive_completed"]
                ),
            })

    return rows


def mean(values):

    return statistics.mean(values)


def improvement_lower(
    baseline,
    improved,
):

    if baseline == 0:

        return 0.0

    return (
        (baseline - improved)
        / baseline
        * 100
    )


def improvement_higher(
    baseline,
    improved,
):

    if baseline == 0:

        return 0.0

    return (
        (improved - baseline)
        / baseline
        * 100
    )


def main():

    rows = load_results()

    fixed_wait = [
        row["fixed_wait"]
        for row in rows
    ]

    adaptive_wait = [
        row["adaptive_wait"]
        for row in rows
    ]

    fixed_speed = [
        row["fixed_speed"]
        for row in rows
    ]

    adaptive_speed = [
        row["adaptive_speed"]
        for row in rows
    ]

    fixed_throughput = [
        row["fixed_throughput"]
        for row in rows
    ]

    adaptive_throughput = [
        row["adaptive_throughput"]
        for row in rows
    ]

    fixed_completed = [
        row["fixed_completed"]
        for row in rows
    ]

    adaptive_completed = [
        row["adaptive_completed"]
        for row in rows
    ]

    fixed_wait_mean = mean(
        fixed_wait
    )

    adaptive_wait_mean = mean(
        adaptive_wait
    )

    fixed_speed_mean = mean(
        fixed_speed
    )

    adaptive_speed_mean = mean(
        adaptive_speed
    )

    fixed_throughput_mean = mean(
        fixed_throughput
    )

    adaptive_throughput_mean = mean(
        adaptive_throughput
    )

    fixed_completed_mean = mean(
        fixed_completed
    )

    adaptive_completed_mean = mean(
        adaptive_completed
    )

    wait_improvement = (
        improvement_lower(
            fixed_wait_mean,
            adaptive_wait_mean,
        )
    )

    speed_improvement = (
        improvement_higher(
            fixed_speed_mean,
            adaptive_speed_mean,
        )
    )

    throughput_improvement = (
        improvement_higher(
            fixed_throughput_mean,
            adaptive_throughput_mean,
        )
    )

    report = f"""
URBANFLOW
TRAFFIC OPTIMIZATION BENCHMARK REPORT
=====================================

EXPERIMENT
----------

Traffic scenarios: {len(rows)}
Comparison: Fixed traffic lights vs Adaptive traffic lights
Same random seeds used for both systems
Simulation duration: 180 seconds per scenario


AVERAGE RESULTS
---------------

                    FIXED        ADAPTIVE
Average wait        {fixed_wait_mean:.2f}       {adaptive_wait_mean:.2f}
Average speed       {fixed_speed_mean:.2f}       {adaptive_speed_mean:.2f}
Throughput          {fixed_throughput_mean:.6f}       {adaptive_throughput_mean:.6f}
Completed trips     {fixed_completed_mean:.2f}       {adaptive_completed_mean:.2f}


IMPROVEMENT
-----------

Waiting time improvement:
{wait_improvement:.2f}%

Average speed improvement:
{speed_improvement:.2f}%

Throughput improvement:
{throughput_improvement:.2f}%


INTERPRETATION
--------------

Adaptive traffic signals were evaluated against fixed-time
traffic signals under identical traffic scenarios.

Waiting time is better when lower.

Average speed and throughput are better when higher.

The benchmark uses multiple random seeds so that the result
does not depend on a single traffic scenario.


FILES
-----

Raw experiment data:
results/benchmark_results.csv

Waiting-time graph:
results/waiting_time_comparison.png

Speed graph:
results/speed_comparison.png

Throughput graph:
results/throughput_comparison.png
"""

    REPORT_FILE.write_text(
        report.strip(),
        encoding="utf-8",
    )

    print()
    print("=" * 60)
    print("URBANFLOW REPORT")
    print("=" * 60)

    print()

    print(
        f"Waiting time improvement: "
        f"{wait_improvement:.2f}%"
    )

    print(
        f"Average speed improvement: "
        f"{speed_improvement:.2f}%"
    )

    print(
        f"Throughput improvement: "
        f"{throughput_improvement:.2f}%"
    )

    print()

    print(
        f"Report saved to:"
    )

    print(
        f"  {REPORT_FILE}"
    )

    print()


if __name__ == "__main__":

    main()