import pandas as pd
import pytest

from swarm.main import BeeMeasure

# Swarming DataFrames with realistic fluctuations
df_swarm_1 = pd.DataFrame(
    {
        "timestamp": pd.date_range("2024-09-27 00:00:00", periods=20, freq="30S"),
        "bee_count": [
            200, 220, 250, 240, 270, 300, 320, 500, 750, 900,
            1000, 950, 900, 850, 700, 600, 550, 500, 450, 400
        ],
    }
)

df_swarm_2 = pd.DataFrame(
    {
        "timestamp": pd.date_range("2024-09-27 00:00:00", periods=20, freq="30S"),
        "bee_count": [
            180, 190, 210, 200, 230, 260, 280, 400, 650, 850,
            950, 1000, 970, 930, 880, 800, 750, 680, 600, 550
        ],
    }
)

# False alarm DataFrames with more moderate fluctuations
df_false_alarm_1 = pd.DataFrame(
    {
        "timestamp": pd.date_range("2024-09-27 00:00:00", periods=20, freq="30S"),
        "bee_count": [
            150, 140, 145, 135, 150, 160, 155, 170, 165, 160,
            170, 180, 175, 170, 165, 160, 155, 150, 145, 140
        ],
    }
)

df_false_alarm_2 = pd.DataFrame(
    {
        "timestamp": pd.date_range("2024-09-27 00:00:00", periods=20, freq="30S"),
        "bee_count": [
            130, 140, 135, 145, 150, 140, 150, 155, 160, 155,
            150, 145, 140, 135, 140, 145, 150, 140, 130, 125
        ],
    }
)

# Hardcoded expected outputs, these should match your swarm detection logic.
expected1 = pd.Series([8, 9, 10], index=[8, 9, 10], name="bee_count")
expected2 = pd.Series([8, 9, 10], index=[8, 9, 10], name="bee_count")
expected3 = pd.Series([], dtype=float, name="bee_count")
expected4 = pd.Series([], dtype=float, name="bee_count")


@pytest.fixture(scope="module")
def bee_measure():
    return BeeMeasure()

@pytest.mark.parametrize(
    "input_, expected",
    [
        (df_swarm_1, expected1),
        (df_swarm_2, expected2),
        (df_false_alarm_1, expected3),
        (df_false_alarm_2, expected4),
    ],
)
def test_swarm(bee_measure, input_, expected):
    actual = bee_measure.detect_swarm_event_rolling(input_)
    pd.testing.assert_series_equal(actual, expected, check_index=False)
