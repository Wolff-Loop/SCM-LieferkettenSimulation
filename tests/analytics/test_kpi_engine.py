from src.analytics.kpi_engine import KPIEngine


def test_kpi_returns_dictionary():

    engine = KPIEngine()

    result = engine.calculate()

    assert isinstance(
        result,
        dict
    )