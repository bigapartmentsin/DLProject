#!/bin/bash
#
#SBATCH --job-name=main
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=100GB
#SBATCH --time=47:00:00

module purge
module load python3/intel/3.5.3
module load numpy/python3.6/intel/1.14.0

for i in 'cna_eng' 'wpb_eng' 'afp_eng' 'xin_eng' 'apw_eng' 'ltw_eng' 'nyt_eng'
do
	python3 cleaner.py --source "$i"
        echo $i done...
done

