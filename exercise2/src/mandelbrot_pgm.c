#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>
#include <omp.h>

// Function to check if a point is in the Mandelbrot set
int mandelbrot(double real, double imag, int max_iter) {
    double z_real = 0.0, z_imag = 0.0;
    int iter;
    for (iter = 0; iter < max_iter; ++iter) {
        double z_real2 = z_real * z_real;
        double z_imag2 = z_imag * z_imag;
        if (z_real2 + z_imag2 > 4.0) {
            return iter;
        }
        z_imag = 2.0 * z_real * z_imag + imag;
        z_real = z_real2 - z_imag2 + real;
    }
    return max_iter;
}

// Function to write PGM image
void write_pgm_image(int width, int height, int max_val, int **matrix, const char *filename) {
    FILE *pgm = fopen(filename, "wb");
    if (!pgm) {
        fprintf(stderr, "Failed to open file for writing.\n");
        exit(1);
    }
    fprintf(pgm, "P5\n%d %d\n%d\n", width, height, 255);
    for (int j = 0; j < height; j++) {
        for (int i = 0; i < width; i++) {
            unsigned char pixel_value;
            if (matrix[j][i] == max_val) {
                pixel_value = 0; // Black for points inside the set
            } else {
                // Normalize to 0-255 range for points outside the set
                pixel_value = (unsigned char)((255 * matrix[j][i]) / max_val);
            }
            fwrite(&pixel_value, sizeof(unsigned char), 1, pgm);
        }
    }
    fclose(pgm);
}

int main(int argc, char *argv[]) {
    if (argc != 8) {
        fprintf(stderr, "Usage: %s n_x n_y x_L y_L x_R y_R I_max\n", argv[0]);
        return 1;
    }

    int n_x = atoi(argv[1]);
    int n_y = atoi(argv[2]);
    double x_L = atof(argv[3]);
    double y_L = atof(argv[4]);
    double x_R = atof(argv[5]);
    double y_R = atof(argv[6]);
    int I_max = atoi(argv[7]);

    int **M = malloc(n_y * sizeof(int *));
    for (int i = 0; i < n_y; i++) {
        M[i] = malloc(n_x * sizeof(int));
    }

    double delta_x = (x_R - x_L) / n_x;
    double delta_y = (y_R - y_L) / n_y;

    // Initialize MPI
    MPI_Init(&argc, &argv);
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    int chunk_size = n_y / size;
    int start_row = rank * chunk_size;
    int end_row = (rank == size - 1) ? n_y : start_row + chunk_size;

    // Calculate Mandelbrot set
    #pragma omp parallel for schedule(dynamic)
    for (int j = start_row; j < end_row; j++) {
        for (int i = 0; i < n_x; i++) {
            double c_real = x_L + i * delta_x;
            double c_imag = y_L + j * delta_y;
            M[j][i] = mandelbrot(c_real, c_imag, I_max);
        }
    }

    // Gather results at root process
    if (rank == 0) {
        for (int src = 1; src < size; src++) {
            MPI_Recv(&(M[src * chunk_size][0]), chunk_size * n_x, MPI_INT, src, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        }
    } else {
        MPI_Send(&(M[start_row][0]), chunk_size * n_x, MPI_INT, 0, 0, MPI_COMM_WORLD);
    }

    // Write PGM image at root process
    if (rank == 0) {
        // Save the image to the specified directory
        write_pgm_image(n_x, n_y, I_max, M, "/u/dssc/vnigam/HPC/exercise2/images_plots/mandelbrot.pgm");
    }

    // Clean up
    for (int i = 0; i < n_y; i++) {
        free(M[i]);
    }
    free(M);

    MPI_Finalize();
    return 0;
}

