#!/bin/bash
#SBATCH --job-name=mandelbrot_job     # Job name
#SBATCH --output=mandelbrot_output.txt # Output file
#SBATCH --error=mandelbrot_error.txt   # Error file
#SBATCH --ntasks=4                     # Number of MPI tasks
#SBATCH --cpus-per-task=4              # Number of OpenMP threads per MPI task
#SBATCH --time=01:00:00                # Time limit hrs:min:sec
#SBATCH --partition=EPYC               # Partition name

# Load the MPI module (adjust based on your system)
module load openMPI/4.1.5/gnu



# Navigate to the directory where the source code is located
cd /u/dssc/vnigam/HPC/exercise2/src/

# Compile the Mandelbrot program
mpicc -fopenmp -o mandelbrot_pgm mandelbrot_pgm.c

# Run the Mandelbrot program
mpirun -np 4 ./mandelbrot_pgm 1024 1024 -2.0 -1.5 1.0 1.5 1000

