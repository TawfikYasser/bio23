#!/bin/bash

# initializing default values for use in the code below
inputfile="sequence.msa.fasta" # use as a default value if user has no input

# code responsible for parsing the arguments
while [[ $# -gt 0 ]]; do
	key="$1"
	case $key in
	    -i|--inName) # for inputting file name
	    inputfile="$2"
	    shift
	    shift
	    ;;
	    *)
	    echo "Unknown option: $1" # if another option entered
	    exit 1
	    ;;
	esac
 done

# displaying the entered values for the arguments
echo "File: $inputfile"

printf "\n"

echo "muscle refine:"
muscle -in "$inputfile" -out /home/tawfik/SSDData/NU/Research/Courses/BIO/BIOPROJECT/BIO23/PTREE/aseq.refined.phylip -refine -phyi
printf "\n"

echo "Phyml Tree:"
phyml -i /home/tawfik/SSDData/NU/Research/Courses/BIO/BIOPROJECT/BIO23/PTREE/aseq.refined.phylip -d nt -m GTR -o tlr
printf "\n"
