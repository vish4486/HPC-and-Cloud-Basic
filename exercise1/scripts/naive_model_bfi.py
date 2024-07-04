import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Load the fixed broadcast benchmark data
broadcast_fixed_core = pd.read_csv('~/Documents/broadcast_fixed_core.txt')

# Filter the data for the pipeline algorithm (assuming ALGO == 3 for pipeline)
pipeline_data = broadcast_fixed_core[broadcast_fixed_core['ALGO'] == 3]

# Extract the relevant columns
X = pipeline_data['NP_total'].values.reshape(-1, 1)
y = pipeline_data['Avg Latency(us)'].values

# Fit a linear regression model
model = LinearRegression()
model.fit(X, y)

# Make predictions
y_pred = model.predict(X)

# Plot the actual vs predicted latencies
plt.figure(figsize=(10, 6))
plt.plot(X, y, 'bo-', label='Actual Latency')
plt.plot(X, y_pred, 'r--', label='Naive Model Prediction')
plt.xlabel('Number of Processes')
plt.ylabel('Latency (us)')
plt.title('Naive Model - Broadcast Operation with Pipeline Algorithm (Fixed Data)')
plt.legend()
plt.grid(True)
plt.savefig('naive_model_pipeline_fixed.png')
plt.show()

# Print the model coefficients
print(f'Naive Model Coefficients: Intercept = {model.intercept_}, Slope = {model.coef_[0]}')

