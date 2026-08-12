from .intersection import Intersection
from .road import Road
from .traffic_light import TrafficLight
from .zone import Zone


class City:

    def __init__(
        self,
        adaptive_lights: bool = True,
    ) -> None:

        self.intersections: list[
            Intersection
        ] = []

        self.roads: list[Road] = []

        self.traffic_lights: dict[
            Intersection,
            TrafficLight,
        ] = {}

        self.zones: list[Zone] = []

        self.adaptive_lights = adaptive_lights

    def add_intersection(
        self,
        intersection: Intersection,
    ) -> None:

        self.intersections.append(
            intersection
        )

        self.traffic_lights[
            intersection
        ] = TrafficLight(
            adaptive=self.adaptive_lights
        )

    def add_road(
        self,
        road: Road,
    ) -> None:

        self.roads.append(road)

    def get_outgoing_roads(
        self,
        intersection: Intersection,
    ) -> list[Road]:

        return [
            road
            for road in self.roads
            if road.start == intersection
        ]

    def get_traffic_light(
        self,
        intersection: Intersection,
    ) -> TrafficLight:

        return self.traffic_lights[
            intersection
        ]

    def create_zones(self) -> None:

        if len(self.intersections) < 25:
            return

        # -----------------------------
        # Residential
        # -----------------------------

        residential = Zone(
            name="Residential",
            intersections=[
                self.intersections[0],
                self.intersections[1],
                self.intersections[5],
                self.intersections[6],
            ],
            attraction=1.0,
        )

        # -----------------------------
        # Business
        # -----------------------------

        business = Zone(
            name="Business",
            intersections=[
                self.intersections[3],
                self.intersections[4],
                self.intersections[8],
                self.intersections[9],
            ],
            attraction=2.0,
        )

        # -----------------------------
        # Shopping
        # -----------------------------

        shopping = Zone(
            name="Shopping",
            intersections=[
                self.intersections[15],
                self.intersections[16],
                self.intersections[20],
                self.intersections[21],
            ],
            attraction=1.5,
        )

        # -----------------------------
        # School
        # -----------------------------

        school = Zone(
            name="School",
            intersections=[
                self.intersections[18],
                self.intersections[19],
                self.intersections[23],
                self.intersections[24],
            ],
            attraction=1.2,
        )

        self.zones = [
            residential,
            business,
            shopping,
            school,
        ]

    def get_zone(
        self,
        intersection: Intersection,
    ) -> Zone | None:

        for zone in self.zones:

            if intersection in zone.intersections:
                return zone

        return None

    def update_traffic_lights(
        self,
        dt: float,
        vehicles: list,
    ) -> None:

        for intersection in self.intersections:

            horizontal_demand = 0
            vertical_demand = 0

            for vehicle in vehicles:

                if vehicle.finished:
                    continue

                road = vehicle.current_road

                if road.end != intersection:
                    continue

                distance = (
                    vehicle.get_road_length()
                    - vehicle.progress
                )

                if distance > 100:
                    continue

                dx = (
                    road.end.x
                    - road.start.x
                )

                dy = (
                    road.end.y
                    - road.start.y
                )

                if abs(dx) > abs(dy):
                    horizontal_demand += 1
                else:
                    vertical_demand += 1

            light = self.traffic_lights[
                intersection
            ]

            light.update(
                dt=dt,
                horizontal_demand=horizontal_demand,
                vertical_demand=vertical_demand,
            )

    def generate_grid(
        self,
        rows: int,
        columns: int,
        spacing: float = 100.0,
    ) -> None:

        intersection_id = 1
        road_id = 1

        for row in range(rows):

            for column in range(columns):

                intersection = Intersection(
                    id=intersection_id,
                    x=column * spacing,
                    y=row * spacing,
                )

                self.add_intersection(
                    intersection
                )

                intersection_id += 1

        for row in range(rows):

            for column in range(columns):

                current_index = (
                    row * columns + column
                )

                current = self.intersections[
                    current_index
                ]

                # Horizontal

                if column < columns - 1:

                    right = self.intersections[
                        current_index + 1
                    ]

                    forward = Road(
                        id=road_id,
                        start=current,
                        end=right,
                    )

                    self.add_road(forward)

                    road_id += 1

                    backward = Road(
                        id=road_id,
                        start=right,
                        end=current,
                    )

                    self.add_road(backward)

                    road_id += 1

                # Vertical

                if row < rows - 1:

                    below = self.intersections[
                        current_index + columns
                    ]

                    forward = Road(
                        id=road_id,
                        start=current,
                        end=below,
                    )

                    self.add_road(forward)

                    road_id += 1

                    backward = Road(
                        id=road_id,
                        start=below,
                        end=current,
                    )

                    self.add_road(backward)

                    road_id += 1

        self.create_zones()