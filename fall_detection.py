import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# 1. Basic simulation settings
# --------------------------------------------------

duration = 10
sampling_rate = 50

t = np.arange(0, duration, 1 / sampling_rate)

# --------------------------------------------------
# 2. Simulate accelerometer data
# --------------------------------------------------

# Normal acceleration due to gravity
ax = np.zeros(len(t))
ay = np.zeros(len(t))
az = np.ones(len(t)) * 9.81

# Small normal movement variations
ax += np.random.normal(0, 0.3, len(t))
ay += np.random.normal(0, 0.3, len(t))
az += np.random.normal(0, 0.3, len(t))

# Fall event between 3 and 4 seconds
fall_start = int(3 * sampling_rate)
fall_end = int(4 * sampling_rate)

# Simulate sudden impact
az[fall_start:fall_end] += 15

# --------------------------------------------------
# 3. Simulate post-fall inactivity
# --------------------------------------------------

inactivity_start = int(4 * sampling_rate)

ax[inactivity_start:] = np.random.normal(
    0, 0.05, len(t) - inactivity_start
)

ay[inactivity_start:] = np.random.normal(
    0, 0.05, len(t) - inactivity_start
)

az[inactivity_start:] = 9.81 + np.random.normal(
    0, 0.05, len(t) - inactivity_start
)

# --------------------------------------------------
# 4. Calculate total acceleration
# --------------------------------------------------

acceleration_magnitude = np.sqrt(
    ax**2 + ay**2 + az**2
)

# --------------------------------------------------
# 5. Simulate gyroscope data
# --------------------------------------------------

# Small angular movement during normal activity
gx = np.random.normal(0, 2, len(t))
gy = np.random.normal(0, 2, len(t))
gz = np.random.normal(0, 2, len(t))

# Simulate sudden orientation change during the fall
gx[fall_start:fall_end] += 100
gy[fall_start:fall_end] += 80

# --------------------------------------------------
# 6. Calculate gyroscope magnitude
# --------------------------------------------------

gyro_magnitude = np.sqrt(
    gx**2 + gy**2 + gz**2
)

# --------------------------------------------------
# 7. Detect sudden impact
# --------------------------------------------------

impact_threshold = 20

impact_indices = np.where(
    acceleration_magnitude > impact_threshold
)[0]

if len(impact_indices) > 0:
    impact_detected = True
    print("Impact detected!")
else:
    impact_detected = False
    print("No impact detected.")

# --------------------------------------------------
# 8. Detect sudden orientation change
# --------------------------------------------------

gyro_threshold = 50

orientation_indices = np.where(
    gyro_magnitude > gyro_threshold
)[0]

if len(orientation_indices) > 0:
    orientation_detected = True
    print("Sudden orientation change detected!")
else:
    orientation_detected = False
    print("No significant orientation change detected.")

# --------------------------------------------------
# 9. Detect post-fall inactivity
# --------------------------------------------------

inactivity_threshold = 0.2

post_fall_movement = np.std(
    acceleration_magnitude[inactivity_start:]
)

if post_fall_movement < inactivity_threshold:
    inactivity_detected = True
    print("Post-fall inactivity detected!")
else:
    inactivity_detected = False
    print("Normal movement detected after impact.")

# --------------------------------------------------
# 10. Final fall decision
# --------------------------------------------------

if (
    impact_detected
    and orientation_detected
    and inactivity_detected
):
    print("Fall detected!")
else:
    print("No fall detected.")

# --------------------------------------------------
# 11. Plot accelerometer data
# --------------------------------------------------

plt.figure()

plt.plot(
    t,
    acceleration_magnitude
)

plt.xlabel("Time (seconds)")
plt.ylabel("Acceleration (m/s²)")
plt.title("Simulated Accelerometer Data")
plt.grid()

plt.show()

# --------------------------------------------------
# 12. Plot gyroscope data
# --------------------------------------------------

plt.figure()

plt.plot(
    t,
    gyro_magnitude
)

plt.xlabel("Time (seconds)")
plt.ylabel("Angular Velocity")
plt.title("Simulated Gyroscope Data")
plt.grid()

plt.show()