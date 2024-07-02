#!/bin/bash
#SBATCH --job-name=osu_latency_test
#SBATCH --output=osu_latency_test.out
#SBATCH --error=osu_latency_test.err
#SBATCH --ntasks=2
#SBATCH --nodes=1
#SBATCH --time=00:10:00
#SBATCH --partition=EPYC
#SBATCH --exclusive

module load openMPI/4.1.5/gnu

# Run the latency test for different CPU sets
mpirun --mca btl ^openib --mca mtl ^ofi -np 2 --cpu-set 0,1 ~/HPC/exercise1/osu-micro-benchmarks-7.0.1/c/mpi/pt2pt/osu_latency > latency_same_ccx.txt
mpirun --mca btl ^openib --mca mtl ^ofi -np 2 --cpu-set 0,8 ~/HPC/exercise1/osu-micro-benchmarks-7.0.1/c/mpi/pt2pt/osu_latency > latency_same_ccd_diff_ccx.txt
mpirun --mca btl ^openib --mca mtl ^ofi -np 2 --cpu-set 0,16 ~/HPC/exercise1/osu-micro-benchmarks-7.0.1/c/mpi/pt2pt/osu_latency > latency_same_numa.txt
mpirun --mca btl ^openib --mca mtl ^ofi -np 2 --cpu-set 0,32 ~/HPC/exercise1/osu-micro-benchmarks-7.0.1/c/mpi/pt2pt/osu_latency > latency_same_socket.txt
mpirun --mca btl ^openib --mca mtl ^ofi -np 2 --cpu-set 0,64 ~/HPC/exercise1/osu-micro-benchmarks-7.0.1/c/mpi/pt2pt/osu_latency > latency_diff_socket.txt
mpirun --mca btl ^openib --mca mtl ^ofi -np 2 --cpu-set epyc002:0,epyc002:8 ~/HPC/exercise1/osu-micro-benchmarks-7.0.1/c/mpi/pt2pt/osu_latency > latency_diff_node.txt

