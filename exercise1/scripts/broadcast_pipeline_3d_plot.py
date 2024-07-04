import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Load the data
broadcast_fixed_core = pd.read_csv('/Users/vishal/Documents/broadcast_fixed_core.txt', header=0, names=["Size", "Avg Latency(us)", "Min Latency(us)", "Max Latency(us)", "Iterations", "NP_total", "ALGO", "ALGO_NAME"])

# Convert ALGO column to integer
broadcast_fixed_core['ALGO'] = broadcast_fixed_core['ALGO'].astype(int)

# Print unique values in ALGO column to verify
print("Unique values in ALGO column:", broadcast_fixed_core['ALGO'].unique())

# Filter data for pipeline algorithm (assuming ALGO 3 represents the pipeline algorithm)
pipeline_data = broadcast_fixed_core[broadcast_fixed_core['ALGO'] == 3]

# Extract relevant columns
num_processes = pipeline_data['NP_total'].astype(int).to_numpy()
message_size = pipeline_data['Size'].astype(int).to_numpy()
latency = pipeline_data['Avg Latency(us)'].astype(float).to_numpy()

# Add small jitter to avoid collinearity
num_processes = num_processes + np.random.normal(0, 0.1, size=num_processes.shape)
message_size = message_size + np.random.normal(0, 0.1, size=message_size.shape)

# Remove duplicates by creating a dataframe and dropping duplicates, then converting back to numpy arrays
df = pd.DataFrame({
    'num_processes': num_processes,
    'message_size': message_size,
    'latency': latency
}).drop_duplicates()

num_processes = df['num_processes'].to_numpy()
message_size = df['message_size'].to_numpy()
latency = df['latency'].to_numpy()

# Check lengths of the arrays
print(f"Number of processes: {len(num_processes)}")
print(f"Message sizes: {len(message_size)}")
print(f"Latencies: {len(latency)}")

# Ensure there are at least three data points
if len(num_processes) >= 3 and len(message_size) >= 3 and len(latency) >= 3:
    # Create the 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plotting the data
    ax.plot_trisurf(np.log2(num_processes), np.log2(message_size), np.log2(latency), cmap='viridis', edgecolor='none')

    # Set labels
    ax.set_xlabel('Log2(Number of Processes)')
    ax.set_ylabel('Log2(Message Size)')
    ax.set_zlabel('Log2(Latency)')

    ax.set_title('3D Plot of Broadcast Operation with Pipeline Algorithm')

    # Save the plot as a PNG image
    plt.savefig('/Users/vishal/Documents/broadcast_pipeline_3d_plot.png')
    plt.show()
else:
    print("Not enough data points to create a 3D plot.")

