# thesis_MDs

# 0. Pre-MD Steps
- Run antibody/antigen complexes on ClusPro
- Examine PRODIGY scores
- Narrow down complexes based on deltaG scores from PRODIGY and model rank from ClusPro
- Select for Model 0 scores

# Running MD Simulations - Test Run 1 - n_ct173_pep7-dk7-model0_MD
# 1. Set up environment on HPC
# make sure each of your cluspro docked model.pdb is in the correct folder, named according to the complex
cd /home1/AMUKHTAR24@kgi.edu/thesis/md_sims_native/n_ct173_pep7-dk7-model0_MD
- [AMUKHTAR24@kgi.edu@laguna1 n_ct173_pep7-dk7-model0_MD]$ module load gcc
- [AMUKHTAR24@kgi.edu@laguna1 n_ct173_pep7-dk7-model0_MD]$ module load fftw
- [AMUKHTAR24@kgi.edu@laguna1 n_ct173_pep7-dk7-model0_MD]$ module load gromacs-gpu
  
# 2. Set Protonation States
- # Use propka to get model PKA values
- python -m propka model.pdb -o 7.4
- ALTERNATIVE: python -m propka model.pdb -o 7.4 (optional)
# begin setting protonation states
- gmx_mpi pdb2gmx -f model.pdb -o model_processed.gro -ignh -inter
   # choose #6 (for Amber99SB-ILDN forcefield) and 1 (for TIP3P water)
   # ignh will ignore the hydrogens, which is important to avoid a fatal error  

  <img width="1472" height="816" alt="image" src="https://github.com/user-attachments/assets/748902f3-970d-406a-ae93-a6e8999a4c94" />

# pH < pKa → residue is protonated (acidic environment wins, proton stays on)
# pH > pKa → residue is deprotonated (basic environment wins, proton leaves)
# e.g. LYS at residue 43 PKA = 9.94; pH(7.4) < pKa (9.94) => protonate 

    #(in this case is we have to determine the protonation state of histidine)
    #there is not possible to set an specific pH value (for our purposes is going to be 7.4) but it is possible to analyse and 
    #determine all the protonation states of each aminoacid specificly if we analyse them with propka, determine their PKa and 
    #finally see which is the protonation state of each aminoacid at 7.4 pH)
    #after we analyze with propka at a specific pH "python -m propka model.gro -o 7.4"
    #we shoud use "pdb2gmx -f protein.pdb -inter" and it wil guide us throught each aminoacid to determine their protonation state
    #Once you select all the protonation state if GROMACS ask you for link amoniacids between each other mark no (n)
  
   #Remember that if you want to neutralize an aminocid you should choose the protonation state that results in an overall charge of 0.
   #This means that If the residue is normally negatively charged (e.g., GLU, ASP) use the protonated form to neutralize it and 
   #If the residue is normally positively charged (e.g., LYS, ARG) use the deprotonated form to neutralize it. So in general if you want a aminaocid neutralized
     #just pay atention to the charge (it has to be 0)

  
# get .gro file
- gmx_mpi pdb2gmx -f model.pdb -o model_processed.gro (optional)
- 
- OR python -m propka model.gro -o 7.4 # depends on your starting file, but mostly likely start with the model.pdb version
    #(we use TIP3P water which is compatible with our Amber99SB-ILDN forcefield)
- gmx_mpi  pdb2gmx -f model.pdb -o model_processed.gro | gmx pdb2gmx -f model.pdb -o model_processed.gro -his |  gmx_mpi pdb2gmx -f model.pdb -o model_processed.gro -inter
    
# 3. Set Box Size 
 - gmx_mpi editconf -f model_processed.gro -o model_newbox.gro -c -d 1.0 -bt cubic
   
# 4. Solvate 
- gmx_mpi solvate -cp model_newbox.gro -cs spc216.gro -o model_solv.gro -p topol.top 
    #(SPC216: simple point charge water is a pre-equilibrated box of 216 SPC water molecules and it is used for 3-site water models like TIP3P. The 216SPC is a file that contains 216 molecules of preequilibrated water taht it is used as a start point to fill a simulation box with water, This 216SPC is like a template that is used to fill you box with as much water as it is needed so even if the tmeplate has 216 water molecues of preequilibrated water you box wil not have only 216 water moleucles, your box wil end with thounsands of preequilibrated TIP3P water molecules that comes from the 216SPC file that was used as a template)
  
  # use: grep "SOL" topol.top to check if the topology file was updated with the water (SOL) molecules (you should see values once you execute this code, for example SOL 66850)
- grep SOL topol.top
  
# 4. Create .mdp files, starting with ions.mdp
- nano ions.mdp (optional, to update ions.mdp)

# 5. Generate ions.tpr
- gmx_mpi grompp -f ions.mdp -c model_solv.gro -p topol.top -o ions.tpr
    #grep -E "NA|CL|ION" topol.top you should not see any values here because IONS will be added in the next step, this is just ot verify that IONS are not present here and will be added in the next step

 # 6. Add ions 
- gmx_mpi genion -s ions.tpr -o model_solv_ions.gro -p topol.top -pname NA -nname CL -neutral -conc 0.15 
    # use the option 13 to add the ions (SOL)
    #(gromacs reads the concentration in mol/L and our target is 150mM or 0.15M)
    # use: grep -E "NA|CL" topol.top to check if the topology file was updated (you should see values once you execute this code, for example NA 10 CL 10)

# 7.  Generate em.tpr
- gmx_mpi grompp -f minim.mdp -c model_solv_ions.gro -p topol.top -o em.tpr

 # 8. Run minimization 
- gmx_mpi mdrun -v -deffnm em 
    #(here we wil use our energy_minimization.sh)
    #This step is used to delete tensions or atomic clashesbefore starting a molecular dynamics. In a protein at the beggining the initial stucture can have atoms very lose to each other or tense bonds which generates high forces, this can produce a unestable simulation. We will eliminate clashes, reduce extremely high forces in bonds and angles, stabilize the molecular geometry and generate a soft beggining for the NVP/NPT ensembles. This algorithm adjust the positions of the atoms to reduce the potential energy of the system using algoritms like: Steepest Descend (goes in the steepest direction in which the energy gets reduced, it is fast and robust but not very precise and it gets used in the first part of the minimization), Conjugate gradient (cg) more precise but slower, it is used after the steep if the system still having high forces. L-BFGS which is more efficient in small systems or with low dimentionallity. If the systems gets stable it means it is ready for the NVT/NPT ensemble andalso for the molecular dynamics.

    #sbatch script.sh (it has to be executable, if for any case it is not use "chmod +x script.sh and then "dos2unix script.sh")
    #grep -E "SOL|NA|CL" topol.top (after the minimization you should check that the topology file contains the ions and water molecules yet. the amount of CL, NA ions and water SOL should remain the same after the energy minimization)

# 8a. Optional, double check potential energy vs energy minimization 
- gmx_mpi energy -f em.edr -o potential.xvg
    #select the option 10 0
    #if the system does not reache a stable minimun it can be a serious problem. The energy should decrease progresively if it gets stuck or keeps decreasing without reaching a minimun there is something wrong. The minimization stops for "Fmax too large", the energy fluctuates instead decreaseing or the atoms overlap or the system collapse. You can increase the number of steps in the energy minimization simualtion (nseps) so you will allow the system to find a stable minimun. You can change the minimization algorith (integrator option in the em.mdp) the recomended is the Steepest Descent (steep), it is fast and efficient is not you can use conjugate gradient (integrator = cg) it is more precise but it requires the system is close to a minimun. If the system collapses or the energy fluctuates you can reduce the step size of the minimization (emstep), the smaller the steps (around 0.001) it will avoid sudden movements and will improve stability. You can use constrain in hidrogen bond (constrains = h-bond) if the forces are very high, this will reduce extreme movements of the hidrogen bonds which can stabilize the minimization. Check on possible atomic clashes, if there are overalpping atoms the minimization will fail (if you see a high Fmax (>10⁵ kJ/mol·nm) you can move the moleucles a bit with gmc editconf with "gmx editconf -f sistema.gro -o sistema_shifted.gro -translate 0.1 0.1 0.1" this can separate the overlaping atoms). Verify the topology, verify if there are atoms with charges or incorrect radius, for example you have 5000 SOL molecules after gmx solvate, make sure that number is correct. Make sure the parameters of the forcefield are correct in the gmx pdb2gmx, correct all the warings in atoms or bonds before minimize.   

# 9. Preprocessing NVT equilibrium (generate nvt input file nvt.tpr)
- gmx_mpi grompp -f nvt.mdp -c em.gro -r em.gro -p topol.top -o nvt.tpr

# 10. Run NVT
- gmx_mpi mdrun -deffnm nvt 
    #this ensemble maitains a fixed volume (the simulation box does not change its size) the temperature gets cosntant through a thermostate like Berendsen, Nose-Hoover or V-rescale. It will equilibrate the temperature before going into the NPT ensemble or when you want to study processes in whihc the volume does not change (simulations in water boxes) or systems in whihc the pressure is not relevant (Remember thsi is used to adjust the temperature with studies at a fixed volume)
    #(here we will use our nvt_ensemble.sh)
    #grep -E "SOL|NA|CL" topol.top (after the minimization you should check that the topology file contains the ions and water molecules yet. the amount of CL, NA ions and water SOL should remain the same after the NVT ensemble)

# 11. Check temperature
- gmx_mpi energy -f nvt.edr -o temperature.xvg
    #select the option 16 0
    #a variation of +-5K for small systems and +-2K for large systems is perfect!a variation like 10/20K is considered inestable so check on that. If the systems initially fluctuates a lot you can use a Berendsen thermostat in the first 20-50ps and then use V-rescale for the rest of the simulation (v-scale is a better Berdensen version that maintains the temperature with realistic physical fluctuations and avoid non-physical effects it is like using V-rescale instead Berdensen) You can also reduce the dt of the system if it is tempearture inestable or define the groups (like protein and non-protein groups). Make sure the system is well minimized so it wont start with wierd temperatures (you can execute an extra step of minimization , if there are atomic clashes or non physical interactions the temperature can go up suddently). If the tempeature is not well defined you can generate new thermal velocities with a seed in the nvt.mdp file (using gen-vel = yes, gen-temp = 300 and gen-seed = -1 for example, this can help to reduce initial fluctuations)

# 12. NPT equilibration  
- gmx_mpi  grompp -f npt.mdp -c nvt.gro -r nvt.gro -t nvt.cpt -p topol.top -o npt.tpr

# 13. run 
- gmx_mpi mdrun -deffnm npt 
    #(here we will use our npt_ensemble.sh)
    #grep -E "SOL|NA|CL" topol.top (after the minimization you should check that the topology file contains the ions and water molecules yet. the amount of CL, NA ions and water SOL should remain the same after the NPT ensemble)

# 14. check pressure
- gmx_mpi energy -f npt.edr -o pressure.xvg
    #select the option 18 0
    #Preassure can range between +-100 bar because the instnat pressure have high fluctuations in the molecualr dynamics. It is a red flag if the pressure is outside of the target consistently

# 15. check density
- gmx_mpi energy -f npt.edr -o density.xvg
    #select the option 24 0
    #density can fluctuate between +-5 kg/m3 which is normal in simulations performed on water. A high density should be around 10>kg/m3
    #in general the NPT ensemble allos the volume to change so the box can fit and reach a target volume. The temperature of the termostat remains (like in a NVT) and the pressure is controlled with a barostat (like Berendsen or Parrinello-Rahman). You will use it to equilibrate the pressure after a NVT. It is used in simulations in which he density is important like fluids, biomolecules in solutions, compressible materials, etc. It is also used to prepare a system befire the final production (stable stage of the molecualr dynamics). Remember this ensemble is used to adjust the pressure and obtain a experimental density.

#if the density or preasure are not stable you can change barostate (pcoupl option in the npt.mdp file). you can use Parrinello-Rahman barostate for long simulations. This barostate is more precise. You can also use Berendsen jsut to stabilize the simulations at the beggining 50-100ps and then change to Parrinello-Rahman, this is becuase Berendsen gets eatable quickly and do not generate realistics physical fluctuations so it should not be used in the production pahse. You can also try higher values of relaxing time (tau_p) values between 2.0 and 5.0 ps so it can soft the pressure range, if the pressure response is slow reduce tau_p to 1.0 to increase the adjust time (but not less than 1.0). The temperature control can also affect density so make sure to use v-rescale or Nose-Hoover (if you use Nose-Hoover use tau_t = 0.5 or greater to avoid exteme fluctuations). If preassure nad density variates a sudently redute the instegration step (dt), the smaller this steps more stable is the simulation but it will be slower. Also revew if the NVT was well executed, if not the NPT can start with high fluctuations. If the energy is not stable execute a longer minimization in between NVT/NPT steps. Remember that preassure fluctuates a lot given the small nuber of molecules in the simulation even in well equililibrated simulations it can variate in +-100bar instantly 


# 16. start MD run pre-processing
- gmx_mpi grompp -f md.mdp -c npt.gro -t npt.cpt -p topol.top -o md_0_1.tpr
    #grep -E "SOL|NA|CL" topol.top (after the minimization you should check that the topology file contains the ions and water molecules yet. the amount of CL, NA ions and water SOL should remain the same before start the MD simulation)

 # 17. Start MD Run   
#sbatch -p gpu --gres=gpu:a100:2 --mem=100g --time=168:00:00 md.sh 
    #(here we use our md.sh)
    #scontrol show job #ABCDE
    #scancel ABCDE


