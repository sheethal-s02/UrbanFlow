import random

import config

from .city import City
from .router import Router
from .vehicle import Vehicle


class TrafficGenerator:

    def __init__(
        self,
        city: City,
        router: Router,
        max_vehicles: int = config.MAX_VEHICLES,
        seed: int | None = None,
    ) -> None:

        self.city = city

        self.router = router

        self.max_vehicles = max_vehicles

        self.timer = 0.0

        self.next_vehicle_id = 1

        self.random = random.Random(seed)

        self.seed = seed

    # ========================================================
    # UPDATE
    # ========================================================

    def update(
        self,
        dt: float,
        current_time: float,
        vehicles: list[Vehicle],
    ) -> None:

        self.timer += dt

        spawn_interval = (
            self.get_spawn_interval(
                current_time
            )
        )

        if self.timer < spawn_interval:
            return

        self.timer = 0.0

        active_vehicles = sum(
            not vehicle.finished
            for vehicle in vehicles
        )

        if active_vehicles >= self.max_vehicles:
            return

        vehicle = self._create_vehicle(
            current_time,
            vehicles,
        )

        if vehicle is not None:
            vehicles.append(vehicle)

    # ========================================================
    # TRAFFIC PATTERN
    # ========================================================

    def get_spawn_interval(
        self,
        current_time: float,
    ) -> float:

        if current_time < 30:

            return config.NIGHT_SPAWN_INTERVAL

        if current_time < 75:

            return (
                config.MORNING_RUSH_SPAWN_INTERVAL
            )

        if current_time < 120:

            return config.MIDDAY_SPAWN_INTERVAL

        if current_time < 165:

            return (
                config.EVENING_RUSH_SPAWN_INTERVAL
            )

        return config.DEFAULT_SPAWN_INTERVAL

    def get_period(
        self,
        current_time: float,
    ) -> str:

        if current_time < 30:

            return "Night"

        if current_time < 75:

            return "Morning Rush"

        if current_time < 120:

            return "Midday"

        if current_time < 165:

            return "Evening Rush"

        return "Night"

    # ========================================================
    # CREATE VEHICLE
    # ========================================================

    def _create_vehicle(
        self,
        current_time: float,
        vehicles: list[Vehicle],
    ) -> Vehicle | None:

        if len(self.city.zones) < 2:
            return None

        if 30 <= current_time < 75:

            start_zone = self._find_zone(
                "Residential"
            )

            destination_zone = (
                self._find_zone(
                    "Business"
                )
            )

        elif 120 <= current_time < 165:

            start_zone = self._find_zone(
                "Business"
            )

            destination_zone = (
                self._find_zone(
                    "Residential"
                )
            )

        else:

            start_zone = self.random.choice(
                self.city.zones
            )

            destination_zone = (
                self.random.choice(
                    self.city.zones
                )
            )

        if (
            start_zone is None
            or destination_zone is None
        ):

            return None

        if start_zone == destination_zone:
            return None

        start = (
            start_zone.choose_intersection()
        )

        destination = (
            destination_zone.choose_intersection()
        )

        route = (
            self.router
            .find_traffic_aware_route(
                start=start,
                destination=destination,
                vehicles=vehicles,
            )
        )

        if not route:
            return None

        vehicle = Vehicle(
            id=self.next_vehicle_id,
            route=route,
            speed=self.random.uniform(
                config.MIN_VEHICLE_SPEED,
                config.MAX_VEHICLE_SPEED,
            ),
        )

        self.next_vehicle_id += 1

        return vehicle

    # ========================================================
    # FIND ZONE
    # ========================================================

    def _find_zone(
        self,
        name: str,
    ):

        for zone in self.city.zones:

            if zone.name == name:
                return zone

        return None