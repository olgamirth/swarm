import pandas as pd
import pytest

from swarm.main import BeeMeasure


@pytest.fixture(scope="module")
def bee_counter():
    return BeeMeasure()


def generate_data(start_time, end_time, normal_count,
                  peak_count=None, peak_duration=0):
    timestamps = pd.date_range(start=start_time, end=end_time, freq='30s')
    bee_counts = [normal_count] * len(timestamps)

    if peak_count and peak_duration:
        peak_start = len(bee_counts) // 2 - peak_duration // 2
        peak_end = peak_start + peak_duration
        bee_counts[peak_start:peak_end] = [peak_count] * peak_duration

    return pd.DataFrame({'timestamp': timestamps, 'bee_count': bee_counts})\
             .set_index('timestamp')


def test_normal_behavior(bee_counter):
    df = generate_data('2024-10-01 05:00:00', '2024-10-01 17:00:00', 10)
    result = bee_counter.detect_swarm_event_pandas(df)
    assert len(result) == 0


def test_swarm_event(bee_counter):
    df = generate_data('2024-10-01 05:00:00', '2024-10-01 17:00:00',
                       10, peak_count=100, peak_duration=20)
    result = bee_counter.detect_swarm_event_pandas(df)
    assert len(result) > 0


def test_threshold_sensitivity(bee_counter):
    df = generate_data('2024-10-01 05:00:00', '2024-10-01 17:00:00',
                       10, peak_count=50, peak_duration=20)
    result1 = bee_counter\
        .detect_swarm_event_pandas(df, cumulative_threshold=5)

    result2 = bee_counter\
        .detect_swarm_event_pandas(df, cumulative_threshold=15)

    assert len(result1) > len(result2)
