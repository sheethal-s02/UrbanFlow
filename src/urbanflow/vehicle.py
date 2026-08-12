from dataclasses import dataclass, field


@dataclass
class Vehicle:

    id: int

    route: list

    speed: float = 40.0

    progress: float = 0.0

    route_index: int = 0

    finished: bool = False

    # ========================================================
    # DYNAMIC ROUTING
    # ========================================================

    reroute_timer: float = 0.0

    reroute_interval: float = 5.0

    reroutes: int = 0

    # ========================================================
    # CURRENT ROAD
    # ========================================================

    @property
    def current_road(self):

        if self.finished:

            return None

        if not self.route:

            return None

        if (
            self.route_index
            >= len(self.route)
        ):

            return None

        return self.route[
            self.route_index
        ]

    # ========================================================
    # UPDATE
    # ========================================================

    def update(
        self,
        dt: float,
    ) -> None:

        if self.finished:

            return

        road = self.current_road

        if road is None:

            self.finished = True

            return

        # ----------------------------------------------------
        # Move along current road
        # ----------------------------------------------------

        distance = (
            self.speed * dt
        )

        road_length = (
            self.get_road_length()
        )

        self.progress += distance

        # ----------------------------------------------------
        # Reached end of road
        # ----------------------------------------------------

        while (
            self.progress
            >= road_length
        ):

            self.progress -= road_length

            self.route_index += 1

            # ------------------------------------------------
            # Destination reached
            # ------------------------------------------------

            if (
                self.route_index
                >= len(self.route)
            ):

                self.finished = True

                self.progress = 0.0

                return

            road = self.current_road

            if road is None:

                self.finished = True

                return

            road_length = (
                self.get_road_length()
            )

    # ========================================================
    # REROUTING TIMER
    # ========================================================

    def update_reroute_timer(
        self,
        dt: float,
    ) -> bool:

        if self.finished:

            return False

        self.reroute_timer += dt

        if (
            self.reroute_timer
            >= self.reroute_interval
        ):

            self.reroute_timer = 0.0

            return True

        return False

    # ========================================================
    # APPLY NEW ROUTE
    # ========================================================

    def apply_new_route(
        self,
        new_route: list,
    ) -> bool:

        if not new_route:

            return False

        current_road = (
            self.current_road
        )

        # ----------------------------------------------------
        # Find the current road inside
        # the new route.
        # ----------------------------------------------------

        start_index = 0

        if current_road is not None:

            for index, road in enumerate(
                new_route
            ):

                if road.id == current_road.id:

                    start_index = index

                    break

        # ----------------------------------------------------
        # Keep current road if possible.
        # ----------------------------------------------------

        self.route = new_route[
            start_index:
        ]

        self.route_index = 0

        self.reroutes += 1

        return True

    # ========================================================
    # ROAD LENGTH
    # ========================================================

    def get_road_length(
        self,
    ) -> float:

        road = self.current_road

        if road is None:

            return 0.0

        return road.get_length()

    # ========================================================
    # POSITION
    # ========================================================

    def get_position(
        self,
    ) -> tuple[float, float]:

        road = self.current_road

        if road is None:

            return (
                0.0,
                0.0,
            )

        road_length = (
            self.get_road_length()
        )

        if road_length <= 0:

            return (
                road.start.x,
                road.start.y,
            )

        ratio = (
            self.progress
            / road_length
        )

        x = (
            road.start.x
            + (
                road.end.x
                - road.start.x
            )
            * ratio
        )

        y = (
            road.start.y
            + (
                road.end.y
                - road.start.y
            )
            * ratio
        )

        return (
            x,
            y,
        )