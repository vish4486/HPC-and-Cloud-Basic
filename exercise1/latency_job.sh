#!/bin/bash
#SBATCH --job-name=osu_latency_test
#SBATCH --output=osu_latency_test.out
#SBATCH --error=osu_latency_test.err
#SBATCH --ntasks=2
#SBATCH --cpus-per-task=1
#SBATCH --nodes=2
#SBATCH --time=00:10:00
#SBATCH --partition=EPYC

module load openMPI/4.1.5/gnu

# Function to run osu_latency and extract latency value
run_latency_test() {
    local cpu_set=$1
    local output_file=$2
    mpirun --mca mtl ^ofi --oversubscribe --bind-to core --cpu-set $cpu_set ~/HPC/exercise1/osu-micro-benchmarks-7.0.1/c/mpi/pt2pt/osu_latency > ${output_file} 2>&1
    if grep -q "hwloc_set_cpubind returned" ${output_file}; then
        echo "Binding failed for cpu-set ${cpu_set}" >> osu_latency_test.err
        return 1
    fi
    latency=$(awk '/^[0-9]+/ {print $2; exit}' ${output_file})
    echo ${latency}
}

# Run latency tests for different core regions
latency_same_ccx=$(run_latency_test "0,1" "latency_same_ccx.txt")
latency_same_ccd_diff_ccx=$(run_latency_test "0,8" "latency_same_ccd_diff_ccx.txt")
latency_same_numa=$(run_latency_test "0,16" "latency_same_numa.txt")
latency_same_socket=$(run_latency_test "0,32" "latency_same_socket.txt")
latency_diff_socket=$(run_latency_test "0,64" "latency_diff_socket.txt")
latency_diff_node=$(run_latency_test "0,epyc002:0" "latency_diff_node.txt")

# Print the latency values
echo "Latency Same CCX: ${latency_same_ccx} us"
echo "Latency Same CCD, Different CCX: ${latency_same_ccd_diff_ccx} us"
echo "Latency Same NUMA: ${latency_same_numa} us"
echo "Latency Same Socket: ${latency_same_socket} us"
echo "Latency Different Socket: ${latency_diff_socket} us"
echo "Latency Different Node: ${latency_diff_node} us"

