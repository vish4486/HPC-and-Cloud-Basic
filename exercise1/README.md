# Performance Evaluation of High Performance Computing with OpenMPI Standards

This repository contains the implementation and results for the performance evaluation of OpenMPI Collective Operations as part of the HPC Final Assignment.


## Exercise 1: HPC Final Assignment

- **Exercise Description**: Please refer to `exercise1.md` for the detailed description of the exercise.
- **Final Report**: The comprehensive report can be found in `Nigam_ex1_report.pdf`.

## Usage

To reproduce the reported latencies and timings, use the provided `benchmark_job.sh` script. This work is accompolished in multiple iterations  due to time constraints on the orfeo  execution environment.

```bash
sbatch benchmark_job.sh [operation_type] [benchmark_type]
```

here operation chosen is:
-broadcast [for algo-default,chain,pipeline and binary tree]
-scatter  [for algo-default,basic linear,binomial,non-blocking linear]

and benchmark type is fixed and full.Fixed is for fixed  message size 4 and for full message sizes (1 2 4 8 16 32 64 128 256 512 1024 2048 4096 8192 16384 32768 65536 131072 262144 524288) so that test could produce relevant visualization.

All the scripts tested are in scripts folder and benchmark files are stored in results folder.plots and images are in images folder.
