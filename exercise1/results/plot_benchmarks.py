import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# Function to create pivot table
def create_pivot_table(data, operation, benchmark_type):
    subset = data[(data['Operation'] == operation) & (data['BenchmarkType'] == benchmark_type)]
    print(f"Data subset for {operation} - {benchmark_type}:\n", subset.head())
    numeric_columns = ['Avg Latency(us)', 'Min Latency(us)', 'Max Latency(us)', 'Iterations']
    subset = subset.groupby(['Size', 'NP_total'])[numeric_columns].mean().reset_index()
    print(f"Grouped subset for {operation} - {benchmark_type}:\n", subset.head())
    pivot_table = subset.pivot(index='Size', columns='NP_total', values='Avg Latency(us)')
    print(f"Pivot table for {operation} - {benchmark_type}:\n", pivot_table.head())
    return pivot_table

# Function to plot 3D heatmap
def plot_3d_heatmap(data, operation, benchmark_type, ax):
    pivot_table = create_pivot_table(data, operation, benchmark_type)
    if pivot_table.empty:
        print(f"No data available for {operation} - {benchmark_type}")
        return
    X, Y = np.meshgrid(pivot_table.columns, pivot_table.index)
    Z = pivot_table.values
    print(f"Meshgrid X for {operation} - {benchmark_type}:\n", X)
    print(f"Meshgrid Y for {operation} - {benchmark_type}:\n", Y)
    print(f"Values Z for {operation} - {benchmark_type}:\n", Z)
    surf = ax.plot_surface(X, Y, Z, cmap='viridis')
    ax.set_xlabel('Total NP')
    ax.set_ylabel('Message Size')
    ax.set_zlabel('Avg Latency (us)')
    ax.set_title(f'{operation.capitalize()} {benchmark_type.capitalize()} Latency')
    plt.colorbar(surf, ax=ax, shrink=0.5, aspect=5)

# Function to plot line plots
def plot_line_plot(data, operation, benchmark_type, ax):
    subset = data[(data['Operation'] == operation) & (data['BenchmarkType'] == benchmark_type)]
    if subset.empty:
        print(f"No data available for {operation} - {benchmark_type}")
        return
    for alg_name in subset['ALGO_NAME'].unique():
        alg_data = subset[subset['ALGO_NAME'] == alg_name]
        ax.plot(alg_data['NP_total'], alg_data['Avg Latency(us)'], label=alg_name)
    ax.set_xlabel('Number of Cores')
    ax.set_ylabel('Avg Latency (us)')
    ax.set_title(f'{operation.capitalize()} {benchmark_type.capitalize()} Latency')
    ax.legend()

# Load the data
broadcast_fixed = pd.read_csv('/Users/vishal/Documents/broadcast_fixed.txt')
broadcast_full = pd.read_csv('/Users/vishal/Documents/broadcast_full.txt')
scatter_fixed = pd.read_csv('/Users/vishal/Documents/scatter_fixed.txt')
scatter_full = pd.read_csv('/Users/vishal/Documents/scatter_full.txt')

# Add operation and benchmark type columns
broadcast_fixed['Operation'] = 'broadcast'
broadcast_fixed['BenchmarkType'] = 'fixed'
broadcast_full['Operation'] = 'broadcast'
broadcast_full['BenchmarkType'] = 'full'
scatter_fixed['Operation'] = 'scatter'
scatter_fixed['BenchmarkType'] = 'fixed'
scatter_full['Operation'] = 'scatter'
scatter_full['BenchmarkType'] = 'full'

# Combine data
combined_data = pd.concat([broadcast_fixed, broadcast_full, scatter_fixed, scatter_full], ignore_index=True)
print("Loaded data:\n", combined_data.head())

# Create the plot
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10), subplot_kw={'projection': '3d'})

# Plot 3D heatmaps
plot_3d_heatmap(combined_data, 'broadcast', 'fixed', ax1)
plot_3d_heatmap(combined_data, 'broadcast', 'full', ax2)
plot_3d_heatmap(combined_data, 'scatter', 'fixed', ax3)
plot_3d_heatmap(combined_data, 'scatter', 'full', ax4)

plt.tight_layout()
plt.savefig('benchmark_3d_heatmaps.png')
plt.show()

# Create line plots
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

# Plot line plots
plot_line_plot(combined_data, 'broadcast', 'fixed', ax1)
plot_line_plot(combined_data, 'broadcast', 'full', ax2)
plot_line_plot(combined_data, 'scatter', 'fixed', ax3)
plot_line_plot(combined_data, 'scatter', 'full', ax4)

plt.tight_layout()
plt.savefig('benchmark_line_plots.png')
plt.show()

