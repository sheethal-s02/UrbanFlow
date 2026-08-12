from .analytics import TrafficAnalytics
from .city import City
from .router import Router
from .traffic_generator import TrafficGenerator
from .vehicle import Vehicle
import config


SAFE_DISTANCE = config.SAFE_DISTANCE

STOP_DISTANCE = config.STOP_DISTANCE

MAX_DECELERATION = (
    config.VEHICLE_MAX_DECELERATION
)

ACCELERATION = (
    config.VEHICLE_ACCELERATION
)

REROUTE_CONGESTION_THRESHOLD = (
    config.REROUTE_CONGESTION_THRESHOLD
)


class Simulation:

    def __init__(
        self,
        city: City,
        traffic_generation: bool = False,
        seed: int | None = None,
    ) -> None:

        self.city = city

        self.vehicles: list[
            Vehicle
        ] = []

        self.time = 0.0

        self.seed = seed

        self.analytics = (
            TrafficAnalytics()
        )

        # ----------------------------------------------------
        # Router
        # ----------------------------------------------------

        self.router = Router(
            city
        )

        # ----------------------------------------------------
        # Traffic generator
        # ----------------------------------------------------

        self.traffic_generator = None

        if traffic_generation:

            self.traffic_generator = (
                TrafficGenerator(
                    city=city,
                    router=self.router,
                    max_vehicles=100,
                    seed=seed,
                )
            )

    # ========================================================
    # ADD VEHICLE
    # ========================================================

    def add_vehicle(
        self,
        vehicle: Vehicle,
    ) -> None:

        self.vehicles.append(
            vehicle
        )

    # ========================================================
    # UPDATE
    # ========================================================

    def update(
        self,
        dt: float,
    ) -> None:

        self.time += dt

        # ----------------------------------------------------
        # Generate traffic
        # ----------------------------------------------------

        if (
            self.traffic_generator
            is not None
        ):

            self.traffic_generator.update(
                dt=dt,
                current_time=self.time,
                vehicles=self.vehicles,
            )

        # ----------------------------------------------------
        # Update traffic lights
        # ----------------------------------------------------

        self.city.update_traffic_lights(
            dt=dt,
            vehicles=self.vehicles,
        )

        # ----------------------------------------------------
        # Dynamic rerouting
        # ----------------------------------------------------

        self._update_routing(
            dt
        )

        # ----------------------------------------------------
        # Vehicle speeds
        # ----------------------------------------------------

        self._update_vehicle_speeds(
            dt
        )

        # ----------------------------------------------------
        # Move vehicles
        # ----------------------------------------------------

        for vehicle in self.vehicles:

            vehicle.update(dt)

        # ----------------------------------------------------
        # Analytics
        # ----------------------------------------------------

        self.analytics.update(
            simulation=self,
            dt=dt,
        )

    # ========================================================
    # DYNAMIC ROUTING
    # ========================================================

    def _update_routing(
        self,
        dt: float,
    ) -> None:

        for vehicle in self.vehicles:

            if vehicle.finished:

                continue

            should_reroute = (
                vehicle
                .update_reroute_timer(
                    dt
                )
            )

            if not should_reroute:

                continue

            current_road = (
                vehicle.current_road
            )

            if current_road is None:

                continue

            congestion = (
                self._get_road_congestion(
                    current_road
                )
            )

            if (
                congestion
                < REROUTE_CONGESTION_THRESHOLD
            ):

                continue

            destination = (
                vehicle.route[-1].end
            )

            new_route = (
                self.router
                .find_traffic_aware_route(
                    start=current_road.end,
                    destination=destination,
                    vehicles=self.vehicles,
                )
            )

            if not new_route:

                continue

            if self._routes_are_same(
                vehicle.route[
                    vehicle.route_index + 1:
                ],
                new_route,
            ):

                continue

            vehicle.apply_new_route(
                new_route
            )

    # ========================================================
    # ROAD CONGESTION
    # ========================================================

    def _get_road_congestion(
        self,
        road,
    ) -> int:

        count = 0

        for vehicle in self.vehicles:

            if vehicle.finished:

                continue

            if (
                vehicle.current_road
                == road
            ):

                count += 1

        return count

    # ========================================================
    # ROUTE COMPARISON
    # ========================================================

    def _routes_are_same(
        self,
        route_a,
        route_b,
    ) -> bool:

        if len(route_a) != len(route_b):

            return False

        for road_a, road_b in zip(
            route_a,
            route_b,
        ):

            if road_a.id != road_b.id:

                return False

        return True

    # ========================================================
    # VEHICLE SPEED CONTROL
    # ========================================================

    def _update_vehicle_speeds(
        self,
        dt: float,
    ) -> None:

        for vehicle in self.vehicles:

            if vehicle.finished:

                vehicle.speed = 0.0

                continue

            if self._red_light_ahead(
                vehicle
            ):

                vehicle.speed = (
                    self._brake(
                        vehicle,
                        dt,
                    )
                )

                continue

            vehicle_ahead = (
                self._find_vehicle_ahead(
                    vehicle
                )
            )

            if vehicle_ahead is None:

                self._accelerate(
                    vehicle,
                    dt,
                )

                continue

            distance = (
                self._distance_to_vehicle(
                    vehicle,
                    vehicle_ahead,
                )
            )

            if (
                distance
                <= SAFE_DISTANCE
            ):

                vehicle.speed = max(
                    0.0,
                    vehicle.speed
                    - (
                        MAX_DECELERATION
                        * dt
                    ),
                )

            elif (
                distance
                <= SAFE_DISTANCE * 2
            ):

                vehicle.speed = max(
                    0.0,
                    vehicle.speed
                    - (
                        MAX_DECELERATION
                        * 0.5
                        * dt
                    ),
                )

            else:

                self._accelerate(
                    vehicle,
                    dt,
                )

    # ========================================================
    # ACCELERATION
    # ========================================================

    def _accelerate(
        self,
        vehicle: Vehicle,
        dt: float,
    ) -> None:

        road_speed = (
            vehicle.current_road
            .speed_limit
        )

        vehicle.speed = min(
            road_speed,
            vehicle.speed
            + (
                ACCELERATION
                * dt
            ),
        )

    # ========================================================
    # BRAKING
    # ========================================================

    def _brake(
        self,
        vehicle: Vehicle,
        dt: float,
    ) -> float:

        return max(
            0.0,
            vehicle.speed
            - (
                MAX_DECELERATION
                * dt
            ),
        )

    # ========================================================
    # RED LIGHT
    # ========================================================

    def _red_light_ahead(
        self,
        vehicle: Vehicle,
    ) -> bool:

        road = vehicle.current_road

        if road is None:

            return False

        distance = (
            vehicle.get_road_length()
            - vehicle.progress
        )

        if distance > STOP_DISTANCE:

            return False

        light = (
            self.city
            .get_traffic_light(
                road.end
            )
        )

        dx = (
            road.end.x
            - road.start.x
        )

        dy = (
            road.end.y
            - road.start.y
        )

        is_horizontal = (
            abs(dx) > abs(dy)
        )

        if is_horizontal:

            return not (
                light
                .allows_horizontal()
            )

        return not (
            light
            .allows_vertical()
        )

    # ========================================================
    # FIND VEHICLE AHEAD
    # ========================================================

    def _find_vehicle_ahead(
        self,
        vehicle: Vehicle,
    ) -> Vehicle | None:

        closest = None

        closest_distance = (
            float("inf")
        )

        for other in self.vehicles:

            if other is vehicle:

                continue

            if other.finished:

                continue

            if (
                other.current_road
                != vehicle.current_road
            ):

                continue

            if (
                other.progress
                <= vehicle.progress
            ):

                continue

            distance = (
                other.progress
                - vehicle.progress
            )

            if (
                distance
                < closest_distance
            ):

                closest = other

                closest_distance = (
                    distance
                )

        return closest

    # ========================================================
    # DISTANCE TO VEHICLE
    # ========================================================

    def _distance_to_vehicle(
        self,
        vehicle: Vehicle,
        other: Vehicle,
    ) -> float:

        return (
            other.progress
            - vehicle.progress
        )