from .scenario import Scenario


class BaselineScenario(
    Scenario
):

    def __init__(self):

        super().__init__(
            "Baseline"
        )