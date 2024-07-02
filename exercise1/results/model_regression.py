import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Data from the benchmarks
neighbor_latency = {
    2: 0.48,
    4: 0.47,
    8: 0.47,
    16: 0.46,
    32: 0.67,
    64: 0.63,
    128: 1.00,
    256: 1.11,
    512: 1.34,
    1024: 1.58,
    2048: 2.12,
    4096: 3.09,
    8192: 4.90,
    16384: 7.77,
    32768: 13.30,
    65536: 24.21,
    131072: 45.77,
    262144: 26.01,
    524288: 47.99,
    1048576: 98.31,
    2097152: 253.25,
    4194304: 580.07
}

distant_latency = {
    2: 0.46,
    4: 0.46,
    8: 0.47,
    16: 0.47,
    32: 0.69,
    64: 0.62,
    128: 1.04,
    256: 1.10,
    512: 1.34,
    1024: 1.57,
    2048: 2.18,
    4096: 3.18,
    8192: 5.04,
    16384: 8.06,
    32768: 13.99,
    65536: 25.77,
    131072: 48.30,
    262144: 25.68,
    524288: 47.52,
    1048576: 98.42,
    2097152: 250.75,
    4194304: 579.65
}

# Extract the latencies for small message sizes to estimate the base latency and alpha
x_data = np.log2(np.array(list(neighbor_latency.keys())))
y_data = np.array(list(neighbor_latency.values()))

# Define the model
def latency_model(x, base_latency, alpha):
    return base_latency + alpha * x

# Fit the model
popt, pcov = curve_fit(latency_model, x_data, y_data)

base_latency_est = popt[0]
alpha_est = popt[1]

print(f"Estimated Base Latency: {base_latency_est}")
print(f"Estimated Alpha: {alpha_est}")

# Plot the results
x_fit = np.linspace(min(x_data), max(x_data), 100)
y_fit = latency_model(x_fit, base_latency_est, alpha_est)

plt.scatter(x_data, y_data, label="Observed Latency")
plt.plot(x_fit, y_fit, label="Fitted Model", color='r')
plt.xlabel('log2(Message Size)')
plt.ylabel('Latency (us)')
plt.legend()
plt.show()

