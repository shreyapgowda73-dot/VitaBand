import os
import pandas as pd
import numpy as np



# ECG ANALYSIS


def analyze_ecg(file_path):

    data = pd.read_csv(file_path)

    peak_indices = np.where(
        data["peaks"].values == 1
    )[0]

    print("ECG ANALYSIS")
    print("------------")
    print("Total ECG samples:", len(data))
    print("Detected R-peaks:", len(peak_indices))

    sampling_rate = 500

    if len(peak_indices) > 1:

        rr_intervals = (
            np.diff(peak_indices)
            / sampling_rate
        )

        average_rr = np.mean(rr_intervals)

        heart_rate = 60 / average_rr

        print(
            "ECG Heart Rate:",
            round(heart_rate, 2),
            "BPM"
        )

    else:

        print(
            "Not enough R-peaks to calculate heart rate."
        )

    print()



# PPG / SpO2 ANALYSIS


def analyze_ppg(file_path):

    data = pd.read_csv(file_path)

    # Dataset mapping:
    # pleth_1 = Red
    # pleth_2 = Infrared

    red = data[
        "pleth_1"
    ].astype(float).values

    ir = data[
        "pleth_2"
    ].astype(float).values

    sampling_rate = 500

    window_seconds = 10

    window_size = (
        sampling_rate
        * window_seconds
    )

    total_windows = (
        len(data)
        // window_size
    )

    valid_windows = 0
    rejected_windows = 0

    r_values = []

    minimum_ac = 5

    for i in range(total_windows):

        start = i * window_size
        end = start + window_size

        red_window = red[
            start:end
        ]

        ir_window = ir[
            start:end
        ]

        # Moving-average filtering
        filter_size = 25

        kernel = (
            np.ones(filter_size)
            / filter_size
        )

        red_filtered = np.convolve(
            red_window,
            kernel,
            mode="same"
        )

        ir_filtered = np.convolve(
            ir_window,
            kernel,
            mode="same"
        )

        # DC components
        red_dc = np.mean(
            red_filtered
        )

        ir_dc = np.mean(
            ir_filtered
        )

        # AC components
        red_ac = np.std(
            red_filtered
        )

        ir_ac = np.std(
            ir_filtered
        )

        if red_dc == 0 or ir_dc == 0:

            rejected_windows += 1
            continue

        if (
            red_ac < minimum_ac
            or ir_ac < minimum_ac
        ):

            rejected_windows += 1
            continue

        # Ratio of ratios
        ratio = (
            (red_ac / red_dc)
            /
            (ir_ac / ir_dc)
        )

        # Engineering signal-quality
        # screening range only.
        if (
            ratio < 0.3
            or ratio > 1.5
        ):

            rejected_windows += 1
            continue

        r_values.append(
            ratio
        )

        valid_windows += 1

    print("PPG / SpO2 ANALYSIS")
    print("-------------------")
    print(
        "PPG channels used: Red + Infrared"
    )

    print(
        "Total PPG samples:",
        len(data)
    )

    print(
        "Window length:",
        window_seconds,
        "seconds"
    )

    print(
        "Total windows:",
        total_windows
    )

    print(
        "Valid PPG windows:",
        valid_windows
    )

    print(
        "Rejected PPG windows:",
        rejected_windows
    )

    if len(r_values) > 0:

        print(
            "Average R value:",
            round(
                np.mean(r_values),
                4
            )
        )

        print(
            "Minimum R value:",
            round(
                np.min(r_values),
                4
            )
        )

        print(
            "Maximum R value:",
            round(
                np.max(r_values),
                4
            )
        )

    print()

    print("Reference SpO2:")
    print("Start: 96 %")
    print("End: 97 %")
    print("Reference range: 96-97%")

    print(
        "Note: Reference SpO2 values are"
    )

    print(
        "start/end measurements from the dataset."
    )

    print(
        "They are not continuous calculated SpO2."
    )

    print()



# MOTION ANALYSIS


def analyze_motion(file_path):

    data = pd.read_csv(file_path)

    ax = data[
        "a_x"
    ].astype(float).values

    ay = data[
        "a_y"
    ].astype(float).values

    az = data[
        "a_z"
    ].astype(float).values

    gx = data[
        "g_x"
    ].astype(float).values

    gy = data[
        "g_y"
    ].astype(float).values

    gz = data[
        "g_z"
    ].astype(float).values

    acceleration_magnitude = np.sqrt(
        ax**2
        + ay**2
        + az**2
    )

    gyro_magnitude = np.sqrt(
        gx**2
        + gy**2
        + gz**2
    )

    print("MOTION ANALYSIS")
    print("---------------")

    print(
        "Acceleration average:",
        round(
            acceleration_magnitude.mean(),
            2
        )
    )

    print(
        "Acceleration maximum:",
        round(
            acceleration_magnitude.max(),
            2
        )
    )

    print(
        "Gyroscope average:",
        round(
            gyro_magnitude.mean(),
            2
        )
    )

    print(
        "Gyroscope maximum:",
        round(
            gyro_magnitude.max(),
            2
        )
    )

    print()



# FALL DETECTION

def detect_fall(
    file_path,
    display_name
):

    print("------------------------------------------")
    print(display_name)
    print("------------------------------------------")

    absolute_path = os.path.abspath(
        file_path
    )

    if not os.path.exists(
        absolute_path
    ):

        print(
            "ERROR: File not found."
        )

        return False

    data = pd.read_csv(
        absolute_path
    )

    # IMPORTANT:
    # t = timestamp
    # Unnamed: 5 = sensor type

    sensor_type = (
        data["Unnamed: 5"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    acc_data = data.loc[
        sensor_type == "acc"
    ].copy()

    gyro_data = data.loc[
        sensor_type == "gyro"
    ].copy()

    print(
        "Accelerometer records:",
        len(acc_data)
    )

    print(
        "Gyroscope records:",
        len(gyro_data)
    )

    if (
        len(acc_data) == 0
        or len(gyro_data) == 0
    ):

        print(
            "Insufficient sensor data."
        )

        return False

    
    # Convert sensor values
    

    for column in [
        "x",
        "y",
        "z"
    ]:

        acc_data[column] = pd.to_numeric(
            acc_data[column],
            errors="coerce"
        )

        gyro_data[column] = pd.to_numeric(
            gyro_data[column],
            errors="coerce"
        )

    acc_data = acc_data.dropna(
        subset=[
            "x",
            "y",
            "z"
        ]
    )

    gyro_data = gyro_data.dropna(
        subset=[
            "x",
            "y",
            "z"
        ]
    )


    # Calculate magnitudes
   

    acc_magnitude = np.sqrt(
        acc_data["x"]**2
        + acc_data["y"]**2
        + acc_data["z"]**2
    ).values

    gyro_magnitude = np.sqrt(
        gyro_data["x"]**2
        + gyro_data["y"]**2
        + gyro_data["z"]**2
    ).values

    peak_acceleration = np.max(
        acc_magnitude
    )

    peak_gyro = np.max(
        gyro_magnitude
    )

    print(
        "Peak acceleration:",
        round(
            peak_acceleration,
            2
        )
    )

    print(
        "Peak gyro:",
        round(
            peak_gyro,
            2
        )
    )

    
    # Find strongest acceleration event
    

    impact_index = np.argmax(
        acc_magnitude
    )

    post_start = (
        impact_index + 1
    )

    post_end = min(
        post_start + 20,
        len(acc_magnitude)
    )

    post_impact = (
        acc_magnitude[
            post_start:post_end
        ]
    )

    
    # Post-event inactivity
   

    inactivity_percentage = 0

    if len(post_impact) > 0:

        movement_threshold = 3.0

        low_movement_samples = np.sum(
            post_impact
            < movement_threshold
        )

        inactivity_percentage = (
            low_movement_samples
            / len(post_impact)
            * 100
        )

    
    # FALL DETECTION THRESHOLDS
    

    acceleration_threshold = 10.0

    gyro_threshold = 2.0

    inactivity_threshold = 50.0

    acceleration_event = (
        peak_acceleration
        >= acceleration_threshold
    )

    orientation_event = (
        peak_gyro
        >= gyro_threshold
    )

    inactivity_event = (
        inactivity_percentage
        >= inactivity_threshold
    )

    
    # Final decision
    

    fall_detected = (
        acceleration_event
        and orientation_event
        and inactivity_event
    )

    print(
        "Acceleration event:",
        "YES"
        if acceleration_event
        else "NO"
    )

    print(
        "Orientation event:",
        "YES"
        if orientation_event
        else "NO"
    )

    print(
        "Post-impact inactivity:",
        round(
            inactivity_percentage,
            2
        ),
        "%"
    )

    print(
        "Inactivity event:",
        "YES"
        if inactivity_event
        else "NO"
    )

    print()

    print(
        display_name,
        ":",
        "FALL DETECTED"
        if fall_detected
        else "NO FALL DETECTED"
    )

    print()

    return fall_detected


# MAIN PROGRAM


print("==========================================")
print("       VITABAND REAL DATA MONITORING")
print("==========================================")
print()



# REAL PHYSIOLOGICAL DATA

physio_file = "s10_run.csv"

analyze_ecg(
    physio_file
)

analyze_ppg(
    physio_file
)

analyze_motion(
    physio_file
)



# FALL DETECTION VALIDATION


print("FALL DETECTION VALIDATION")
print("--------------------------")
print()


fall1_result = detect_fall(
    "full_dataset/dataset/fall/user1/user1_fall1.csv",
    "user1_fall1.csv"
)

fall2_result = detect_fall(
    "full_dataset/dataset/fall/user1/user1_fall2.csv",
    "user1_fall2.csv"
)

adl1_result = detect_fall(
    "full_dataset/dataset/ADL/user1/user1_adl1.csv",
    "user1_adl1.csv"
)

adl8_result = detect_fall(
    "full_dataset/dataset/ADL/user1/user1_adl8.csv",
    "user1_adl8.csv"
)



# FINAL VITABAND STATUS

print("==========================================")
print("       FINAL VITABAND STATUS")
print("==========================================")

print(
    "ECG Status: DATA PROCESSED"
)

print(
    "PPG Status: DATA PROCESSED"
)

print(
    "Reference SpO2: 96-97%"
)

print(
    "Fall1 validation:",
    "PASS"
    if fall1_result
    else "FAIL"
)

print(
    "Fall2 validation:",
    "PASS"
    if fall2_result
    else "FAIL"
)

print(
    "ADL1 validation:",
    "PASS"
    if not adl1_result
    else "FAIL"
)

print(
    "ADL8 validation:",
    "PASS"
    if not adl8_result
    else "FAIL"
)

print()

if (
    fall1_result
    and fall2_result
    and not adl1_result
    and not adl8_result
):

    print(
        "FALL DETECTION VALIDATION: "
        "ALL SELECTED TESTS PASSED"
    )

else:

    print(
        "FALL DETECTION VALIDATION: "
        "FURTHER ANALYSIS REQUIRED"
    )

print(
    "=========================================="
)