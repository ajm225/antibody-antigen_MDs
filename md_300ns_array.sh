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

set -e

module load gcc
module load fftw
module load gromacs-gpu

REP=${SLURM_ARRAY_TASK_ID}

if [ -z "$REP" ]; then
    echo "ERROR: SLURM_ARRAY_TASK_ID is not set."
    exit 1
fi

REP_DIR="rep${REP}"

echo "========================================"
echo "Starting 300 ns MD for ${REP_DIR}"
echo "Start time: $(date)"
echo "========================================"

cd ${REP_DIR}

# Your Step 16 creates md.tpr, so use -s md.tpr
# -deffnm md_300ns names the outputs md_300ns.xtc, md_300ns.edr, etc.
gmx_mpi mdrun -s md.tpr -deffnm md_300ns

echo "========================================"
echo "Finished 300 ns MD for ${REP_DIR}"
echo "End time: $(date)"
echo "========================================"
