import random
def get_heart_rate():
    heart_rate = random.randint(60, 100)
    return heart_rate
print("❤️ VitaBand Health Monitor")
print(f"Current Heart Rate:{get_heart_rate()} BPM")