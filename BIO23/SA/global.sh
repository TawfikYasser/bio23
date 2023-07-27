#!/bin/bash

# Initialize variables
sequence1=""
sequence2=""
alignment=""

# Function to display usage message
function usage {
  echo "Usage: $(basename "$0") -s <sequence1.fasta> -q <sequence2.fasta> -o <alignment_output>"
  exit 1
}

# Parse command-line options using getopts
while getopts "s:q:o:" opt; do
  case $opt in
    s) sequence1="$OPTARG";;
    q) sequence2="$OPTARG";;
    o) alignment="$OPTARG";;
    \?) usage;;
    :) echo "Option -$OPTARG requires an argument"; usage;;
  esac
done

# Check if mandatory options are provided
if [[ -z "$sequence1" || -z "$sequence2" || -z "$alignment" ]]; then
  usage
fi

output_directory="/home/tawfik/SSDData/NU/Research/Courses/BIO/BIOPROJECT/BIO23/SA/globalData"

# Perform global alignment using EMBOSS Needle
needle -asequence "$sequence1" -bsequence "$sequence2" -gapopen 10 -gapextend 0.5 -outfile "$output_directory/$alignment"


