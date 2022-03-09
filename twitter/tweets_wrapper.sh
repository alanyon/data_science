#!/bin/bash -l
#SBATCH --qos=long
#SBATCH --mem=10G
#SBATCH --ntasks=8
#SBATCH --output=/net/home/h04/alanyon/data_science/twitter/output.out
#SBATCH --time=1800
#SBATCH --error=/net/home/h04/alanyon/data_science/twitter/output.err

# Load scitools
module load scitools

python tweets.py yes
