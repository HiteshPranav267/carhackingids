# carhackingids
This project implements a machine learning-based Intrusion Detection System for CAN bus networks, designed for automotive cybersecurity research and education.
---

## 📁 Project Structure

- `01_load_and_label.py` — Loads raw CAN datasets, labels normal and attack frames, and combines them.
- `02_preprocess.py` — Converts hexadecimal fields to integers and prepares the data for ML.
- `03_train_model.py` — Trains a Random Forest classifier on the preprocessed data and saves the model.
- `04_firewall.py` — Real-time CAN firewall that uses the trained model to detect and block attacks.
- `05_can_gui_sender.py` — GUI tool to simulate and send CAN messages (normal and attack types).
- `utils.py` — Utility functions (e.g., hex to int conversion).
- `dataset/` — Folder containing raw and processed CSV files.

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```sh
git clone <your-repo-url>
cd Car-Hacking-Dataset
```

### 2. Install Dependencies

```sh
pip install pandas scikit-learn joblib python-can
```

### 3. Prepare the Dataset

- Place all raw CAN CSV files in the `dataset/` folder.

### 4. Data Processing Pipeline

**a. Combine and Label Data**
```sh
python 01_load_and_label.py
```
- Combines all datasets and labels them as normal or attack.

**b. Preprocess Data**
```sh
python 02_preprocess.py
```
- Converts hex fields to integers and saves `data_preprocessed.csv`.

**c. Train the Model**
```sh
python 03_train_model.py
```
- Trains a Random Forest model and saves it as `can_ids_model.pkl`.

---

## 🚦 Running the Real-Time Firewall

Make sure your CAN interface (e.g., `vcan0` for virtual or `can0` for hardware) is set up.

```sh
python 04_firewall.py
```
- Listens for CAN frames and blocks those detected as attacks.
- Logs results to `firewall_log.csv`.

---

## 🖥️ CAN Message Sender GUI

Simulate CAN traffic (normal and attacks) with a graphical interface.

```sh
python 05_can_gui_sender.py
```
- Select attack mode, frequency, ID range, or enter manual ID/data.
- Sends messages to the CAN bus for testing.

---

## 📝 Notes

- For real hardware, change `channel='vcan0'` to `channel='can0'` in the scripts.
- For Raspberry Pi deployment, ensure you have a CAN HAT (e.g., PiCAN2) and configure the interface as described in the documentation.
- All logs and processed files are saved in the project directory.

---

## 📚 References

- [python-can documentation](https://python-can.readthedocs.io/)
- [scikit-learn documentation](https://scikit-learn.org/)
- [Raspberry Pi CAN setup guide](https://www.raspberrypi.org/forums/viewtopic.php?t=141052)

---

## 🛡️ Disclaimer

This project is for educational and research purposes only. Do not use on vehicles without proper authorization.
