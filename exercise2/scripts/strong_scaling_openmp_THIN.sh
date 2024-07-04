#!/bin/bash
#SBATCH --job-name=omp_strong_scaling
#SBATCH --output=/u/dssc/vnigam/HPC/exercise2/results/omp_strong_scaling_output.txt
#SBATCH --error=/u/dssc/vnigam/HPC/exercise2/results/omp_strong_scaling_error.txt
#SBATCH --nodes=2
#SBATCH --time=02:00:00
#SBATCH --partition=THIN
#SBATCH --exclusive

# Load necessary modules
module load openMPI/4.1.5/gnu/

# Compile the code
mpicc -fopenmp -o /u/dssc/vnigam/HPC/exercise2/src/mandelbrot_pgm /u/dssc/vnigam/HPC/exercise2/src/mandelbrot_pgm.c

# Set parameters
n_x=1000
n_y=1000
x_L=-2.0
y_L=-2.0
x_R=2.0
y_R=2.0
I_max=255

# Create results file
results_file="/u/dssc/vnigam/HPC/exercise2/results/omp_strong_scaling_THIN.csv"
echo "Threads,Time" > $results_file

# Run with different numbers of OpenMP threads
for n_threads in {2..64..2}; do
    export OMP_NUM_THREADS=$n_threads
    start_time=$(date +%s%N)
    mpiexec --map-by core -np 1 /u/dssc/vnigam/HPC/exercise2/src/mandelbrot_pgm $n_x $n_y $x_L $y_L $x_R $y_R $I_max
    end_time=$(date +%s%N)
    runtime=$((($end_time - $start_time) / 1000000))
    echo "$n_threads,$runtime" >> $results_file
done

