#!/bin/bash
#SBATCH --job-name=plot_benchmarks
#SBATCH --output=/u/dssc/vnigam/HPC/exercise1/results/plot_output.log
#SBATCH --error=/u/dssc/vnigam/HPC/exercise1/results/plot_error.log
#SBATCH --time=01:00:00
#SBATCH --partition=EPYC
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1


# Load conda module
module load conda/23.3.1
# Create a virtual environment
python -m venv myenv
source myenv/bin/activate

# Create a new conda environment and install packages
conda create -n myenv python=3.9 seaborn pandas matplotlib -y
source activate myenv

# Run the Python script
python /u/dssc/vnigam/HPC/exercise1/results/plot_benchmarks.py

