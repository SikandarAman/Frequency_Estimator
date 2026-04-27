import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# PARAMETERS
N = 5

# LOAD LOGGED DATA
df = pd.read_csv("Arduino_Serial.csv")

# Extract columns
t = df["timestamp"].values
x = df["value"].values

# Sampling time (auto-computed from data)
Ts = np.mean(np.diff(t))
fs = 1 / Ts

print(f"Detected Fs: {fs:.2f} Hz")

# STORAGE
time_axis = []
MA1 = []
MA2 = []
tz_est = []
original = []

# ZC STORAGE
zc_region_tz = []
Tc_list = []

# PROCESSING
for k in range(2*N, len(x)):

    W1 = x[k-2*N:k-N]
    W2 = x[k-N:k]

    m1 = np.mean(W1)
    m2 = np.mean(W2)

    MA1.append(m1)
    MA2.append(m2)

    current_time = t[k]
    time_axis.append(current_time)
    original.append(x[k])

    # SIGN CHANGE REGION
    if m1 * m2 < 0:

        den = 2 * (m1 - m2)

        if abs(den) > 1e-12:
            tz = current_time - N*Ts*(1 - (m1 + m2)/den)
            tz_est.append(tz)
            zc_region_tz.append(tz)
        else:
            tz_est.append(np.nan)

    else:
        tz_est.append(np.nan)

        # REGION END → Tc
        if len(zc_region_tz) > 0:
            Tc = np.mean(zc_region_tz)
            Tc_list.append(Tc)
            zc_region_tz = []

# HANDLE LAST REGION
if len(zc_region_tz) > 0:
    Tc = np.mean(zc_region_tz)
    Tc_list.append(Tc)

# CONVERT TO ARRAYS
time_axis = np.array(time_axis)
MA1 = np.array(MA1)
MA2 = np.array(MA2)
tz_est = np.array(tz_est)
original = np.array(original)
Tc_array = np.array(Tc_list)

# VALID ZC
valid = ~np.isnan(tz_est)
tz_plot = tz_est[valid]

# SAVE TABLE
df_out = pd.DataFrame({
    "Time": time_axis,
    "Original_Signal": original,
    "MA1": MA1,
    "MA2": MA2,
    "Estimated_ZC": tz_est
})

df_out.to_csv("processed_zc_output.csv", index=False)

# PLOT
plt.figure(figsize=(10,5))

plt.plot(t, x, label="Original Signal")
plt.plot(time_axis, MA1, label="MA1")
plt.plot(time_axis, MA2, label="MA2")

plt.scatter(tz_plot, np.zeros_like(tz_plot),
            marker='x', color='black', label="Estimated ZC")

plt.scatter(Tc_array, np.zeros_like(Tc_array),
            marker='o', color='red', label="Tc (Avg ZC)", s=70)

plt.xlabel("Time (seconds)")
plt.ylabel("Amplitude")
plt.title("Zero Crossing Detection (From Logged Data)")
plt.legend()
plt.grid(True)

plt.savefig("zc_from_logged_data.png", dpi=300)
plt.show()