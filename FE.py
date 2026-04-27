import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# PARAMETERS
f_signal = 50
duration = 0.05 

# TUNABLE FACTORS
fs = 5000
N = 20

Ts = 1/fs

# TIME VECTOR
t = np.arange(0, duration, Ts)

# NOISE
noise_std = 0.1
noise = np.random.normal(0, noise_std, len(t))

# SIGNAL
x = np.sin(2*np.pi*f_signal*t) + noise

# STORAGE
time_axis = []
MA1 = []
MA2 = []
tz_est = []
original = []

# NEW STORAGE
zc_region_tz = []   # store tz values in region
Tc_list = []

# WINDOWS PROCESSING
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

        # Numerical stability check
        if abs(den) > 1e-12:
            tz = current_time - N*Ts*(1 - (m1 + m2)/den)
            tz_est.append(tz)
            zc_region_tz.append(tz)
        else:
            tz_est.append(np.nan)

    else:
        tz_est.append(np.nan)

        # Region ended → compute Tc
        if len(zc_region_tz) > 0:
            Tc = np.mean(zc_region_tz)
            Tc_list.append(Tc)
            zc_region_tz = []

# HANDLE last region
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

# FILTER valid ZC points
valid = ~np.isnan(tz_est)
tz_plot = tz_est[valid]

# SAVE TABLE
df = pd.DataFrame({
    "Time": time_axis,
    "Original_Signal": original,
    "MA1": MA1,
    "MA2": MA2,
    "Estimated_ZC": tz_est
})

df.to_csv("dual_moving_average_zc_estimation.csv", index=False)

# PLOT
plt.figure(figsize=(10,5))

plt.plot(t, x, label="Original Signal")
plt.plot(time_axis, MA1, label="MA1")
plt.plot(time_axis, MA2, label="MA2")

# Estimated ZC points
plt.scatter(tz_plot, np.zeros_like(tz_plot), 
            marker='x', color='black', label="Estimated ZC")

# # Tc points (average of ZC region)
plt.scatter(Tc_array, np.zeros_like(Tc_array), 
            marker='o', color ='red', label="Tc (Avg of ZC)", s=70)

plt.xlabel("Time (seconds)")
plt.ylabel("Amplitude")
plt.title("Zero Crossing Detection using Dual Moving Averages (Corrected)")
plt.legend()
plt.grid(True)

plt.savefig("zero_crossing_with_Tc.png", dpi=300)
plt.show()