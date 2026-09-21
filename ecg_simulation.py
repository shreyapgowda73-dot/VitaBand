import numpy as np
import matplotlib.pyplot as plt


heart_rate = 110       # beats per minute
duration = 10            # simulation time in seconds
sampling_rate = 250      # samples per second



t = np.arange(0, duration, 1 / sampling_rate)



ecg = np.zeros(len(t))

beat_interval = 60 / heart_rate

for beat_start in np.arange(0, duration, beat_interval):

    # P wave
    ecg += 0.15 * np.exp(
        -((t - (beat_start + 0.20)) ** 2) / (2 * 0.025 ** 2)
    )

    # Q wave
    ecg -= 0.15 * np.exp(
        -((t - (beat_start + 0.38)) ** 2) / (2 * 0.012 ** 2)
    )

    # R wave
    ecg += 1.00 * np.exp(
        -((t - (beat_start + 0.40)) ** 2) / (2 * 0.015 ** 2)
    )

    # S wave
    ecg -= 0.25 * np.exp(
        -((t - (beat_start + 0.43)) ** 2) / (2 * 0.012 ** 2)
    )

    # T wave
    ecg += 0.30 * np.exp(
        -((t - (beat_start + 0.65)) ** 2) / (2 * 0.05 ** 2)
    )





# Add Realistic Noise


# Small random electrical noise
random_noise = np.random.normal(0, 0.03, len(t))

# Slow baseline variation
baseline_wander = 0.05 * np.sin(2 * np.pi * 0.5 * t)

# Simulated motion artifact
motion_artifact = np.zeros(len(t))

motion_start = int(4 * sampling_rate)
motion_end = int(5 * sampling_rate)

motion_artifact[motion_start:motion_end] = (
    0.25 * np.sin(2 * np.pi * 8 * t[motion_start:motion_end])
)

# Combine the noise components
ecg = ecg + random_noise + baseline_wander + motion_artifact

# ECG Filtering

window_size = 5

filtered_ecg = np.convolve(
    ecg,
    np.ones(window_size) / window_size,
    mode="same"
)

# R-Peak Detection


r_peaks = []

# Minimum distance between two R-peaks
min_distance = int(0.5 * sampling_rate)

for i in range(1, len(filtered_ecg) - 1):

    if filtered_ecg[i] > filtered_ecg[i - 1] and filtered_ecg[i] > filtered_ecg[i + 1]:

        if filtered_ecg[i] > 0.5:

            if len(r_peaks) == 0 or i - r_peaks[-1] > min_distance:
                r_peaks.append(i)



# Calculate Heart Rate


if len(r_peaks) > 1:

    rr_intervals = np.diff(r_peaks) / sampling_rate

    average_rr = np.mean(rr_intervals)

    calculated_heart_rate = 60 / average_rr

else:

    calculated_heart_rate = 0


print("Detected R-peaks:", len(r_peaks))
print("Calculated Heart Rate:",
      round(calculated_heart_rate, 2), "BPM")



# Display ECG with R-peaks


plt.figure(figsize=(12, 4))

plt.plot(t, ecg, label="Noisy ECG")
plt.plot(t, filtered_ecg, label="Filtered ECG")

plt.scatter(
    t[r_peaks],
    filtered_ecg[r_peaks],
    label="Detected R-peaks"
)

plt.title("VitaBand - ECG Simulation and R-Peak Detection")
plt.xlabel("Time (seconds)")
plt.ylabel("ECG Amplitude")

plt.legend()
plt.grid(True)

plt.show()