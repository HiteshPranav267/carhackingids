import can
import joblib
import pandas as pd
from datetime import datetime

# Load trained model
model = joblib.load('can_ids_model.pkl')

def preprocess_frame(frame):
    # Pad data to 8 bytes if shorter
    data = list(frame.data) + [0] * (8 - len(frame.data))
    features = [frame.arbitration_id] + data
    return pd.DataFrame([features], columns=['id'] + [f'data[{i}]' for i in range(8)])

def firewall_check(frame):
    features = preprocess_frame(frame)
    prediction = model.predict(features)[0]

    if prediction == 1:
        print(f"[{datetime.now()}] 🚫 Attack detected! Blocking frame: ID={frame.arbitration_id}, DATA={frame.data.hex()}")
        # Optional: log to file
        with open("firewall_log.csv", "a") as log:
             log.write(f"{datetime.now()},{frame.arbitration_id},{frame.data.hex()},BLOCKED\n")
        return False
    else:
        print(f"[{datetime.now()}] ✅ Frame allowed: ID={frame.arbitration_id}, DATA={frame.data.hex()}")
        # Optional: log to file
        with open("firewall_log.csv", "a") as log:
             log.write(f"{datetime.now()},{frame.arbitration_id},{frame.data.hex()},ALLOWED\n")
        return True

def main():
    try:
        bus = can.interface.Bus(channel='vcan0', bustype='socketcan')
        print("🚦 Firewall started. Listening on vcan0...")
        
        while True:
            msg = bus.recv()
            if msg:
                firewall_check(msg)
    
    except KeyboardInterrupt:
        print("\n🛑 Firewall stopped by user.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
