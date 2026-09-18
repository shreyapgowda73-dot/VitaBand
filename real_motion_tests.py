import pandas as pd
import numpy as np

data = pd.read_csv("s10_run.csv")

# Real accelerometer data
ax = data["a_x"].values
ay = data["a_y"].values
az = data["a_z"].values

# Real gyroscope data
gx = data["g_x"].values
gy = data["g_y"].values
gz = data["g_z"].values

# Calculate acceleration magnitude
acceleration_magnitude = np.sqrt(ax**2 + ay**2 + az**2)

# Calculate gyroscope magnitude
gyro_magnitude = np.sqrt(gx**2 + gy**2 + gz**2)

print("Real Motion Data Test")
print("---------------------")

print("Total samples:", len(data))

print()
print("Accelerometer:")
print("Minimum magnitude:", round(acceleration_magnitude.min(), 2))
print("Maximum magnitude:", round(acceleration_magnitude.max(), 2))
print("Average magnitude:", round(acceleration_magnitude.mean(), 2))

print()
print("Gyroscope:")
print("Minimum magnitude:", round(gyro_magnitude.min(), 2))
print("Maximum magnitude:", round(gyro_magnitude.max(), 2))
print("Average magnitude:", round(gyro_magnitude.mean(), 2))