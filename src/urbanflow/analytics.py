class TrafficAnalytics:

    def __init__(self) -> None:

        self.total_vehicles_created = 0

        self.completed_trips = 0

        self.current_time = 0.0

        self.total_wait_time = 0.0

        self.maximum_congestion = 0

        # ----------------------------------------------------
        # Fair speed measurement
        #
        # We accumulate:
        #
        # speed × time
        #
        # and divide by:
        #
        # total vehicle-time
        #
        # This prevents vehicles that finish early from
        # disappearing from the speed calculation.
        # ----------------------------------------------------

        self.total_speed_time = 0.0

        self.total_vehicle_time = 0.0

    # ========================================================
    # UPDATE
    # ========================================================

    def update(
        self,
        simulation,
        dt: float,
    ) -> None:

        self.current_time += dt

        self.total_vehicles_created = (
            len(simulation.vehicles)
        )

        # ----------------------------------------------------
        # Vehicle-time and speed-time
        # ----------------------------------------------------

        for vehicle in simulation.vehicles:

            if vehicle.finished:

                continue

            self.total_vehicle_time += dt

            self.total_speed_time += (
                vehicle.speed * dt
            )

        # ----------------------------------------------------
        # Waiting time
        # ----------------------------------------------------

        stopped = (
            self.get_stopped_vehicles(
                simulation
            )
        )

        self.total_wait_time += (
            stopped * dt
        )

        # ----------------------------------------------------
        # Maximum congestion
        # ----------------------------------------------------

        current_max = 0

        for intersection in (
            simulation.city.intersections
        ):

            count = (
                self.get_intersection_congestion(
                    simulation,
                    intersection,
                )
            )

            current_max = max(
                current_max,
                count,
            )

        self.maximum_congestion = max(
            self.maximum_congestion,
            current_max,
        )

        # ----------------------------------------------------
        # Completed trips
        # ----------------------------------------------------

        self.completed_trips = sum(
            1
            for vehicle in simulation.vehicles
            if vehicle.finished
        )

    # ========================================================
    # ACTIVE VEHICLES
    # ========================================================

    def get_active_vehicles(
        self,
        simulation,
    ) -> int:

        return sum(
            not vehicle.finished
            for vehicle in simulation.vehicles
        )

    # ========================================================
    # STOPPED VEHICLES
    # ========================================================

    def get_stopped_vehicles(
        self,
        simulation,
    ) -> int:

        return sum(
            1
            for vehicle in simulation.vehicles
            if (
                not vehicle.finished
                and vehicle.speed < 1.0
            )
        )

    # ========================================================
    # AVERAGE SPEED
    # ========================================================

    def get_average_speed(
        self,
        simulation,
    ) -> float:

        if self.total_vehicle_time <= 0:

            return 0.0

        return (
            self.total_speed_time
            / self.total_vehicle_time
        )

    # ========================================================
    # CONGESTION
    # ========================================================

    def get_congestion(
        self,
        simulation,
    ) -> float:

        active = (
            self.get_active_vehicles(
                simulation
            )
        )

        if active == 0:

            return 0.0

        stopped = (
            self.get_stopped_vehicles(
                simulation
            )
        )

        return (
            stopped
            / active
            * 100.0
        )

    # ========================================================
    # AVERAGE WAIT TIME
    # ========================================================

    def get_average_wait_time(
        self,
        simulation,
    ) -> float:

        if self.total_vehicles_created <= 0:

            return 0.0

        return (
            self.total_wait_time
            / self.total_vehicles_created
        )

    # ========================================================
    # COMPLETED TRIPS
    # ========================================================

    def get_completed_trips(
        self,
        simulation,
    ) -> int:

        return self.completed_trips

    # ========================================================
    # THROUGHPUT
    # ========================================================

    def get_throughput(
        self,
        simulation,
    ) -> float:

        if self.current_time <= 0:

            return 0.0

        return (
            self.completed_trips
            / self.current_time
        )

    # ========================================================
    # MAXIMUM CONGESTION
    # ========================================================

    def get_maximum_congestion(
        self,
    ) -> int:

        return self.maximum_congestion

    # ========================================================
    # DEMAND
    # ========================================================

    def get_total_demand(
        self,
        simulation,
    ) -> tuple[int, int]:

        horizontal = 0
        vertical = 0

        for light in (
            simulation.city
            .traffic_lights
            .values()
        ):

            horizontal += (
                light.horizontal_demand
            )

            vertical += (
                light.vertical_demand
            )

        return (
            horizontal,
            vertical,
        )

    # ========================================================
    # INTERSECTION CONGESTION
    # ========================================================

    def get_intersection_congestion(
        self,
        simulation,
        intersection,
    ) -> int:

        congestion = 0

        for vehicle in simulation.vehicles:

            if vehicle.finished:

                continue

            road = vehicle.current_road

            if road is None:

                continue

            if road.end != intersection:

                continue

            distance = (
                vehicle.get_road_length()
                - vehicle.progress
            )

            if distance <= 100:

                congestion += 1

        return congestion

    # ========================================================
    # CONGESTION LEVEL
    # ========================================================

    def get_congestion_level(
        self,
        vehicle_count: int,
    ) -> str:

        if vehicle_count == 0:

            return "LOW"

        if vehicle_count <= 2:

            return "MODERATE"

        if vehicle_count <= 4:

            return "HEAVY"

        return "SEVERE"

    # ========================================================
    # WORST INTERSECTION
    # ========================================================

    def get_worst_intersection(
        self,
        simulation,
    ):

        worst_intersection = None

        worst_count = 0

        for intersection in (
            simulation.city.intersections
        ):

            count = (
                self.get_intersection_congestion(
                    simulation,
                    intersection,
                )
            )

            if count > worst_count:

                worst_count = count

                worst_intersection = (
                    intersection
                )

        if worst_intersection is None:

            return (
                None,
                0,
                "LOW",
            )

        level = (
            self.get_congestion_level(
                worst_count
            )
        )

        return (
            worst_intersection,
            worst_count,
            level,
        )