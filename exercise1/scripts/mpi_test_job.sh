#!/bin/bash
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=128
#SBATCH --time=00:10:00
#SBATCH --partition=EPYC  # Modify as needed

module load openMPI/4.1.5/gnu
MPI_DIR="/u/dssc/vnigam/HPC/exercise1/osu-micro-benchmarks-7.0.1/c/mpi/collective"
mpirun --mca coll_tuned_use_dynamic_rules true --mca coll_tuned_bcast_algorithm 0 --map-by ppr:128:node $MPI_DIR/osu_bcast -m 1,2,4,8 -x 10 -i 50

