#!/bin/bash

#SBATCH --job-name=md_300ns_reps
#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
#SBATCH --gres=gpu:l40s:1
#SBATCH --mem=48G
#SBATCH --time=7-00:00:00
#SBATCH --array=1-3
#SBATCH --output=logs/md_300ns_reps_%A_%a.out
#SBATCH --error=logs/md_300ns_reps_%A_%a.err

set -euo pipefail

module purge
module load gcc/13.3.0
module load gromacs-gpu/2024.3

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

BASE_DIR="/project/<PATH/TO/YOUR/FILES>"
REP_DIR="${BASE_DIR}/rep${SLURM_ARRAY_TASK_ID}_150ns"
DEFFNM="md_rep${SLURM_ARRAY_TASK_ID}"

cd "$REP_DIR"

echo "=============================="
echo "Job ID: $SLURM_JOB_ID"
echo "Array Task ID: $SLURM_ARRAY_TASK_ID"
echo "Working directory: $(pwd)"
echo "Node: $SLURM_JOB_NODELIST"
echo "DEFFNM: $DEFFNM"
which gmx_mpi
echo "=============================="

gmx_mpi mdrun -deffnm "$DEFFNM" -ntomp $OMP_NUM_THREADS -gpu_id 0
