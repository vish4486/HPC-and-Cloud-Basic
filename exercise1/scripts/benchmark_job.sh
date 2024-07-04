#!/bin/bash
#SBATCH --ntasks-per-node=128
#SBATCH --exclusive
#SBATCH --partition=EPYC
#SBATCH --job-name=osu_benchmark
#SBATCH --cpus-per-task=1
#SBATCH --nodes=2
#SBATCH --time=02:00:00
#SBATCH --output=output.log
#SBATCH --error=error.log

# Load the correct MPI module
module load openMPI/4.1.5/gnu

# Usage check
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <operation> <benchmark_type>"
    exit 1
fi

operation=$1
benchmark_type=$2

# Define the number of MPI processes per node
TASKS_PER_NODE=128

# Directory where the MPI executables are located
MPI_DIR="/u/dssc/vnigam/HPC/exercise1/osu-micro-benchmarks-7.0.1/c/mpi/collective"

# Define warm-up and total iteration counts
WARMUP_ITERATIONS=500
TOTAL_ITERATIONS=25000

# Define a map from operation name to executable
declare -A op_to_exec
op_to_exec[broadcast]="osu_bcast"
op_to_exec[scatter]="osu_scatter"

# Verify if the operation is supported
if [[ -z "${op_to_exec[$operation]}" ]]; then
    echo "Invalid operation: $operation"
    exit 1
fi

# Assign executable name from the map
EXECUTABLE="${op_to_exec[$operation]}"

# Algorithm definitions for broadcast
declare -A algorithms
if [ "$operation" == "broadcast" ]; then
    algorithms=(
        [ignore]=0
	[chain]=2
	[pipeline]=3
        [binary_tree]=5
    )
elif [ "$operation" == "scatter" ]; then
    algorithms=(
	[default]=0
	[basic linear]=1
	[binomial]=2
        [non-blocking linear]=3
         )
else
    echo "Invalid operation: $operation"
    exit 1
fi

# Initialize output file for the entire run
OUTPUT_FILE="${operation}_${benchmark_type}_$(date +%Y%m%d%H%M%S).txt"
echo "Size,Avg Latency(us),Min Latency(us),Max Latency(us),Iterations,NP_total,ALGO,ALGO_NAME" > "$OUTPUT_FILE"

# Loop over algorithms, message sizes, and number of processes
for alg_name in "${!algorithms[@]}"; do
    alg_num="${algorithms[$alg_name]}"
    
    if [ "$benchmark_type" == "fixed" ]; then
        sizes=(4)  # Fixed size
        for np in $(seq 2 2 256); do
            TEMP_OUTPUT=$(mktemp)
            mpirun --mca coll_tuned_use_dynamic_rules true --mca coll_tuned_${operation}_algorithm $alg_num --map-by ppr:$TASKS_PER_NODE:node -np $np $MPI_DIR/$EXECUTABLE -m ${sizes[0]} -x $WARMUP_ITERATIONS -i $TOTAL_ITERATIONS > $TEMP_OUTPUT
            if [ $? -ne 0 ]; then
                echo "Error running mpirun for $alg_name with size ${sizes[0]}, np $np, check output file for details."
            else
                # Parse the output and format it according to the specified layout
                awk -v size="${sizes[0]}" -v np="$np" -v algo="$alg_num" -v alg_name="$alg_name" \
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
                    if (seen == 1) print size, avg_latency, min_latency, max_latency, 30000, np, algo, alg_name 
                 }' $TEMP_OUTPUT >> "$OUTPUT_FILE"
            fi
            rm $TEMP_OUTPUT  # Clean up temporary file
        done
    elif [ "$benchmark_type" == "full" ]; then
        sizes=(1 2 4 8 16 32 64 128 256 512 1024 2048 4096 8192 16384 32768 65536 131072 262144 524288)
        for np in 2 4 8 16 32 64 128 256; do
            for size in "${sizes[@]}"; do
                TEMP_OUTPUT=$(mktemp)
                mpirun --mca coll_tuned_use_dynamic_rules true --mca coll_tuned_${operation}_algorithm $alg_num --map-by ppr:$TASKS_PER_NODE:node -np $np $MPI_DIR/$EXECUTABLE -m $size -x $WARMUP_ITERATIONS -i $TOTAL_ITERATIONS > $TEMP_OUTPUT
                if [ $? -ne 0 ]; then
                    echo "Error running mpirun for $alg_name with size $size, np $np, check output file for details."
                else
                    # Parse the output and format it according to the specified layout
                    awk -v size="$size" -v np="$np" -v algo="$alg_num" -v alg_name="$alg_name" \
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
                        if (seen == 1) print size, avg_latency, min_latency, max_latency, 30000, np, algo, alg_name 
                     }' $TEMP_OUTPUT >> "$OUTPUT_FILE"
                fi
                rm $TEMP_OUTPUT  # Clean up temporary file
            done
        done
    else
        echo "Invalid benchmark type: $benchmark_type"
        exit 1
    fi
done

