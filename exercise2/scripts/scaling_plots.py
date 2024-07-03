import pandas as pd
import matplotlib.pyplot as plt

# Function to plot scaling data
def plot_scaling(file_path, x_label, y_label, title, output_file):
    df = pd.read_csv(file_path)
    plt.figure(figsize=(10, 6))
    plt.plot(df.iloc[:, 0], df.iloc[:, 1], marker='o', linestyle='-', color='b')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.grid(True)
    plt.savefig(output_file)
    plt.show()

# Plot OpenMP Strong Scaling
plot_scaling(
    '/u/dssc/vnigam/HPC/exercise2/results/omp_strong_scaling.csv',
    'Number of OpenMP Threads',
    'Execution Time (ms)',
    'OpenMP Strong Scaling',
    '/u/dssc/vnigam/HPC/exercise2/results/omp_strong_scaling_plot.png'
)

# Plot OpenMP Weak Scaling
plot_scaling(
    '/u/dssc/vnigam/HPC/exercise2/results/omp_weak_scaling.csv',
    'Number of OpenMP Threads',
    'Execution Time (ms)',
    'OpenMP Weak Scaling',
    '/u/dssc/vnigam/HPC/exercise2/results/omp_weak_scaling_plot.png'
)

# Plot MPI Strong Scaling
plot_scaling(
    '/u/dssc/vnigam/HPC/exercise2/results/mpi_strong_scaling.csv',
    'Number of MPI Tasks',
    'Execution Time (ms)',
    'MPI Strong Scaling',
    '/u/dssc/vnigam/HPC/exercise2/results/mpi_strong_scaling_plot.png'
)

# Plot MPI Weak Scaling
plot_scaling(
    '/u/dssc/vnigam/HPC/exercise2/results/mpi_weak_scaling.csv',
    'Number of MPI Tasks',
    'Execution Time (ms)',
    'MPI Weak Scaling',
    '/u/dssc/vnigam/HPC/exercise2/results/mpi_weak_scaling_plot.png'
)
