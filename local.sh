#!/bin/bash

# Initialize variables
refseq=""
qseq=""
outName=""

# Parse command-line options and arguments using getopts
while getopts ":d:q:o:" opt; do
  case $opt in
    d) refseq="$OPTARG";;   # Option -d specifies the protein FASTA file (BLAST database)
    q) qseq="$OPTARG";;     # Option -q specifies the protein query sequences FASTA file
    o) outName="$OPTARG";;  # Option -o specifies the output file name
    \?) echo "Invalid option -$OPTARG" >&2; exit 1;;
    :) echo "Option -$OPTARG requires an argument" >&2; exit 1;;
  esac
done

# Check if mandatory arguments are provided
if [[ -z "$refseq" || -z "$qseq" || -z "$outName" ]]; then
  echo "Usage: $(basename "$0") -d <protein_FASTA> -q <query_FASTA> -o <output_file>"
  exit 1
fi

# Create the BLAST database using makeblastdb
makeblastdb -in "$refseq" -dbtype prot

# Perform the BLAST search using blastp
blastp -query "$qseq" -db "$refseq" -out "$outName"
