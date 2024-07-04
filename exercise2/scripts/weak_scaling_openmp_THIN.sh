#!/bin/bash
#SBATCH --job-name=omp_weak_scaling
#SBATCH --output=/u/dssc/vnigam/HPC/exercise2/results/omp_weak_scaling_output.txt
#SBATCH --error=/u/dssc/vnigam/HPC/exercise2/results/omp_weak_scaling_error.txt
#SBATCH --nodes=2
#SBATCH --time=02:00:00
#SBATCH --partition=THIN
#SBATCH --exclusive

# Load necessary modules
module load openMPI/4.1.5/gnu/

# Compile the code
mpicc -fopenmp -o /u/dssc/vnigam/HPC/exercise2/src/mandelbrot_pgm /u/dssc/vnigam/HPC/exercise2/src/mandelbrot_pgm.c

# Define base parameters
x_L=-2.0
y_L=-2.0
x_R=2.0
y_R=2.0
I_max=255
n_x_base=1000
n_y_base=1000

# Create results file
results_file="/u/dssc/vnigam/HPC/exercise2/results/omp_weak_scaling_THIN.csv"
echo "Threads,Time" > $results_file

# Function to calculate the square root of an integer
int_sqrt() {
    echo "sqrt($1)" | bc
}

# Run with different numbers of OpenMP threads and proportionally increased problem size
for n_threads in {2..64..2}; do
    export OMP_NUM_THREADS=$n_threads
    scaled_n_threads=$(int_sqrt $n_threads)
    n_x=$(($n_x_base * $scaled_n_threads))
    n_y=$(($n_y_base * $scaled_n_threads))
    start_time=$(date +%s%N)
    mpiexec --map-by core -np 1 /u/dssc/vnigam/HPC/exercise2/src/mandelbrot_pgm $n_x $n_y $x_L $y_L $x_R $y_R $I_max
    end_time=$(date +%s%N)
    runtime=$((($end_time - $start_time) / 1000000))
    echo "$n_threads,$runtime" >> $results_file
done

