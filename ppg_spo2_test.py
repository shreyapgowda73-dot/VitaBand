import pandas as pd
import numpy as np



# LOAD REAL PPG DATA


data = pd.read_csv("s10_run.csv")

# Official dataset mapping:
# pleth_1 = Red
# pleth_2 = Infrared

red = data["pleth_1"].astype(float).values
ir = data["pleth_2"].astype(float).values

sampling_rate = 500

print("VitaBand Real PPG Analysis")
print("--------------------------")
print("Total PPG samples:", len(red))



# SIMPLE MOVING AVERAGE FILTER


filter_window = 25

red_smooth = np.convolve(
    red,
    np.ones(filter_window) / filter_window,
    mode="same"
)

ir_smooth = np.convolve(
    ir,
    np.ones(filter_window) / filter_window,
    mode="same"
)



# SHORT WINDOW ANALYSIS


window_seconds = 10
window_samples = window_seconds * sampling_rate

number_of_windows = len(red) // window_samples

print("Window length:", window_seconds, "seconds")
print("Number of complete windows:", number_of_windows)

print()
print("Window Results")
print("--------------")


valid_ratios = []
rejected_windows = []


for i in range(number_of_windows):

    start = i * window_samples
    end = start + window_samples

    red_window = red[start:end]
    ir_window = ir[start:end]

    red_smooth_window = red_smooth[start:end]
    ir_smooth_window = ir_smooth[start:end]

    
    # DC COMPONENT
    

    red_dc = np.mean(red_window)
    ir_dc = np.mean(ir_window)

    
    # AC COMPONENT
    

    red_ac_signal = (
        red_window - red_smooth_window
    )

    ir_ac_signal = (
        ir_window - ir_smooth_window
    )

    red_ac = np.std(red_ac_signal)
    ir_ac = np.std(ir_ac_signal)

   
    # SIGNAL QUALITY CHECK
    

    minimum_ac = 5

    if (
        red_ac < minimum_ac
        or ir_ac < minimum_ac
    ):

        rejected_windows.append(i + 1)

        print(
            "Window",
            i + 1,
            "| REJECTED - Low PPG variation"
        )

        continue

    
    # RATIO OF RATIOS
    

    ratio = (
        (red_ac / red_dc)
        /
        (ir_ac / ir_dc)
    )

    # Engineering screening range
    if ratio < 0.3 or ratio > 1.5:

        rejected_windows.append(i + 1)

        print(
            "Window",
            i + 1,
            "| REJECTED - Unusual R:",
            round(ratio, 4)
        )

        continue

    valid_ratios.append(ratio)

    print(
        "Window",
        i + 1,
        "| R:",
        round(ratio, 4),
        "| VALID"
    )



# PPG PROCESSING SUMMARY


print()
print("--------------------------")
print("PPG Processing Summary")
print("--------------------------")

print(
    "Total windows:",
    number_of_windows
)

print(
    "Valid windows:",
    len(valid_ratios)
)

print(
    "Rejected windows:",
    len(rejected_windows)
)

if len(valid_ratios) > 0:

    average_r = np.mean(valid_ratios)

    print(
        "Average R:",
        round(average_r, 4)
    )

    print(
        "Minimum R:",
        round(np.min(valid_ratios), 4)
    )

    print(
        "Maximum R:",
        round(np.max(valid_ratios), 4)
    )



# REFERENCE SpO2


reference_spo2_start = 96
reference_spo2_end = 97

print()
print("--------------------------")
print("REFERENCE SpO2")
print("--------------------------")

print(
    "Reference SpO2 at start:",
    reference_spo2_start,
    "%"
)

print(
    "Reference SpO2 at end:",
    reference_spo2_end,
    "%"
)

print()
print(
    "Reference SpO2 range:",
    f"{reference_spo2_start}-{reference_spo2_end}%"
)

print()
print(
    "Note: Reference SpO2 values are"
)

print(
    "start/end measurements from the dataset."
)

print(
    "They are not continuous ground-truth"
)

print(
    "SpO2 values for every PPG window."
)