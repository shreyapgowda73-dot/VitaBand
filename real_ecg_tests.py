import pandas as pd
import numpy as np

# Load real ECG data
data = pd.read_csv("s10_run.csv")

# Get the ECG peak annotations
peak_indices = np.where(data["peaks"].values == 1)[0]

print("Real ECG Data Test")
print("------------------")
print("Total ECG samples:", len(data))
print("Detected R-peaks:", len(peak_indices))

# Dataset ECG sampling rate = 500 Hz
sampling_rate = 500

# Calculate heart rate from consecutive R-peaks
if len(peak_indices) > 1:
    rr_intervals = np.diff(peak_indices) / sampling_rate
    average_rr = np.mean(rr_intervals)
    heart_rate = 60 / average_rr

    print("Average RR interval:", round(average_rr, 3), "seconds")
    print("Calculated Heart Rate:", round(heart_rate, 2), "BPM")
else:
    print("Not enough R-peaks to calculate heart rate.")