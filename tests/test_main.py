import pandas as pd
import pytest

from swarm.main import BeeMeasure

df_swarm_1 = pd.DataFrame(
    {
        "timestamp": pd.date_range("2024-09-27 00:00:00", periods=20, freq="30S"),
        "bee_count": [
            30,
            32,
            35,
            40,
            42,
            45,
            50,
            60,
            80,
            100,
            120,
            150,
            180,
            200,
            220,
            240,
            260,
            280,
            300,
            320,
        ],
    }
)

df_swarm_2 = pd.DataFrame(
    {
        "timestamp": pd.date_range("2024-09-27 00:00:00", periods=20, freq="30S"),
        "bee_count": [
            20,
            21,
            22,
            23,
            24,
            26,
            28,
            30,
            35,
            40,
            45,
            50,
            55,
            60,
            100,
            120,
            150,
            200,
            250,
            300,
        ],
    }
)

df_false_alarm_1 = pd.DataFrame(
    {
        "timestamp": pd.date_range("2024-09-27 00:00:00", periods=20, freq="30S"),
        "bee_count": [
            30,
            28,
            27,
            29,
            31,
            30,
            32,
            31,
            30,
            29,
            28,
            27,
            26,
            27,
            28,
            29,
            30,
            29,
            28,
            27,
        ],
    }
)

df_false_alarm_2 = pd.DataFrame(
    {
        "timestamp": pd.date_range("2024-09-27 00:00:00", periods=20, freq="30S"),
        "bee_count": [
            20,
            21,
            22,
            23,
            24,
            25,
            24,
            25,
            26,
            27,
            28,
            27,
            28,
            29,
            30,
            29,
            30,
            31,
            32,
            31,
        ],
    }
)

# Hardcoded expected outputs, these should match your swarm detection logic.
expected1 = pd.Series(
    [12, 13, 14], index=[12, 13, 14]
)  # Example: indices where swarm detected
expected2 = pd.Series([15, 16, 17], index=[15, 16, 17])
expected3 = pd.Series([], dtype=float)  # False alarms should return empty Series
expected4 = pd.Series([], dtype=float)


@pytest.fixture(scope="module")
def bee_measure():
    return BeeMeasure()


@pytest.mark.parametrize(
    "input_, output",
    [
        (df_swarm_1, expected1),
        (df_swarm_2, expected2),
        (df_false_alarm_1, expected3),
        (df_false_alarm_2, expected4),
    ],
)
def test_swarm(bee_measure, input_, output):
    actual = bee_measure.detect_swarm_event_pandas(input_)
    pd.testing.assert_series_equal(actual, output)
