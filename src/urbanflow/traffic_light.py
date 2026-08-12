from dataclasses import dataclass


@dataclass
class TrafficLight:

    # ========================================================
    # TIMING PARAMETERS
    # ========================================================

    min_green_duration: float = 3.0
    normal_max_green_duration: float = 10.0
    pressure_max_green_duration: float = 16.0

    decision_interval: float = 0.5

    fixed_duration: float = 5.0

    # ========================================================
    # STATE
    # ========================================================

    timer: float = 0.0
    decision_timer: float = 0.0

    horizontal_green: bool = True

    # ========================================================
    # TRAFFIC DATA
    # ========================================================

    horizontal_demand: int = 0
    vertical_demand: int = 0

    # ========================================================
    # CONTROL MODE
    # ========================================================

    adaptive: bool = True

    # ========================================================
    # PRESSURE
    # ========================================================

    horizontal_pressure: float = 0.0
    vertical_pressure: float = 0.0

    # ========================================================
    # UPDATE
    # ========================================================

    def update(
        self,
        dt: float,
        horizontal_demand: int,
        vertical_demand: int,
    ) -> None:

        self.timer += dt
        self.decision_timer += dt

        self.horizontal_demand = (
            horizontal_demand
        )

        self.vertical_demand = (
            vertical_demand
        )

        # ----------------------------------------------------
        # Calculate traffic pressure
        # ----------------------------------------------------

        self.horizontal_pressure = (
            self._calculate_pressure(
                horizontal_demand
            )
        )

        self.vertical_pressure = (
            self._calculate_pressure(
                vertical_demand
            )
        )

        # ----------------------------------------------------
        # Fixed traffic lights
        # ----------------------------------------------------

        if not self.adaptive:

            if self.timer >= self.fixed_duration:

                self.switch_phase()

            return

        # ----------------------------------------------------
        # Don't make decisions too frequently
        # ----------------------------------------------------

        if (
            self.decision_timer
            < self.decision_interval
        ):

            return

        self.decision_timer = 0.0

        # ----------------------------------------------------
        # Protect minimum green time
        # ----------------------------------------------------

        if (
            self.timer
            < self.min_green_duration
        ):

            return

        # ----------------------------------------------------
        # Current / opposite pressure
        # ----------------------------------------------------

        if self.horizontal_green:

            current_pressure = (
                self.horizontal_pressure
            )

            opposite_pressure = (
                self.vertical_pressure
            )

        else:

            current_pressure = (
                self.vertical_pressure
            )

            opposite_pressure = (
                self.horizontal_pressure
            )

        # ----------------------------------------------------
        # Determine maximum green time
        # ----------------------------------------------------

        max_green = (
            self.normal_max_green_duration
        )

        # Heavy traffic allows the current phase
        # to stay green longer.

        if current_pressure >= 5:

            max_green = (
                self.pressure_max_green_duration
            )

        # ----------------------------------------------------
        # Severe pressure imbalance
        # ----------------------------------------------------

        if (
            opposite_pressure
            >= current_pressure + 3
        ):

            self.switch_phase()

            return

        # ----------------------------------------------------
        # Current direction has no traffic
        # ----------------------------------------------------

        if (
            current_pressure == 0
            and opposite_pressure > 0
        ):

            self.switch_phase()

            return

        # ----------------------------------------------------
        # Maximum green time reached
        # ----------------------------------------------------

        if self.timer >= max_green:

            self.switch_phase()

            return

        # ----------------------------------------------------
        # Moderate pressure imbalance
        # ----------------------------------------------------

        if (
            opposite_pressure
            >= current_pressure + 2
            and self.timer >= self.min_green_duration
        ):

            self.switch_phase()

    # ========================================================
    # PRESSURE CALCULATION
    # ========================================================

    def _calculate_pressure(
        self,
        demand: int,
    ) -> float:

        if demand <= 0:
            return 0.0

        # More vehicles = greater pressure.
        #
        # This can later be replaced with a more
        # sophisticated formula involving:
        #
        # queue length
        # waiting time
        # vehicle priority
        # road length

        return float(demand)

    # ========================================================
    # SWITCH PHASE
    # ========================================================

    def switch_phase(self) -> None:

        self.horizontal_green = (
            not self.horizontal_green
        )

        self.timer = 0.0

        self.decision_timer = 0.0

    # ========================================================
    # LIGHT STATE
    # ========================================================

    def allows_horizontal(self) -> bool:

        return self.horizontal_green

    def allows_vertical(self) -> bool:

        return not self.horizontal_green

    # ========================================================
    # STATE NAME
    # ========================================================

    def get_state(self) -> str:

        if self.horizontal_green:

            return "HORIZONTAL GREEN"

        return "VERTICAL GREEN"

    # ========================================================
    # CURRENT PRESSURE
    # ========================================================

    def get_current_pressure(self) -> float:

        if self.horizontal_green:

            return self.horizontal_pressure

        return self.vertical_pressure

    # ========================================================
    # OPPOSITE PRESSURE
    # ========================================================

    def get_opposite_pressure(self) -> float:

        if self.horizontal_green:

            return self.vertical_pressure

        return self.horizontal_pressure

    # ========================================================
    # PRESSURE DIFFERENCE
    # ========================================================

    def get_pressure_difference(self) -> float:

        return (
            self.get_opposite_pressure()
            - self.get_current_pressure()
        )