#include <iostream>
#include <fstream>
#include <cstdlib>
#include <string>

// Struct to represent an algorithm with an ID and a name
struct Algorithm {
    int id;
    std::string name;
};

// Function to run a system command and log its output
void run_command(const std::string& command) {
    std::cout << "Executing: " << command << std::endl;
    int result = system(command.c_str());
    if (result != 0) {
        std::cerr << "Error executing command: " << command << std::endl;
    }
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << " <operation_type> <benchmark_type>" << std::endl;
        return 1;
    }

    std::string operation_type = argv[1];
    std::string benchmark_type = argv[2];

    const int num_iterations = 25000;  // Number of iterations for the benchmark
    const int message_size = 524288;  // Message size for the benchmark
    const std::string scatter_benchmark_path = "./osu-micro-benchmarks-7.0.1/c/mpi/collective/osu_scatter";
    const std::string broadcast_benchmark_path = "./osu-micro-benchmarks-7.0.1/c/mpi/collective/osu_bcast";
    const int warmup_iterations = 500;  // Number of warmup iterations

    int np_values[] = {2, 4, 8, 16, 32, 64, 128, 256};
    int num_np_values = sizeof(np_values) / sizeof(np_values[0]);

    Algorithm broadcast_algorithms[] = {
        {0, "default"},
        {2, "chain"},
        {5, "binary tree"},
        {3, "pipeline"}
    };
    int num_broadcast_algorithms = sizeof(broadcast_algorithms) / sizeof(broadcast_algorithms[0]);

    Algorithm scatter_algorithms[] = {
        {0, "default"},
        {1, "basic linear"},
        {2, "binomial"},
        {3, "non-blocking linear"}
    };
    int num_scatter_algorithms = sizeof(scatter_algorithms) / sizeof(scatter_algorithms[0]);

    for (int i = 0; i < num_np_values; ++i) {
        int np = np_values[i];

        if (operation_type == "scatter") {
            for (int j = 0; j < num_scatter_algorithms; ++j) {
                int scatter_algo = scatter_algorithms[j].id;
                std::string scatter_algo_name = scatter_algorithms[j].name;

                if (benchmark_type == "fixedsize" || benchmark_type == "both") {
                    // Scatter with fixedsize
                    std::string command_scatter_fixedsize = "mpirun --map-by core --mca coll_tuned_use_dynamic_rules true --mca coll_tuned_scatter_algorithm "
                                                            + std::to_string(scatter_algo) + " -np " + std::to_string(np) + " " + scatter_benchmark_path 
                                                            + " -x " + std::to_string(warmup_iterations) + " -i " + std::to_string(num_iterations) 
                                                            + " -f -m " + std::to_string(message_size) + " >> results_SCATTER1_fixedsize_" 
                                                            + scatter_algo_name + ".txt 2>&1";
                    run_command(command_scatter_fixedsize);
                }

                if (benchmark_type == "full" || benchmark_type == "both") {
                    // Scatter with full
                    std::string command_scatter_full = "mpirun --map-by core --mca coll_tuned_use_dynamic_rules true --mca coll_tuned_scatter_algorithm "
                                                       + std::to_string(scatter_algo) + " -np " + std::to_string(np) + " " + scatter_benchmark_path 
                                                       + " -x " + std::to_string(warmup_iterations) + " -i " + std::to_string(num_iterations) 
                                                       + " >> results_SCATTER1_full_" + scatter_algo_name + ".txt 2>&1";
                    run_command(command_scatter_full);
                }
            }
        } else if (operation_type == "broadcast") {
            for (int k = 0; k < num_broadcast_algorithms; ++k) {
                int broadcast_algo = broadcast_algorithms[k].id;
                std::string broadcast_algo_name = broadcast_algorithms[k].name;

                if (benchmark_type == "fixedsize" || benchmark_type == "both") {
                    // Broadcast with fixedsize
                    std::string command_broadcast_fixedsize = "mpirun --map-by core --mca coll_tuned_use_dynamic_rules true --mca coll_tuned_bcast_algorithm "
                                                              + std::to_string(broadcast_algo) + " -np " + std::to_string(np) + " " + broadcast_benchmark_path 
                                                              + " -x " + std::to_string(warmup_iterations) + " -i " + std::to_string(num_iterations) 
                                                              + " -f -m " + std::to_string(message_size) + " >> results_BROADCAST1_fixedsize_" 
                                                              + broadcast_algo_name + ".txt 2>&1";
                    run_command(command_broadcast_fixedsize);
                }

                if (benchmark_type == "full" || benchmark_type == "both") {
                    // Broadcast with full
                    std::string command_broadcast_full = "mpirun --map-by core --mca coll_tuned_use_dynamic_rules true --mca coll_tuned_bcast_algorithm "
                                                         + std::to_string(broadcast_algo) + " -np " + std::to_string(np) + " " + broadcast_benchmark_path 
                                                         + " -x " + std::to_string(warmup_iterations) + " -i " + std::to_string(num_iterations) 
                                                         + " >> results_BROADCAST1_full_" + broadcast_algo_name + ".txt 2>&1";
                    run_command(command_broadcast_full);
                }
            }
        } else {
            std::cerr << "Invalid operation type. Please use 'scatter' or 'broadcast'." << std::endl;
            return 1;
        }
    }

    return 0;
}

