## AM - UPDATED WITH NOTES##
# 1. RMSD + RMSF Analysis
#RMSD = Root Mean Square Deviation => Overall structural deviation over time compared to a reference structure (time vs deviation)
#RMSF = Per-residue flexibility over the trajectory (residue index vs fluctuation)

    > module load fftw
    > module load gcc
    > module load gromacs-gpu

# per replicate, do the following create an analysis folder
    > mkdir -p Analysis

## analysis of trajectory files, select "protein" for all commands"
module load gcc/12.3.0 gromacs-gpu/2024.3
    > gmx_mpi trjconv -s md_0_1.tpr -f md_0_1.xtc -o Analysis/md_0_1_noPBC.xtc -pbc cluster -center
## per replicate:
    > gmx_mpi trjconv -s md_rep1.tpr -f md_rep1.xtc -o Analysis/rep1_noPBC.xtc -pbc cluster -center

## set atom range numbers instead or residues (since residues restart from 1 everytime)
e.g. 
    > a 1-1795
    
    Found 1795 atoms in range 1-1795
    
    > name 17 Heavy




## the following command will look at the structural stability, choose backbone (optin 4) for least squeare fit and RMSD calculation
> gmx_mpi rms -s md_0_1.tpr -f Analysis/md_0_1_noPBC.xtc -o Analysis/rmsd.xvg -tu ns
> gmx_mpi rms -s em.tpr -f Analysis/md_0_1_noPBC.xtc -o Analysis/rmsd_xtal.xvg -tu ns
> gmx_mpi rmsf -s md_0_1.tpr -f Analysis/md_0_1_noPBC.xtc -o Analysis/rmsf.xvg
## per replicate:
> gmx_mpi rms -s md_rep1.tpr -f Analysis/rep1_noPBC.xtc -o Analysis/rmsd.xvg -tu ns
> gmx_mpi rms -s em.tpr -f Analysis/rep1_noPBC.xtc -o Analysis/rmsd_xtal.xvg -tu ns
> gmx_mpi rmsf -s md_rep1.tpr -f Analysis/rep1_noPBC.xtc -o Analysis/rmsf.xvg



##generating differnet index files to analyze RMSD and RMSF separatelly 
> gmx_mpi make_ndx -f md_0_1.gro -o Analysis/index.ndx 
## per replicate
> gmx_mpi make_ndx -f md_rep1.gro -o Analysis/index.ndx 

#Review .gro file and atom numbering to select for proper index of protein 1 and protein 2, "a" for atom or "r" for residue
#Press "q" to save and quit
    #name protein1
    #a 101-200
    #name protein2
    #a 500-5600
gmx_mpi select -f md_0_1.gro -n Analysis/index.ndx
gmx_mdmat -f Analysis/md_0_1_noPBC.xtc -s md_0_1.gro -n Analysis/index.ndx  -mean Analysis/contact_map.xpm -no contact_map.xvg #choos 4 backbone for this

# per replicate
> gmx_mpi select -f md_rep1.gro -n Analysis/index.ndx
> gmx_mpi mdmat -f Analysis/rep1_noPBC.xtc -s md_rep1.gro -n Analysis/index.ndx -mean Analysis/contact_map.xpm -no contact_map.xvg #choos 4 backbone for this


## get representative PDB from a number of frames from trajectory file##, analyze cluster from cluster.log and get frames, choose protein (1) as output
gmx_mpi trjconv -f Analysis/md_0_1_noPBC.xtc -s md_0_1.tpr -o snapshots_cluster1.pdb -b 27200 -e 100000

# per replicate
> gmx_mpi trjconv -f Analysis/rep1_noPBC.xtc -s md_rep1.tpr -o snapshots_cluster1.pdb -b 27200 -e 100000


##get one single pdb from a specific frame, this example at frame 100 000
gmx_mpi trjconv -f Analysis/md_0_1_noPBC.xtc -s md_0_1.tpr -o snapshots_cluster1_pdb.pdb -dump 100000

# per replicate
> gmx_mpi trjconv -f Analysis/rep1_noPBC.xtc -s md_rep1.tpr -o snapshots_cluster1_pdb.pdb -dump 100000


##analysing RMSD and RMSF separately using the index file
    #this only works to generate hte RMSD of each protein, it will not work for the entire complex
gmx_mpi trjconv -s md_0_1.tpr -f md_0_1.xtc -o fitted.xtc -pbc mol -center
    #select system (group 0) and then protein (group 1)
gmx_mpi rms -s model.pdb -f fitted.xtc -n index.ndx -o rmsd_protein1.xvg -tu ns
    #select your protein from the index (protein 1 and protein 2)
gmx_mpi rmsf -s md_0_1.tpr -f md_0_1_noPBC1.xtc -n index.ndx -o rmsf_protein1.xvg
    #select your protein from the index (protein 1 and protein 2)



# per replicate
> gmx_mpi trjconv -s md_rep1.tpr -f md_rep1.xtc -o fitted.xtc -pbc mol -center
    #select system (group 0) and then protein (group 1)

#>gmx_mpi rms -s model.pdb -f fitted.xtc -n index.ndx -o rmsd_protein1.xvg -tu ns
    #select your protein from the index (protein 1 and protein 2)
# NOTE: ^This one didn't work with antigen because of atom number mismatch --> check with Ka (?), attempt 2:
--> run this two separate times:
> gmx_mpi rms -s md_rep1.tpr -f fitted.xtc -n index.ndx -o rmsd_protein1.xvg -tu ns
run 1:     
- protein 1: antibody 
- protein 2: antigen

Run 2:
- protein 1: antibody backbone
- protein 2: antigen backbone


> gmx_mpi rmsf -s md_rep1.tpr -f rep1_noPBC.xtc -n index.ndx -o rmsf_protein1.xvg
    #select your protein from the index (protein 1 and protein 2)


#####if for some reason this produce an error try this instead (spliting the model.pdb in 2 per protein, this should not be needed and typically generates more errors)
gmx editconf -f model.pdb -o protein1_reference.pdb -n index.ndx
    #select atoms1
gmx rms -s protein1_reference.pdb -f fitted.xtc -n index.ndx -o rmsd_protein1.xvg
    #select atoms
    #select atoms1
gmx editconf -f model.pdb -o protein2_reference.pdb -n index.ndx
    #select atoms2
gmx rms -s protein2_reference.pdb -f fitted.xtc -n index.ndx -o rmsd_protein1.xvg
    #select atoms2
    #select atoms2



----------------------

#####Generating the Cluster Analysis
- gmx_mpi trjconv -s md_rep1.tpr -f md_rep1.xtc -o md_rep1.xtc -pbc mol -center -fit rot+trans 
    #this is nost necesary but just in case. You can use the one in step 51
    #NOTE: I skipped the above because I already had noPBC.xtc generated from previous step

> gmx_mpi cluster -s md_rep1.tpr -f rep1_noPBC.xtc -n index.ndx -o clusters.xpm -g cluster.log -dist cluster.xvg -method gromos -cutoff 0.2
# select 4 for backbone

> gmx_mpi cluster -s md_rep1.tpr -f rep1_noPBC.xtc -o index.xpm -g cluster.log -cl cluster.pdb 
   # Select backbone for RMSD calc & output
    #if the previous comand to generate the cluster.pdb does not work use this one:
gmx cluster -s md_0_1.tpr -f cluster.xtc -o cluster.xpm -g cluster.log -cl clusters.pdb -method gromos -cutoff 0.1

    #This for the system in general
    #I selected the Carbon alpha or backbone, the protein choice takes a lot of time so the system wil kill it
    #I seelcted alpha carbon or backbone for the output as well
    #In case this is not ok delete the index fiel from the code line (it shoud not be a problen becuase here you are analysing all the system but just in case)


__________________________
######### Generating PDB Snapshots of MD Run 
NOTE: This section takes a PDB snapshot every 1000ps of an entire MD run. Depending on the simulation length, this part can take a significant amount of time. I started this process for a 150ns run, and it took over an hour. 

      for t in {0..100000..1000}; do           #0..100000..1000 means from 0 to 100000ps every 1000ps of snapshot
          gmx trjconv -s md_0_1.tpr -f md_0_1_noPBC.xtc -n index.ndx -o snapshot_${t}ps.pdb -dump $t
      done
         #then select the numbers to evaluate if you want the protein (1) or the system (0), etc

#Combining all generated snapshots into one PDB #

#this will generate different .pdb files that can be joint using is a single one using: 
    cat snapshot1.pdb snapshot2.pdb snapshot3.pdb > combined_snapshots.pdb

#here is an automatic way to combine al the generated snapshots in one .pdb file, in order:

 >        output_file="combined_snapshots.pdb"
          > "$output_file"
        
        for pdb_file in $(ls snapshot_*ps.pdb | sort -V); do
            echo "Adding $pdb_file to $output_file..."
            echo "MODEL $(basename "$pdb_file" .pdb | grep -o '[0-9]*')" >> "$output_file"
            cat "$pdb_file" >> "$output_file"
            echo "ENDMDL" >> "$output_file"
        done


#If you upload each snapshot separatelly and combine them in pymol, then aligned them to generate a superimpose picture with all the snapshots
#it seems there is no automatic way to do this, so you will have to do it manually in pymol or try to find a pymol script



-----------------------------

#####Interaction Analysis
#you can just se the interaction_analysis.py file to generate the heatmaps of intercation and the index file for the analysis in gromacs
#(THIS IS NEEDED for pair wise analysis, minimun distance interaction and number of hydrogen bonds). 
#for this analysis always use the md_0_1.xtc (it is going to be that file every time you want to generate a heatmail with MDAnalysis in python, do nto use the md_0_1_noPBC,xtc)
#here you will generate a interacting_residues_cogs.ndx which is an index file that separates only the residues (for each protein) that are interacting between these 2 proteins
#below an specific cutof porint (normaly below 5A), with this index file you can perform the minimun distance, pariwise distance and number of hidrogen bonds analysis in GROMACS
- Add the attached interaction_analysis.py file to your folder
    - make sure you have all of the correct python libraries installed, this .py uses MDAnalysis
- run the .py file, get out the interacting_residues_cogs.ndx
    > python interaction_analysis.py

# Example output: 
    Interacting Antibody residues: 46
    Interacting Antigen residues: 21
    Output written to: interacting_residues_cogs.ndx


#minimun distance - What is the closest contact at each time?
gmx_mpi mindist -s md_rep1.tpr -f md_rep1.xtc -n interacting_residues_cogs.ndx -od mindist.xvg -on num_contact.xvg -d 0.5
     #the interacting_residues_cogs.ndx is the ndx file generated in the interaction_analysis.py, the -d is the distance in nm

#pairwise distance - How far are these selected interface groups from each other over time?
gmx_mpi pairdist -s md_rep1.tpr -f md_rep1.xtc -n interacting_residues_cogs.ndx -o pairdist.xvg -ref Interacting_Protein1 -sel Interacting_Protein2
     #-ref Interacting_Protein1 -sel Interacting_Protein2 were determined in interacting_residues_cogs.ndx

#Hydrogen bonds
gmx_mpi hbond -s md_rep1.tpr -f rep1_noPBC.xtc -n interacting_residues_cogs.ndx -num hbondsnew.xvg
     #this tells you the number of hidrogen bonds present in the interactions. 
    
    #You will be prompted to enter a selection for a reference 'r' and target 't': 
    # For 'r': Interacting_Protein1
    # For 't': Interacting_Protein2

#It is posible to perform a salt bridge analysis, the code is in interaction_analysis.py


#secondary structure analysis
gmx_mpi dssp -f md_rep1.xtc -s md_rep1.tpr -o structure.dat -num numstruc.xvg
    #This will generate a .dat file that wil be used in the python script to generate the secondary structure map to see the change of secondary structures along time
# Note: to run this, you will likely have to download the module for "dssp" if you don't already have it. I had to create an entire python environment and use "conda" to install dssp




///MMPBSA: Molecular Mechanics – Poisson–Boltzmann Surface Area
# post-processing method used after MD simulations to estimate binding free energy (ΔG_bind) between two molecules 

#MMPBSA analysis 
   #First the groups have to be well defined in the index file (MAKE SURE YOU'VE DONE EVERYTHING PRIOR TO THIS TIL THIS POINT)

module load gromacs
module load gmx_mmpbsa
   #load both modules (gromacs and gmx_mmbpsa) at the same time

gmx_MMPBSA --create_input gb 
    #this is to generate a mmbpsa.in file

gmx_MMPBSA -i mmpbsa.in -cs md_0_1.tpr -ct md_0_1.xtc -ci indexfinal3.ndx -cg 17 18 -o results_mmpbsa.dat -eo results_mmpbsa.csv
   #in this comand the numbers 17 and 18 are the receptor and ligand repectively. Both have to be specified in this commandline

#for now it seems it only works with leaprc.protein.ff14SB forcefield, I could not run it with AMBER or Amber99SB-ILDN forcefields, maybe try Amber





1. Set up environment (create an mmpbsa environment first if it doesnt exist)
- module purge
- module load gcc/13.3.0
- module load openmpi
- module load gromacs-gpu/2024.3
- conda activate mmmpbsa_env

2. Using your previously made index.ndx file, you will need to create a modified version of it containing only the groups you need for MMPBSA (antibody and antigen)
- gmx_mpi make_ndx -f md_rep1.tpr -n index.ndx -o index_mmpbsa.ndx
    - use 'del' to remove all other groups than [Antigen] & [Antibody]

# create your mmpbsa.in file 
    gmx_MMPBSA --create_input gb
    output: mmpbsa.in

      gmx_MMPBSA \
          -i mmpbsa.in \
          -cs md_rep1.tpr \
          -ct md_rep1.xtc \
          -ci index_mmpbsa.ndx \ #use new index file you made
          -cg 1 0 \              # these numbers correspond to your [Antigen] & [Antibody] groups
          -o results_mmpbsa.dat \
          -eo results_mmpbsa.csv  

#for now it seems it only works with leaprc.protein.ff14SB forcefield, I could not run it with AMBER or Amber99SB-ILDN forcefields, maybe try Amber

















------------------------------------------------------------------------------------
## ORIGINAL ##
## Analysis of MD run simulations ###

## analysis of trajectory files, select "protein" for all comands"
module load gcc/12.3.0 gromacs-gpu/2024.3
gmx_mpi trjconv -s md_0_1.tpr -f md_0_1.xtc -o Analysis/md_0_1_noPBC.xtc -pbc cluster -center
## the following command will look at the structural stability, choose backbone (optin 4) for least squeare fit and RMSD calculation
gmx_mpi rms -s md_0_1.tpr -f Analysis/md_0_1_noPBC.xtc -o Analysis/rmsd.xvg -tu ns
gmx_mpi rms -s em.tpr -f Analysis/md_0_1_noPBC.xtc -o Analysis/rmsd_xtal.xvg -tu ns
gmx_mpi rmsf -s md_0_1.tpr -f Analysis/md_0_1_noPBC.xtc -o Analysis/rmsf.xvg

##generating differnet index files to analyze RMSD and RMSF separatelly 
gmx_mpi make_ndx -f md_0_1.gro -o Analysis/index.ndx 
#Review .gro file and atom numbering to select for proper index of protein 1 and protein 2, "a" for atom or "r" for residue
#Press "q" to save and quit
    #name protein1
    #a 101-200
    #name protein2
    #a 500-5600
gmx_mpi select -f md_0_1.gro -n Analysis/index.ndx
gmx_mdmat -f Analysis/md_0_1_noPBC.xtc -s md_0_1.gro -n Analysis/index.ndx  -mean Analysis/contact_map.xpm -no contact_map.xvg #choos 4 backbone for this
## get representative PDB from a number of frames from trajectory file##, analyze cluster from cluster.log and get frames, choose protein (1) as output
gmx_mpi trjconv -f Analysis/md_0_1_noPBC.xtc -s md_0_1.tpr -o snapshots_cluster1.pdb -b 27200 -e 100000
##get one single pdb from a specific frame, this example at frame 100 000
gmx_mpi trjconv -f Analysis/md_0_1_noPBC.xtc -s md_0_1.tpr -o snapshots_cluster1_pdb.pdb -dump 100000
##analysing RMSD and RMSF separately using the index file
    #this only works to generate hte RMSD of each protein, it will not work for the entire complex
gmx trjconv -s md_0_1.tpr -f md_0_1.xtc -o fitted.xtc -pbc mol -center
    #select system (group 0) and then protein (group 1)
gmx rms -s model.pdb -f fitted.xtc -n index.ndx -o rmsd_protein1.xvg -tu ns
    #select your protein from the index (protein 1 and protein 2)
gmx rmsf -s md_0_1.tpr -f md_0_1_noPBC1.xtc -n index.ndx -o rmsf_protein1.xvg
    #select your protein from the index (protein 1 and protein 2)

#####if for some reason this produce an error try this instead (spliting the model.pdb in 2 per protein, this should not be needed and typically generates more errors)
gmx editconf -f model.pdb -o protein1_reference.pdb -n index.ndx
    #select atoms1
gmx rms -s protein1_reference.pdb -f fitted.xtc -n index.ndx -o rmsd_protein1.xvg
    #select atoms
    #select atoms1
gmx editconf -f model.pdb -o protein2_reference.pdb -n index.ndx
    #select atoms2
gmx rms -s protein2_reference.pdb -f fitted.xtc -n index.ndx -o rmsd_protein1.xvg
    #select atoms2
    #select atoms2

##Generating the Cluster Analysis
gmx trjconv -s md_0_1.tpr -f trajectory.xtc -o md_0_1.xtc -pbc mol -center -fit rot+trans 
    #this is nost necesary but just in case. You can use the one in step 51
gmx cluster -s md_0_1.tpr -f md_0_1_noPBC.xtc -n index.ndx -o clusters.xpm -g cluster.log -dist cluster.xvg -method gromos -cutoff 0.2
gmx cluster -s md_0_1.tpr -f md_0_1_noPBC.xtc -o index.xpm -g cluster.log -cl cluster.pdb 
    #if the previous comand to generate the cluster.pdb does not work use this one:
gmx cluster -s md_0_1.tpr -f cluster.xtc -o cluster.xpm -g cluster.log -cl clusters.pdb -method gromos -cutoff 0.1

    #This for the system in general
    #I selected the Carbon alpha or backbone, the protein choice takes a lot of time so the system wil kill it
    #I seelcted alpha carbon or backbone for the output as well
    #In case this is not ok delete the index fiel from the code line (it shoud not be a problen becuase here you are analysing all the system but just in case)

#########Generating images suring the molecualr dynamics run
  for t in {0..100000..1000}; do           #0..100000..1000 means from 0 to 100000ps every 1000ps of snapshot
      gmx trjconv -s md_0_1.tpr -f md_0_1_noPBC.xtc -n index.ndx -o snapshot_${t}ps.pdb -dump $t
  done
     #then select the numbers to evaluate if you want the protein (1) or the system (0), etc
#it is possible to also use this will print 1 or 17 or the needed number several times (the ones that you need)
    for t in {0..100000..1000}; do
        echo "Processing time $t ps...";
        printf "17\n" | gmx trjconv -s md_0_1.tpr -f md_0_1_noPBC.xtc -n index.ndx -o snapshot_${t}ps.pdb -dump $t; done
    done 

#this will generate different .pdb files that can be joint using is a single one using: 
cat snapshot1.pdb snapshot2.pdb snapshot3.pdb > combined_snapshots.pdb
#here is an automatic way to combine al the generated snapshots in one .pdb file:

    output_file="combined_snapshots.pdb"
    > $output_file  # Clear the output file if it exists

    for pdb_file in snapshot_*ps.pdb; do
        echo "Adding $pdb_file to $output_file..."
        echo "MODEL $(basename $pdb_file .pdb | grep -o '[0-9]*')" >> $output_file
        cat "$pdb_file" >> $output_file
        echo "ENDMDL" >> $output_file
    done

#If you upload each snapshot separatelly and combine them in pymol, then aligned them to generate a superimpose picture with all the snapshots
#it seems there is no automatic way to do this, so you will have to do it manually in pymol or try to find a pymol script

#Interaction analysis
#you can just se the interaction_analysis.py file to generate the heatmaps of intercation and the index file for the analysis in gromacs
#(pair wise analysis, minimun distance interaction and number of hydrogen bonds). 
#for this analysis always use the md_0_1.xtc (it is going to be that file every time you want to generate a heatmail with MDAnalysis in python, do nto use the md_0_1_noPBC,xtc)
#here you will generate a interacting_residues_cogs.ndx which is an index file that separates only the residues (for each protein) that are interacting between these 2 proteins
#below an specific cutof porint (normaly below 5A), whit this index file oyu can perform the minimun distance, pariwise distance and number of hidrogen bonds analysis in GROMACS

#minimun distance 
gmx mindist -s md_0_1.tpr -f md_0_1.xtc -n interacting_residues_cogs.ndx -od mindist.xvg -on num_contact.xvg -d 0.5
     #the interacting_residues_cogs.ndx is the ndx file generated in the interaction_analysis.py, the -d is the distance in nm

#pairwise distance
gmx pairdist -s md_0_1.tpr -f md_0_1.xtc -n interacting_residues_cogs.ndx -o pairdist.xvg -ref Interacting_Protein1 -sel Interacting_Protein2
     #-ref Interacting_Protein1 -sel Interacting_Protein2 were determined in interacting_residues_cogs.ndx

#Hidrogen bonds
gmx hbond -s md_0_1.tpr -f md_0_1_noPBC1.xtc -n interacting_residues_cogs.ndx -num hbondsnew.xvg
     #this tells you the number of hidrogen bonds present in the interactions. 

#It is posible to perform a salt bridge analysis, the code is in interaction_analysis.py


#secondary structure analysis
gmx dssp -f md_0_1.xtc -s md_0_1.tpr -o structure.xvg -num numstruc.xvg
    #This will generate a .dat file that wil be used in the python script to generate the secondary structure map to see the change of secondary structures along time

#MMPBSA analysis 
   #First the groups have to be wel deifned in the index file

module load gromacs
module load gmx_mmpbsa
   #load both modules (gromacs and gmx_mmbpsa) at the same time

gmx_MMPBSA --create_input gb 
    #this is to generate a mmbpsa.in file

gmx_MMPBSA -i mmpbsa.in -cs md_0_1.tpr -ct md_0_1.xtc -ci indexfinal3.ndx -cg 17 18 -o results_mmpbsa.dat -eo results_mmpbsa.csv
   #in this comand the numbers 17 and 18 are the receptor and ligand repectively. Both have to be specified in this commandline

#for now it seems it only works with leaprc.protein.ff14SB forcefield, I could not run it with AMBER or Amber99SB-ILDN forcefields, maybe try Amber
