import pandas as pd
import matplotlib.pyplot as plt

def generate_data(start_time, end_time, normal_count, peak_count=None, peak_duration=0):
    timestamps = pd.date_range(start=start_time, end=end_time, freq='30S')
    bee_counts = [normal_count] * len(timestamps)
    
    if peak_count and peak_duration:
        peak_start = len(bee_counts) // 2 - peak_duration // 2
        peak_end = peak_start + peak_duration
        bee_counts[peak_start:peak_end] = [peak_count] * peak_duration
    
    return pd.DataFrame({'timestamp': timestamps, 'bee_count': bee_counts}).set_index('timestamp')

# Generate sample data
df = generate_data('2024-10-01 05:00:00', '2024-10-01 17:00:00', 10, peak_count=100, peak_duration=20)

# Print first and last few rows
print(df.head())
print(df.tail())

# Plot the data
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['bee_count'])
plt.title('Bee Count Over Time')
plt.xlabel('Time')
plt.ylabel('Bee Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
