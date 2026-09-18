import pandas as pd

data = pd.read_csv("s10_run.csv")

print("=" * 50)
print("       VITABAND TEMPERATURE DATA TEST")
print("=" * 50)

print("\nTemperature Sensor Data")
print("-----------------------")

print(data[["temp_1", "temp_2", "temp_3"]].describe())

print("\nTemperature Channels:")
print("temp_1: PPG sensor temperature")
print("temp_2: PPG sensor temperature")
print("temp_3: IMU sensor temperature")

print("\nTemperature data successfully processed.")