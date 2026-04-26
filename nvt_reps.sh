#!/bin/bash
###############################################
# SLURM ARRAY SETTINGS
###############################################

#SBATCH --array=1-3                        # Run 3 tasks → rep1, rep2, rep3
#SBATCH --job-name=nvt_reps                # Job name shown in queue/logs
#SBATCH --partition=compute               # Partition to run on
#SBATCH --ntasks=1                        # One MPI task per replicate
#SBATCH --cpus-per-task=8                 # Number of CPU cores per task
#SBATCH --mem=16G                         # Memory per task
#SBATCH --time=48:00:00                   # Max runtime
#SBATCH --output=logs/%x_%A_%a.out        # Output log (jobname_jobID_arrayID.out)

###############################################
# LOAD REQUIRED MODULES
###############################################

module load gcc
module load fftw
module load gromacs-gpu                   # Load GROMACS (Laguna environment)

###############################################
# DEFINE REPLICATE NUMBER
###############################################

# SLURM_ARRAY_TASK_ID will be:
# 1 → rep1
# 2 → rep2
# 3 → rep3
REP=${SLURM_ARRAY_TASK_ID}

###############################################
# DEFINE RANDOM SEEDS FOR THIS REPLICATE
###############################################

# These seeds control:
# - gen_seed → initial velocity assignment
# - ld_seed  → stochastic thermostat behavior

# Each replicate gets unique seeds for independent trajectories
GEN_SEED=$((1000 + REP))   # rep1=1001, rep2=1002, rep3=1003
LD_SEED=$((2000 + REP))    # rep1=2001, rep2=2002, rep3=2003

###############################################
# CREATE REPLICATE DIRECTORY
###############################################

# Create a folder for this replicate (if it doesn't already exist)
mkdir -p rep${REP}

###############################################
# PRINT RUN INFORMATION (FOR LOGS / REPRODUCIBILITY)
###############################################

echo "========================================"
echo "Starting NVT for replicate: rep${REP}"
echo "gen_seed = ${GEN_SEED}"
echo "ld_seed  = ${LD_SEED}"
echo "Start time: $(date)"
echo "========================================"

###############################################
# GENERATE REPLICATE-SPECIFIC NVT.MDP
###############################################

# nvt_template.mdp contains placeholders:
#   GEN_SEED and LD_SEED
#
# This command replaces those placeholders with actual values
# and writes a new file: repX/nvt.mdp

sed -e "s/GEN_SEED/${GEN_SEED}/g" \
    -e "s/LD_SEED/${LD_SEED}/g" \
    nvt_template.mdp > rep${REP}/nvt.mdp

# Optional: confirm that the seeds were correctly inserted
echo "Checking generated nvt.mdp:"
grep -E "gen_seed|ld_seed" rep${REP}/nvt.mdp

###############################################
# PREPROCESS NVT (GENERATE .TPR FILE)
###############################################

# grompp compiles the mdp + structure + topology into a binary input file (.tpr)
# This is where the seeds are "locked in" for the simulation

gmx_mpi grompp \
    -f rep${REP}/nvt.mdp \
    -c em.gro \
    -r em.gro \
    -p topol.top \
    -o rep${REP}/nvt.tpr

###############################################
# RUN NVT SIMULATION
###############################################

# mdrun executes the simulation using the .tpr file
# This is the first dynamic step where randomness is introduced

gmx_mpi mdrun \
    -deffnm rep${REP}/nvt

###############################################
# FINISH MESSAGE
###############################################

echo "========================================"
echo "Finished NVT for replicate: rep${REP}"
echo "End time: $(date)"
echo "========================================"
