import random

def get_heart_rate():
    return random.randint(60, 100)

def get_temperature():
    return round(random.uniform(36.5, 37.5), 1)

def get_spo2():
    return random.randint(95, 100)

heart_rate = get_heart_rate()
temperature= get_temperature()
spo2 = get_spo2()

def check_heart_rate(heart_rate):
    print(f"Heart Rate : {heart_rate} BPM")

    if heart_rate < 60:
        print("Status : Low Heart Rate")
        print("Advice : Please consult a doctor if you feel dizzy or weak.")
    elif heart_rate <= 100:
        print("Status : Normal")
        print("Advice : Your heart rate is within the healthy range.")
    else:
        print("Status : High Heart Rate")
        print("Advice : Please sit down, rest, and consult a doctor if it remains high.")

def check_temperature(temperature):
    print(f"\nTemperature : {temperature} °C")

    if temperature < 36.5:
        print("Status : Low Temperature")
        print("Advice : Keep yourself warm and monitor your temperature.")
    elif temperature <= 37.5:
        print("Status : Normal")
        print("Advice : Your body temperature is normal.")
    else:
        print("Status : Fever")
        print("Advice : Stay hydrated and consult a doctor if the fever persists.")

def check_spo2(spo2):
    print(f"\nSpO₂ : {spo2} %")

    if spo2 < 95:
        print("Status : Low Oxygen Level")
        print("Advice : Please seek medical attention if it continues to stay low.")
    elif spo2 <= 100:
        print("Status : Normal")
        print("Advice : Your oxygen level is normal.")
    else:
        print("Status : Invalid Reading")
        print("Advice : Please check the sensor.")

def overall_health_status(heart_rate, temperature, spo2):
    print("\nOverall Health Status")

    if heart_rate >= 60 and heart_rate <= 100 and temperature >= 36.5 and temperature <= 37.5 and spo2 >= 95:
        print("All vitals are normal.")
    else:
        print("One or more vitals need attention.")
while True:
    print("\n=== VitaBand Health Monitor ===")

    heart_rate = get_heart_rate()
    temperature = get_temperature()
    spo2 = get_spo2()

    check_heart_rate(heart_rate)
    check_temperature(temperature)
    check_spo2(spo2)
    overall_health_status(heart_rate, temperature, spo2)
    choice = input("\nDo you want to check again? (yes/no): ")
    if choice.lower() == "no":
        print("\nThank you for using VitaBand!")
        print("Stay Healthy ")
        break

    