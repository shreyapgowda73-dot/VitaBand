import pandas as pd
import numpy as np

# Load the real fall dataset
file_path = "full_dataset/dataset/fall/user1/user1_fall1.csv"

data = pd.read_csv(file_path, header=None)

# Give names to the columns
data.columns = ["time", "x", "y", "z", "a", "sensor"]

print("VitaBand Real Fall Data Test")
print("----------------------------")

# Separate accelerometer and gyroscope data
acc_data = data[data["sensor"] == "acc"]
gyro_data = data[data["sensor"] == "gyro"]

print("Total records:", len(data))
print("Accelerometer records:", len(acc_data))
print("Gyroscope records:", len(gyro_data))

# Calculate acceleration magnitude
if len(acc_data) > 0:
    ax = acc_data["x"].astype(float).values
    ay = acc_data["y"].astype(float).values
    az = acc_data["z"].astype(float).values

    acceleration_magnitude = np.sqrt(
        ax**2 + ay**2 + az**2
    )

    print()
    print("Accelerometer Analysis")
    print("----------------------")
    print("Minimum magnitude:",
          round(acceleration_magnitude.min(), 2))
    print("Maximum magnitude:",
          round(acceleration_magnitude.max(), 2))
    print("Average magnitude:",
          round(acceleration_magnitude.mean(), 2))

# Calculate gyroscope magnitude
if len(gyro_data) > 0:
    gx = gyro_data["x"].astype(float).values
    gy = gyro_data["y"].astype(float).values
    gz = gyro_data["z"].astype(float).values

    gyro_magnitude = np.sqrt(
        gx**2 + gy**2 + gz**2
    )

    print()
    print("Gyroscope Analysis")
    print("------------------")
    print("Minimum magnitude:",
          round(gyro_magnitude.min(), 2))
    print("Maximum magnitude:",
          round(gyro_magnitude.max(), 2))
    print("Average magnitude:",
          round(gyro_magnitude.mean(), 2))