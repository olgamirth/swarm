import pytest

from swarm.main import BeeMeasure

from .helpers import generate_bee_count_data


@pytest.fixture
def no_swarm_data():
    return generate_bee_count_data()


@pytest.fixture
def swarm_event():
    return generate_bee_count_data(swarm_time=...)


@pytest.fixture
def bee_measure():
    return BeeMeasure()


def test_bee_measure_false_alert(bee_measure, no_swarm_data):
    swarm_events = bee_measure.detect_swarm_event_pandas(no_swarm_data)
    assert swarm_events == []


def test_bee_measure_swarm_event(bee_measure, swarm_event):
    swarm_events = bee_measure.detect_swarm_event_pandas(swarm_event)
    assert swarm_events == [...]
