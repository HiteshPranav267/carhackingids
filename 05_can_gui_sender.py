import tkinter as tk
import threading
import random
import time
import can

ATTACK_MODES = ["Normal", "DoS", "Fuzzy", "Gear", "RPM", "Manual"]

class CANMessageSender:
    def __init__(self, master):
        self.master = master
        master.title("CAN Message Simulator")

        # Frequency input
        tk.Label(master, text="Frequency (msg/sec):").grid(row=0, column=0)
        self.freq_entry = tk.Entry(master)
        self.freq_entry.insert(0, "5")
        self.freq_entry.grid(row=0, column=1)

        # ID range input
        tk.Label(master, text="ID Range (min-max):").grid(row=1, column=0)
        self.id_range_entry = tk.Entry(master)
        self.id_range_entry.insert(0, "100-200")
        self.id_range_entry.grid(row=1, column=1)

        # Attack mode dropdown
        tk.Label(master, text="Attack Mode:").grid(row=2, column=0)
        self.attack_mode = tk.StringVar(value=ATTACK_MODES[0])
        self.attack_menu = tk.OptionMenu(master, self.attack_mode, *ATTACK_MODES, command=self.toggle_manual_fields)
        self.attack_menu.grid(row=2, column=1)

        # Manual ID and Data input
        tk.Label(master, text="Manual ID:").grid(row=3, column=0)
        self.manual_id_entry = tk.Entry(master, state=tk.DISABLED)
        self.manual_id_entry.grid(row=3, column=1)

        tk.Label(master, text="Manual Data (comma sep, 8 bytes):").grid(row=4, column=0)
        self.manual_data_entry = tk.Entry(master, state=tk.DISABLED)
        self.manual_data_entry.grid(row=4, column=1)

        # Start and Stop buttons
        self.start_btn = tk.Button(master, text="Start Sending", command=self.start_sending)
        self.start_btn.grid(row=5, column=0, pady=10)

        self.stop_btn = tk.Button(master, text="Stop", command=self.stop_sending, state=tk.DISABLED)
        self.stop_btn.grid(row=5, column=1, pady=10)

        self.running = False
        self.thread = None

        # Setup CAN bus (vcan0 or can0)
        self.bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

    def toggle_manual_fields(self, *args):
        if self.attack_mode.get() == "Manual":
            self.manual_id_entry.config(state=tk.NORMAL)
            self.manual_data_entry.config(state=tk.NORMAL)
        else:
            self.manual_id_entry.config(state=tk.DISABLED)
            self.manual_data_entry.config(state=tk.DISABLED)

    def generate_random_frame(self, min_id, max_id):
        can_id = random.randint(min_id, max_id)
        data = [random.randint(0, 255) for _ in range(8)]
        return can.Message(arbitration_id=can_id, data=data, is_extended_id=False)

    def generate_attack_frame(self, mode):
        # You can customize these for each attack type
        if mode == "DoS":
            can_id = 0x000  # Flood with lowest ID
            data = [0xFF] * 8
        elif mode == "Fuzzy":
            can_id = random.randint(0, 0x7FF)
            data = [random.randint(0, 255) for _ in range(8)]
        elif mode == "Gear":
            can_id = 0x123  # Example gear ID
            data = [0x01] * 8
        elif mode == "RPM":
            can_id = 0x456  # Example RPM ID
            data = [0xFF, 0xFF, 0, 0, 0, 0, 0, 0]
        else:  # Normal
            can_id = random.randint(100, 200)
            data = [random.randint(0, 255) for _ in range(8)]
        return can.Message(arbitration_id=can_id, data=data, is_extended_id=False)

    def send_loop(self):
        try:
            freq = float(self.freq_entry.get())
            delay = 1 / freq
            min_id, max_id = map(int, self.id_range_entry.get().split("-"))
            mode = self.attack_mode.get()

            while self.running:
                if mode == "Manual":
                    try:
                        can_id = int(self.manual_id_entry.get(), 0)
                        data = [int(x) for x in self.manual_data_entry.get().split(",")]
                        if len(data) != 8:
                            print("Manual data must be 8 bytes.")
                            time.sleep(delay)
                            continue
                        msg = can.Message(arbitration_id=can_id, data=data, is_extended_id=False)
                    except Exception as e:
                        print("Manual input error:", e)
                        time.sleep(delay)
                        continue
                elif mode == "Normal":
                    msg = self.generate_random_frame(min_id, max_id)
                else:
                    msg = self.generate_attack_frame(mode)

                try:
                    self.bus.send(msg)
                    print(f"Sent: {msg}")
                except can.CanError as e:
                    print("Send failed:", e)
                time.sleep(delay)
        except ValueError:
            print("Invalid input. Please enter numbers correctly.")

    def start_sending(self):
        self.running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.thread = threading.Thread(target=self.send_loop)
        self.thread.start()

    def stop_sending(self):
        self.running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = CANMessageSender(root)
    root.mainloop()
