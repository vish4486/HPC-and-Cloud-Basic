import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

def fit_and_plot_naive_model(file_name, algo, algo_name, output_file):
    # Load the data
    data = pd.read_csv(file_name)
    
    # Filter the data for the specific algorithm
    algo_data = data[data['ALGO'] == algo]
    
    # Extract the relevant columns
    X = algo_data['NP_total'].values.reshape(-1, 1)
    y = algo_data['Avg Latency(us)'].values
    
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
    plt.title(f'Naive Model - {file_name} with {algo_name}')
    plt.legend()
    plt.grid(True)
    plt.savefig(output_file)
    plt.show()
    
    # Print the model coefficients
    print(f'{algo_name} Naive Model Coefficients: Intercept = {model.intercept_}, Slope = {model.coef_[0]}')

# Define the files and algorithms
files_algorithms = {
    'broadcast_fixed_core.txt': {3: 'Pipeline'},
    'broadcast_full_core.txt': {3: 'Pipeline'},
    'scatter_fixed_core.txt': {2: 'Binomial'},
    'scatter_full_core.txt': {2: 'Binomial'}
}

# Loop over files and algorithms
for file, algos in files_algorithms.items():
    for algo, algo_name in algos.items():
        output_file = f'naive_model_{file.split(".")[0]}_{algo_name}.png'
        fit_and_plot_naive_model(file, algo, algo_name, output_file)

