import pandas as pd
import numpy as np

# Load real fall data
file_path = "full_dataset/dataset/adl/user1/user1_adl8.csv"

data = pd.read_csv(file_path, header=None)
data.columns = ["time", "x", "y", "z", "a", "sensor"]

print("VitaBand Real Fall Analysis")
print("---------------------------")

# -----------------------------
# Accelerometer data
# -----------------------------
acc_data = data[data["sensor"] == "acc"].copy()

ax = acc_data["x"].astype(float).values
ay = acc_data["y"].astype(float).values
az = acc_data["z"].astype(float).values

acceleration_magnitude = np.sqrt(
    ax**2 + ay**2 + az**2
)

# -----------------------------
# Gyroscope data
# -----------------------------
gyro_data = data[data["sensor"] == "gyro"].copy()

gx = gyro_data["x"].astype(float).values
gy = gyro_data["y"].astype(float).values
gz = gyro_data["z"].astype(float).values

gyro_magnitude = np.sqrt(
    gx**2 + gy**2 + gz**2
)

# -----------------------------
# Impact detection
# -----------------------------
impact_threshold = 20

impact_indices = np.where(
    acceleration_magnitude > impact_threshold
)[0]

if len(impact_indices) > 0:

    impact_detected = True

    impact_index = impact_indices[
        np.argmax(
            acceleration_magnitude[impact_indices]
        )
    ]

    peak_acceleration = acceleration_magnitude[
        impact_index
    ]

    print("Impact detected!")
    print("Peak acceleration:",
          round(peak_acceleration, 2))

    print("Impact sample index:",
          impact_index)

else:

    impact_detected = False
    impact_index = None
    peak_acceleration = 0

    print("No significant impact detected.")

# -----------------------------
# Gyroscope analysis
# -----------------------------
gyro_threshold = 2

if len(gyro_magnitude) > 0:

    peak_gyro = np.max(gyro_magnitude)

    if peak_gyro > gyro_threshold:
        orientation_detected = True

        print()
        print("Significant motion/orientation change detected!")
        print("Peak gyroscope magnitude:",
              round(peak_gyro, 2))

    else:
        orientation_detected = False

        print()
        print("No significant orientation change detected.")

else:

    orientation_detected = False
    peak_gyro = 0

    print()
    print("No gyroscope data available.")

# -----------------------------
# Post-impact inactivity
# -----------------------------
if impact_detected:

    post_start = impact_index + 1

    post_end = min(
        impact_index + 21,
        len(acceleration_magnitude)
    )

    post_fall_acceleration = acceleration_magnitude[
        post_start:post_end
    ]

    print()
    print("Post-impact acceleration values:")
    print(np.round(post_fall_acceleration, 2))

    if len(post_fall_acceleration) > 0:

        movement_threshold = 3.0

        low_movement_samples = np.sum(
            post_fall_acceleration < movement_threshold
        )

        total_post_samples = len(
            post_fall_acceleration
        )

        low_movement_percentage = (
            low_movement_samples /
            total_post_samples
        ) * 100

        print()
        print("Low-movement samples:",
              low_movement_samples)

        print("Total post-impact samples:",
              total_post_samples)

        print("Low-movement percentage:",
              round(low_movement_percentage, 2), "%")

        if low_movement_percentage >= 60:

            inactivity_detected = True
            print("Post-fall inactivity detected!")

        else:

            inactivity_detected = False
            print("Post-fall inactivity not detected.")

    else:

        inactivity_detected = False
        print("Not enough post-impact data.")

else:

    inactivity_detected = False
    print("Inactivity check skipped because no impact was detected.")

# -----------------------------
# Final fall decision
# -----------------------------
if (
    impact_detected
    and orientation_detected
    and inactivity_detected
):

    fall_detected = True

else:

    fall_detected = False

print()
print("----------------------------")

if fall_detected:

    print("FALL DETECTED")

else:

    print("NO FALL DETECTED")

print("----------------------------")