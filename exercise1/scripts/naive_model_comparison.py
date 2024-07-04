import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Load the datasets
broadcast_fixed = pd.read_csv('~/Documents/broadcast_fixed_core.txt')
broadcast_full = pd.read_csv('~/Documents/broadcast_full_core.txt')
scatter_fixed = pd.read_csv('~/Documents/scatter_fixed_core.txt')
scatter_full = pd.read_csv('~/Documents/scatter_full_core.txt')

# Define algorithms and their corresponding numbers for broadcast and scatter
algo_names = {
    'broadcast': {0: 'ignore', 2: 'chain', 3: 'pipeline', 5: 'binary_tree'},
    'scatter': {0: 'default', 1: 'basic linear', 2: 'binomial', 3: 'non-blocking linear'}
}

# Plotting function
def plot_with_naive_model(data, algo_dict, title, output_file):
    plt.figure(figsize=(12, 6))

    for algo, name in algo_dict.items():
        algo_data = data[data['ALGO'] == algo]
        if algo_data.empty:
            continue

        X = algo_data['NP_total'].values.reshape(-1, 1)
        y = algo_data['Avg Latency(us)'].values

        # Fit a linear regression model
        model = LinearRegression()
        model.fit(X, y)
        y_pred = model.predict(X)

        plt.plot(X, y, 'o-', label=f'{name} (Actual)')
        plt.plot(X, y_pred, '--', label=f'{name} (Naive Model)')

    plt.xlabel('Number of Processes')
    plt.ylabel('Latency (us)')
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.savefig(output_file)
    plt.show()

# Plot for broadcast_fixed
plot_with_naive_model(broadcast_fixed, algo_names['broadcast'],
                      'Naive Model Comparison - Broadcast Fixed Data',
                      'naive_model_comparison_broadcast_fixed.png')

# Plot for broadcast_full
plot_with_naive_model(broadcast_full, algo_names['broadcast'],
                      'Naive Model Comparison - Broadcast Full Data',
                      'naive_model_comparison_broadcast_full.png')

# Plot for scatter_fixed
plot_with_naive_model(scatter_fixed, algo_names['scatter'],
                      'Naive Model Comparison - Scatter Fixed Data',
                      'naive_model_comparison_scatter_fixed.png')

# Plot for scatter_full
plot_with_naive_model(scatter_full, algo_names['scatter'],
                      'Naive Model Comparison - Scatter Full Data',
                      'naive_model_comparison_scatter_full.png')

