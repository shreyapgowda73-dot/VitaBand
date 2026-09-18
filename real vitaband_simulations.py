import pandas as pd
import numpy as np


# ==================================================
# FILE PATHS
# ==================================================

ecg_file = "s10_run.csv"

fall1_file = "full_dataset/dataset/fall/user1/user1_fall1.csv"
fall2_file = "full_dataset/dataset/fall/user1/user1_fall2.csv"

adl1_file = "full_dataset/dataset/ADL/user1/user1_adl1.csv"
adl8_file = "full_dataset/dataset/ADL/user1/user1_adl8.csv"


# ==================================================
# VITABAND REAL DATA MONITORING
# ==================================================

print()
print("==========================================")
print("       VITABAND REAL DATA MONITORING")
print("==========================================")


# ==================================================
# 1. REAL ECG DATA
# ==================================================

print()
print("ECG ANALYSIS")
print("------------")

data = pd.read_csv(ecg_file)

sampling_rate = 500

peak_indices = np.where(
    data["peaks"].values == 1
)[0]

print("Total ECG samples:", len(data))
print("Detected R-peaks:", len(peak_indices))

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

    heart_rate = 0

    print(
        "Not enough R-peaks to calculate heart rate."
    )


# ==================================================
# 2. REAL PPG + SpO2 ANALYSIS
# ==================================================

print()
print("PPG / SpO2 ANALYSIS")
print("-------------------")

# Official dataset mapping:
# pleth_1 = Red
# pleth_2 = Infrared

red = data[
    "pleth_1"
].astype(float).values

ir = data[
    "pleth_2"
].astype(float).values

print(
    "PPG channels used: Red + Infrared"
)

print(
    "Total PPG samples:",
    len(red)
)


# ==================================================
# PPG FILTERING
# ==================================================

filter_window = 25

red_smooth = np.convolve(
    red,
    np.ones(filter_window)
    / filter_window,
    mode="same"
)

ir_smooth = np.convolve(
    ir,
    np.ones(filter_window)
    / filter_window,
    mode="same"
)


# ==================================================
# PPG WINDOW ANALYSIS
# ==================================================

window_seconds = 10

window_samples = (
    window_seconds
    * sampling_rate
)

number_of_windows = (
    len(red)
    // window_samples
)

valid_ratios = []

rejected_windows = []


for i in range(number_of_windows):

    start = i * window_samples

    end = (
        start
        + window_samples
    )

    red_window = red[start:end]

    ir_window = ir[start:end]

    red_smooth_window = (
        red_smooth[start:end]
    )

    ir_smooth_window = (
        ir_smooth[start:end]
    )


    # ----------------------------------------------
    # DC COMPONENT
    # ----------------------------------------------

    red_dc = np.mean(
        red_window
    )

    ir_dc = np.mean(
        ir_window
    )


    # ----------------------------------------------
    # AC COMPONENT
    # ----------------------------------------------

    red_ac_signal = (
        red_window
        - red_smooth_window
    )

    ir_ac_signal = (
        ir_window
        - ir_smooth_window
    )

    red_ac = np.std(
        red_ac_signal
    )

    ir_ac = np.std(
        ir_ac_signal
    )


    # ----------------------------------------------
    # SIGNAL QUALITY CHECK
    # ----------------------------------------------

    minimum_ac = 5

    if (
        red_ac < minimum_ac
        or
        ir_ac < minimum_ac
    ):

        rejected_windows.append(
            i + 1
        )

        continue


    # ----------------------------------------------
    # RATIO OF RATIOS
    # ----------------------------------------------

    ratio = (
        (red_ac / red_dc)
        /
        (ir_ac / ir_dc)
    )


    # Engineering screening range
    if (
        ratio < 0.3
        or
        ratio > 1.5
    ):

        rejected_windows.append(
            i + 1
        )

        continue


    valid_ratios.append(
        ratio
    )


# ==================================================
# PPG RESULTS
# ==================================================

print(
    "Window length:",
    window_seconds,
    "seconds"
)

print(
    "Total windows:",
    number_of_windows
)

print(
    "Valid PPG windows:",
    len(valid_ratios)
)

print(
    "Rejected PPG windows:",
    len(rejected_windows)
)


if len(valid_ratios) > 0:

    average_r = np.mean(
        valid_ratios
    )

    minimum_r = np.min(
        valid_ratios
    )

    maximum_r = np.max(
        valid_ratios
    )

    print(
        "Average R value:",
        round(
            average_r,
            4
        )
    )

    print(
        "Minimum R value:",
        round(
            minimum_r,
            4
        )
    )

    print(
        "Maximum R value:",
        round(
            maximum_r,
            4
        )
    )

    ppg_status = (
        "DATA PROCESSED"
    )

else:

    average_r = 0

    minimum_r = 0

    maximum_r = 0

    ppg_status = (
        "DATA NOT AVAILABLE"
    )

    print(
        "No valid PPG windows available."
    )


# ==================================================
# REFERENCE SpO2
# ==================================================

reference_spo2_start = 96

reference_spo2_end = 97

print()
print(
    "Reference SpO2:"
)

print(
    "Start:",
    reference_spo2_start,
    "%"
)

print(
    "End:",
    reference_spo2_end,
    "%"
)

print(
    "Reference range:",
    f"{reference_spo2_start}-{reference_spo2_end}%"
)

print(
    "Note: Reference SpO2 values are"
)

print(
    "start/end measurements from the dataset."
)

print(
    "They are not continuous calculated SpO2."
)


# ==================================================
# 3. REAL MOTION DATA
# ==================================================

print()
print("MOTION ANALYSIS")
print("---------------")

ax = data[
    "a_x"
].values

ay = data[
    "a_y"
].values

az = data[
    "a_z"
].values

gx = data[
    "g_x"
].values

gy = data[
    "g_y"
].values

gz = data[
    "g_z"
].values


# Acceleration magnitude

acceleration_magnitude = np.sqrt(
    ax**2
    + ay**2
    + az**2
)


# Gyroscope magnitude

gyro_magnitude = np.sqrt(
    gx**2
    + gy**2
    + gz**2
)


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


# ==================================================
# 4. FALL DETECTION FUNCTION
# ==================================================

def detect_fall(file_path):

    data = pd.read_csv(
        file_path,
        header=None
    )

    data.columns = [
        "time",
        "x",
        "y",
        "z",
        "a",
        "sensor"
    ]


    # ==================================================
    # ACCELEROMETER
    # ==================================================

    acc_data = data[
        data["sensor"] == "acc"
    ].copy()


    if len(acc_data) == 0:

        return {
            "fall": False,
            "impact": False,
            "orientation": False,
            "inactivity": False,
            "peak_acceleration": 0,
            "peak_gyro": 0
        }


    ax = acc_data[
        "x"
    ].astype(float).values

    ay = acc_data[
        "y"
    ].astype(float).values

    az = acc_data[
        "z"
    ].astype(float).values


    acceleration_magnitude = np.sqrt(
        ax**2
        + ay**2
        + az**2
    )


    # ==================================================
    # GYROSCOPE
    # ==================================================

    gyro_data = data[
        data["sensor"] == "gyro"
    ].copy()


    if len(gyro_data) > 0:

        gx = gyro_data[
            "x"
        ].astype(float).values

        gy = gyro_data[
            "y"
        ].astype(float).values

        gz = gyro_data[
            "z"
        ].astype(float).values


        gyro_magnitude = np.sqrt(
            gx**2
            + gy**2
            + gz**2
        )

    else:

        gyro_magnitude = (
            np.array([])
        )


    # ==================================================
    # 1. IMPACT DETECTION
    # ==================================================

    impact_threshold = 20

    impact_indices = np.where(
        acceleration_magnitude
        > impact_threshold
    )[0]


    if len(impact_indices) > 0:

        impact_detected = True

        impact_index = impact_indices[
            np.argmax(
                acceleration_magnitude[
                    impact_indices
                ]
            )
        ]

        peak_acceleration = (
            acceleration_magnitude[
                impact_index
            ]
        )

    else:

        impact_detected = False

        impact_index = None

        peak_acceleration = 0


    # ==================================================
    # 2. ORIENTATION / MOTION CHANGE
    # ==================================================

    gyro_threshold = 2


    if len(gyro_magnitude) > 0:

        peak_gyro = np.max(
            gyro_magnitude
        )

        orientation_detected = (
            peak_gyro
            > gyro_threshold
        )

    else:

        peak_gyro = 0

        orientation_detected = False


    # ==================================================
    # 3. POST-IMPACT MOVEMENT
    # ==================================================

    inactivity_detected = False


    if impact_detected:

        post_start = (
            impact_index + 1
        )

        post_end = min(
            impact_index + 21,
            len(
                acceleration_magnitude
            )
        )


        post_data = (
            acceleration_magnitude[
                post_start:post_end
            ]
        )


        if len(post_data) > 0:

            movement_threshold = 3.0


            low_movement_samples = np.sum(
                post_data
                < movement_threshold
            )


            low_movement_percentage = (
                low_movement_samples
                / len(post_data)
            ) * 100


            # More flexible supporting
            # inactivity criterion

            if (
                low_movement_percentage
                >= 30
            ):

                inactivity_detected = True

            else:

                inactivity_detected = False

        else:

            inactivity_detected = False


    # ==================================================
    # 4. FALL DECISION
    # ==================================================

    # Current research prototype:
    #
    # Strong impact
    # +
    # Significant orientation change
    #
    # indicates a possible fall.
    #
    # Post-impact inactivity is retained
    # as supporting information.


    if (
        impact_detected
        and
        orientation_detected
    ):

        fall_detected = True

    else:

        fall_detected = False


    # ==================================================
    # RETURN RESULTS
    # ==================================================

    return {

        "fall":
            fall_detected,

        "impact":
            impact_detected,

        "orientation":
            orientation_detected,

        "inactivity":
            inactivity_detected,

        "peak_acceleration":
            peak_acceleration,

        "peak_gyro":
            peak_gyro
    }


# ==================================================
# 5. FALL DATA VALIDATION
# ==================================================

print()
print("FALL DETECTION VALIDATION")
print("--------------------------")


fall1_result = detect_fall(
    fall1_file
)

fall2_result = detect_fall(
    fall2_file
)

adl1_result = detect_fall(
    adl1_file
)

adl8_result = detect_fall(
    adl8_file
)


print()

print(
    "user1_fall1.csv:",
    "FALL DETECTED"
    if fall1_result["fall"]
    else
    "NO FALL DETECTED"
)

print(
    "user1_fall2.csv:",
    "FALL DETECTED"
    if fall2_result["fall"]
    else
    "NO FALL DETECTED"
)

print(
    "user1_adl1.csv:",
    "FALL DETECTED"
    if adl1_result["fall"]
    else
    "NO FALL DETECTED"
)

print(
    "user1_adl8.csv:",
    "FALL DETECTED"
    if adl8_result["fall"]
    else
    "NO FALL DETECTED"
)


# ==================================================
# 6. FINAL VITABAND STATUS
# ==================================================

print()
print("==========================================")
print("       FINAL VITABAND STATUS")
print("==========================================")


# ECG status

if heart_rate > 0:

    print(
        "ECG Status: DATA PROCESSED"
    )

else:

    print(
        "ECG Status: DATA NOT AVAILABLE"
    )


# PPG status

print(
    "PPG Status:",
    ppg_status
)

print(
    "Valid PPG Windows:",
    len(valid_ratios)
)

print(
    "Average R Value:",
    round(
        average_r,
        4
    )
)

print(
    "Reference SpO2:",
    f"{reference_spo2_start}-{reference_spo2_end}%"
)


# Selected fall test

selected_fall_status = (
    "FALL DETECTED"
    if fall1_result["fall"]
    else
    "NO FALL"
)

print(
    "Selected Fall Test:",
    selected_fall_status
)


# Final status

if fall1_result["fall"]:

    final_status = (
        "ATTENTION REQUIRED"
    )

else:

    final_status = "NORMAL"


print()

print(
    "FINAL VITABAND STATUS:",
    final_status
)

print(
    "=========================================="
)