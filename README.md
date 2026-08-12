# UrbanFlow — Traffic City Simulator

UrbanFlow is a Python-based traffic-city simulator designed to explore
adaptive traffic signal control, congestion-aware routing, dynamic
vehicle behavior, and traffic optimization.

## Features

- 5 × 5 city intersection network
- 40-road traffic network
- Dynamic vehicle generation
- Traffic lights
- Adaptive traffic signal control
- Traffic-aware A* routing
- Dynamic vehicle rerouting
- Congestion detection
- Bottleneck identification
- Real-time simulation dashboard
- Reproducible benchmarking
- Fixed vs adaptive traffic-light experiments
- CSV experiment data
- Performance graphs

## Architecture

```text
UrbanFlow
│
├── City
│   ├── Intersections
│   ├── Roads
│   └── Traffic lights
│
├── Simulation
│   ├── Vehicles
│   ├── Traffic generation
│   ├── Movement
│   └── Dynamic rerouting
│
├── Intelligence
│   ├── Adaptive traffic lights
│   ├── Traffic-aware routing
│   └── Congestion analysis
│
└── Analytics
    ├── Waiting time
    ├── Average speed
    ├── Throughput
    └── Benchmarking