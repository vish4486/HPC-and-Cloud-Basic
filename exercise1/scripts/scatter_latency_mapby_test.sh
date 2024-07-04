#!/bin/bash
#SBATCH --ntasks-per-node=48
#SBATCH --exclusive
#SBATCH --partition=GPU
#SBATCH --job-name=osu_benchmark_scatter
#SBATCH --cpus-per-task=1
#SBATCH --nodes=2
#SBATCH --time=02:00:00
#SBATCH --output=output_scatter.log
#SBATCH --error=error_scatter.log

# Load the correct MPI module
module load openMPI/4.1.5/gnu

# Usage check
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <map_by>"
    exit 1
fi

map_by=$1

# Define the number of MPI processes per node
TASKS_PER_NODE=128

# Directory where the MPI executables are located
MPI_DIR="/u/dssc/vnigam/HPC/exercise1/osu-micro-benchmarks-7.0.1/c/mpi/collective"

# Define warm-up and total iteration counts
WARMUP_ITERATIONS=500
TOTAL_ITERATIONS=25000

# Scatter algorithms to test
declare -A algorithms
algorithms=(
    [default]=0
    [basic_linear]=1
    [binomial]=2
    [non_blocking_linear]=3
)

# Initialize output file for the entire run
OUTPUT_FILE="scatter_${map_by}_$(date +%Y%m%d%H%M%S).txt"
echo "Test Type,Message Size,Avg Latency(us)" > "$OUTPUT_FILE"

# Loop over algorithms and run tests
for alg_name in "${!algorithms[@]}"; do
    alg_num="${algorithms[$alg_name]}"
    
    sizes=(2)  # Fixed size for the test
    for np in 2; do  # Two processes for latency test
        TEMP_OUTPUT=$(mktemp)
        mpirun --mca coll_tuned_use_dynamic_rules true --mca coll_tuned_scatter_algorithm $alg_num --map-by $map_by -np $np $MPI_DIR/osu_scatter -m ${sizes[0]} -x $WARMUP_ITERATIONS -i $TOTAL_ITERATIONS > $TEMP_OUTPUT
        if [ $? -ne 0 ]; then
            echo "Error running mpirun for $alg_name with size ${sizes[0]}, np $np, check output file for details."
        else
            # Parse the output and format it according to the specified layout
            awk -v size="${sizes[0]}" -v np="$np" -v algo="$alg_num" -v alg_name="$alg_name" -v map_by="$map_by" \
            'BEGIN { OFS=","; seen=0; min_latency="N/A"; max_latency="N/A" } 
             /^[0-9]+/ && seen == 0 { 
                avg_latency=$2; 
                min_latency=$2;
                max_latency=$2; 
                seen=1 
             } 
             /^[0-9]+/ && seen == 1 { 
                if ($2 < min_latency) min_latency=$2;
                if ($2 > max_latency) max_latency=$2;
             } 
             END { 
                if (seen == 1) print map_by, size, avg_latency
             }' $TEMP_OUTPUT >> "$OUTPUT_FILE"
        fi
        rm $TEMP_OUTPUT  # Clean up temporary file
    done
done

