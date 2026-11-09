class EdgeCalculator:

    def calculate_cost(
        self,
        distance,
        cost_per_km
    ):
        return distance * cost_per_km

    def calculate_travel_time(
        self,
        distance,
        speed
    ):
        return distance / speed

    def calculate_co2(
        self,
        distance,
        factor
    ):
        return distance * factor