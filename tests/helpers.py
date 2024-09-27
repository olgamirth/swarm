import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def generate_bee_count_data(days=1, interval_minutes=0.5, swarm_time=None):
    # TODO: make sure the data returned here supports rolling, because we
    # got a: *** AttributeError: 'BeeMeasure' object has no attribute 'rolling'

    start_time = datetime.now().replace(hour=0, minute=0, second=0,
                                        microsecond=0)
    end_time = start_time + timedelta(days=days)
    timestamps = pd.date_range(start=start_time, end=end_time,
                               freq=f'{interval_minutes}T')

    # Base bee count (normal activity)
    base_count = 50

    # TODO: take the randomness out

    # Generate bee counts
    bee_counts = []
    for timestamp in timestamps:
        hour = timestamp.hour

        # Daytime activity factor (higher during the day)
        day_factor = 1 + 0.5 * np.sin(np.pi * (hour - 6) / 12) \
            if 6 <= hour <= 18 else 0.5

        # Random noise
        noise = np.random.normal(0, 5)

        # Calculate bee count
        count = int(base_count * day_factor + noise)

        # Simulate swarming event
        if swarm_time and timestamp >= swarm_time and \
           timestamp < swarm_time + timedelta(hours=2):

            swarm_factor = 5 * np.exp(-((timestamp -
                                         swarm_time).total_seconds() / 3600))
            count = int(count * swarm_factor)

        bee_counts.append(count)

    df = pd.DataFrame({'timestamp': timestamps, 'bee_count': bee_counts})
    return df
