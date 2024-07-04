import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Load the benchmark data
broadcast_fixed_core = pd.read_csv('~/Documents/broadcast_fixed_core.txt')
broadcast_full_core = pd.read_csv('~/Documents/broadcast_full_core.txt')
scatter_fixed_core = pd.read_csv('~/Documents/scatter_fixed_core.txt')
scatter_full_core = pd.read_csv('~/Documents/scatter_full_core.txt')

# Define a function to fit a multiple linear regression model and print the coefficients
def fit_and_print_coefficients(data, operation_name):
    X = data[['NP_total', 'Size']].values
    y = data['Avg Latency(us)'].values
    
    model = LinearRegression()
    model.fit(X, y)
    
    # Print the model coefficients
    print(f'{operation_name}: Intercept = {model.intercept_}, Coefficients = {model.coef_}')
    
    return model

# Fit models for broadcast fixed and full data
broadcast_fixed_model = fit_and_print_coefficients(broadcast_fixed_core, 'Broadcast Fixed')
broadcast_full_model = fit_and_print_coefficients(broadcast_full_core, 'Broadcast Full')

# Fit models for scatter fixed and full data
scatter_fixed_model = fit_and_print_coefficients(scatter_fixed_core, 'Scatter Fixed')
scatter_full_model = fit_and_print_coefficients(scatter_full_core, 'Scatter Full')

# Define a function to plot the actual vs predicted latencies
def plot_actual_vs_predicted(data, model, operation_name, file_name):
    X = data[['NP_total', 'Size']].values
    y = data['Avg Latency(us)'].values
    y_pred = model.predict(X)
    
    plt.figure(figsize=(10, 6))
    plt.scatter(X[:, 0], y, color='blue', label='Actual Latency')
    plt.scatter(X[:, 0], y_pred, color='red', label='Predicted Latency', alpha=0.5)
    plt.xlabel('Number of Processes')
    plt.ylabel('Latency (us)')
    plt.title(f'{operation_name} - Actual vs Predicted Latency')
    plt.legend()
    plt.grid(True)
    plt.savefig(file_name)
    plt.show()

# Plot results for broadcast fixed and full data
plot_actual_vs_predicted(broadcast_fixed_core, broadcast_fixed_model, 'Broadcast Fixed', 'broadcast_fixed_model.png')
plot_actual_vs_predicted(broadcast_full_core, broadcast_full_model, 'Broadcast Full', 'broadcast_full_model.png')

# Plot results for scatter fixed and full data
plot_actual_vs_predicted(scatter_fixed_core, scatter_fixed_model, 'Scatter Fixed', 'scatter_fixed_model.png')
plot_actual_vs_predicted(scatter_full_core, scatter_full_model, 'Scatter Full', 'scatter_full_model.png')

