import heapq
import math


class Router:

    def __init__(
        self,
        city,
    ) -> None:

        self.city = city

    # ========================================================
    # NORMAL ROUTE
    # ========================================================

    def find_route(
        self,
        start,
        destination,
    ):

        return self.find_traffic_aware_route(
            start=start,
            destination=destination,
            vehicles=None,
        )

    # ========================================================
    # TRAFFIC-AWARE ROUTE
    # ========================================================

    def find_traffic_aware_route(
        self,
        start,
        destination,
        vehicles=None,
    ):

        if start == destination:

            return []

        open_set = []

        heapq.heappush(
            open_set,
            (
                0.0,
                start.id,
                start,
            ),
        )

        came_from = {}

        cost_so_far = {
            start: 0.0
        }

        while open_set:

            _, _, current = (
                heapq.heappop(
                    open_set
                )
            )

            if current == destination:

                return self._reconstruct_path(
                    came_from,
                    current,
                )

            for road in self.city.roads:

                if road.start != current:
                    continue

                next_node = road.end

                road_cost = (
                    self._road_cost(
                        road,
                        vehicles,
                    )
                )

                new_cost = (
                    cost_so_far[current]
                    + road_cost
                )

                if (
                    next_node
                    not in cost_so_far
                    or new_cost
                    < cost_so_far[next_node]
                ):

                    cost_so_far[
                        next_node
                    ] = new_cost

                    priority = (
                        new_cost
                        + self._heuristic(
                            next_node,
                            destination,
                        )
                    )

                    heapq.heappush(
                        open_set,
                        (
                            priority,
                            next_node.id,
                            next_node,
                        ),
                    )

                    came_from[
                        next_node
                    ] = (
                        current,
                        road,
                    )

        return []

    # ========================================================
    # ROAD COST
    # ========================================================

    def _road_cost(
        self,
        road,
        vehicles,
    ) -> float:

        base_cost = (
            road.get_length()
        )

        if vehicles is None:

            return base_cost

        traffic_count = 0

        for vehicle in vehicles:

            if vehicle.finished:
                continue

            if (
                vehicle.current_road
                == road
            ):

                traffic_count += 1

        # ----------------------------------------------------
        # Traffic penalty
        # ----------------------------------------------------
        #
        # Example:
        #
        # 0 vehicles -> normal cost
        # 5 vehicles -> higher cost
        # 10 vehicles -> much higher cost
        #
        # This encourages vehicles to avoid
        # congested roads.

        traffic_penalty = (
            traffic_count
            * 20.0
        )

        return (
            base_cost
            + traffic_penalty
        )

    # ========================================================
    # HEURISTIC
    # ========================================================

    def _heuristic(
        self,
        current,
        destination,
    ) -> float:

        dx = (
            destination.x
            - current.x
        )

        dy = (
            destination.y
            - current.y
        )

        return math.sqrt(
            dx * dx
            + dy * dy
        )

    # ========================================================
    # PATH RECONSTRUCTION
    # ========================================================

    def _reconstruct_path(
        self,
        came_from,
        current,
    ) -> list:

        path = []

        while current in came_from:

            previous, road = (
                came_from[current]
            )

            path.append(
                road
            )

            current = previous

        path.reverse()

        return path