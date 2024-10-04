import pandas as pd
import pytest

from swarm.main import BeeMeasure

# Swarming DataFrames with realistic fluctuations
df_swarm_1 = pd.DataFrame(
    {
        "timestamp": pd.date_range("2024-09-27 00:00:00", periods=20, freq="30s"),
        "bee_count": [
            200, 220, 250, 240, 270, 300, 320, 500, 750, 900,
            1000, 950, 900, 850, 700, 600, 550, 500, 450, 400
        ],
    }
)

df_swarm_2 = pd.DataFrame(
    {
        "timestamp": pd.date_range("2024-09-27 00:00:00", periods=20, freq="30s"),
        "bee_count": [
            180, 190, 210, 200, 230, 260, 280, 400, 650, 850,
            950, 1000, 970, 930, 880, 800, 750, 680, 600, 550
        ],
    }
)

# False alarm DataFrames with more moderate fluctuations
df_false_alarm_1 = pd.DataFrame(
    {
        "timestamp": pd.date_range("2024-09-27 00:00:00", periods=20, freq="30s"),
        "bee_count": [
            150, 140, 145, 135, 150, 160, 155, 170, 165, 160,
            170, 180, 175, 170, 165, 160, 155, 150, 145, 140
        ],
    }
)

df_false_alarm_2 = pd.DataFrame(
    {
        "timestamp": pd.date_range("2024-09-27 00:00:00", periods=20, freq="30s"),
        "bee_count": [
            130, 140, 135, 145, 150, 140, 150, 155, 160, 155,
            150, 145, 140, 135, 140, 145, 150, 140, 130, 125
        ],
    }
)

# False alarm DataFrames with sustained activity at the hive entrance;
# Mimicks "bearding"
df_false_alarm_3 = pd.DataFrame(
    {
        "timestamp": pd.date_range("2024-09-27 00:00:00", periods=20, freq="30s"),
        "bee_count": [
            180, 190, 210, 200, 230, 260, 280, 400, 650, 850,
            950, 1000, 1000, 1010, 990, 1020, 1005, 995, 1000, 1010
        ],
    }
)

@pytest.fixture(scope="module")
def bee_measure():
    return BeeMeasure()

@pytest.mark.parametrize(
    "input_, expected",
    [
        (df_swarm_1, True),
        (df_swarm_2, True),
        (df_false_alarm_1, False),
        (df_false_alarm_2, False),
    ],
)
def test_swarm(bee_measure, input_, expected):
    actual = bee_measure.detect_swarm_event_rolling(input_)
    assert actual is expected
