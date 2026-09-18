import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# 1. Basic simulation settings
# --------------------------------------------------

duration = 10
sampling_rate = 50

t = np.arange(0, duration, 1 / sampling_rate)

# --------------------------------------------------
# 2. Simulate normal accelerometer movement
# --------------------------------------------------

ax = np.random.normal(0, 0.5, len(t))
ay = np.random.normal(0, 0.5, len(t))
az = 9.81 + np.random.normal(0, 0.5, len(t))

# Calculate total acceleration
acceleration_magnitude = np.sqrt(
    ax**2 + ay**2 + az**2
)

# --------------------------------------------------
# 3. Simulate normal gyroscope movement
# --------------------------------------------------

gx = np.random.normal(0, 5, len(t))
gy = np.random.normal(0, 5, len(t))
gz = np.random.normal(0, 5, len(t))

# Calculate total angular velocity
gyro_magnitude = np.sqrt(
    gx**2 + gy**2 + gz**2
)

# --------------------------------------------------
# 4. Detect impact
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
# 5. Detect sudden orientation change
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
# 6. Check for inactivity
# --------------------------------------------------

inactivity_threshold = 0.2

# Normal movement continues throughout the simulation
post_fall_movement = np.std(
    acceleration_magnitude
)

if post_fall_movement < inactivity_threshold:
    inactivity_detected = True
    print("Post-fall inactivity detected!")
else:
    inactivity_detected = False
    print("Normal movement detected.")

# --------------------------------------------------
# 7. Final fall decision
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
# 8. Plot accelerometer data
# --------------------------------------------------

plt.figure()

plt.plot(
    t,
    acceleration_magnitude
)

plt.xlabel("Time (seconds)")
plt.ylabel("Acceleration (m/s²)")
plt.title("Normal Movement - Accelerometer Data")
plt.grid()

plt.show()

# --------------------------------------------------
# 9. Plot gyroscope data
# --------------------------------------------------

plt.figure()

plt.plot(
    t,
    gyro_magnitude
)

plt.xlabel("Time (seconds)")
plt.ylabel("Angular Velocity")
plt.title("Normal Movement - Gyroscope Data")
plt.grid()

plt.show()