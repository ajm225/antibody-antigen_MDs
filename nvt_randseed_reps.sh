#!/bin/bash
#SBATCH --array=1-3
#SBATCH --job-name=nvt_reps
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=16G
#SBATCH --time=48:00:00
#SBATCH --output=logs/%x_%A_%a.out

module load gcc
module load fftw
module load gromacs-gpu

REP=${SLURM_ARRAY_TASK_ID}
GEN_SEED=$((1000 + REP))
LD_SEED=$((2000 + REP))

mkdir -p rep${REP}

echo "Replicate: rep${REP}"
echo "gen_seed = ${GEN_SEED}"
echo "ld_seed  = ${LD_SEED}"

sed -e "s/GEN_SEED/${GEN_SEED}/g" \
    -e "s/LD_SEED/${LD_SEED}/g" \
    nvt_template.mdp > rep${REP}/nvt.mdp

gmx_mpi grompp \
    -f rep${REP}/nvt.mdp \
    -c em.gro \
    -r em.gro \
    -p topol.top \
    -o rep${REP}/nvt.tpr

gmx_mpi mdrun \
    -deffnm rep${REP}/nvt
