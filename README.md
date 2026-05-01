# Frequency Estimator

A frequency estimation system for periodic signals using **Dual Moving Average (DMA) Zero-Crossing Detection**, implemented in Python (simulation & logging) and Arduino (hardware acquisition).

## How It Works

Two sliding windows of samples compute consecutive moving averages (MA1, MA2). A sign change between them indicates a zero-crossing, and the exact crossing time is interpolated algebraically. Frequency is then estimated from the period between crossings. This approach is robust to Gaussian noise and avoids false triggers common in simple threshold detectors.

## Files

| File | Description |
|------|-------------|
| `FE.py` | Core simulation on a synthetic noisy 50 Hz sine wave |
| `ZCD.py` | Standalone zero-crossing detection module |
| `FE_Log_File.py` | Runs the estimator on a saved CSV log |
| `Log_Generator.py` | Generates synthetic log files for offline testing |
| `FE_Arduino.ino` | Arduino sketch — samples analog pin A0 at 5 kHz over Serial |
| `Arduino_Print_Value.ino` | Utility sketch for inspecting raw ADC values |
| `Arduino_Serial.csv` | Sample data captured from Arduino |
| `Python_Serial.csv` | Real-time frequency estimation results captured from the Python serial reader |

## Usage

**Simulation:**
```bash
pip install numpy pandas matplotlib
python FE.py
```

**Real Hardware:**
1. Flash `FE_Arduino.ino` to your Arduino with the signal on pin A0.
2. Run `FE_Log_File.py` to read and estimate frequency from the serial stream.

## Languages
- Python 92% · C++ (Arduino) 8%
