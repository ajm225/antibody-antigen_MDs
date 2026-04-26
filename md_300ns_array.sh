#!/bin/bash
#SBATCH --job-name=md_300ns_reps
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=16G
#SBATCH --time=7-00:00:00
#SBATCH --array=1-3%1
#SBATCH --output=logs/%x_%A_%a.out

###############################################
# LOAD MODULES
###############################################
module load gcc
module load fftw
module load gromacs-gpu

###############################################
# DEFINE REPLICATE
###############################################
REP=${SLURM_ARRAY_TASK_ID}
REP_DIR="rep${REP}_300ns"

echo "========================================"
echo "Starting MD for ${REP_DIR}"
echo "Start time: $(date)"
echo "========================================"

###############################################
# MOVE INTO REPLICATE DIRECTORY
###############################################
cd ${REP_DIR}

###############################################
# RUN PRODUCTION MD
###############################################
gmx_mpi mdrun -deffnm md_300ns

###############################################
# FINISH
###############################################
echo "Finished ${REP_DIR}"
echo "End time: $(date)"
