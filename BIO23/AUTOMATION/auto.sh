#!/bin/bash

# Check if the user provided enough arguments
if [ $# -lt 4 ]; then
    echo "Usage: $0 <db> <accession_number> <num_alignments> <msa_algorithm>"
    echo "msa_algorithm options: mft (MAFFT), clo (Clustal Omega)"
    exit 1
fi

# Access the values of db, accession, num_alignments, and msa_algorithm as command-line arguments
db=$1
accession_number=$2
num_alignments=$3
msa_algorithm=$4

# Trim leading and trailing whitespaces from the accession number
accession_number=$(echo "$accession_number" | xargs)

# Specify the output directory (can be made configurable or use relative paths)
output_directory="/home/tawfik/SSDData/NU/Research/Courses/BIO/BIOPROJECT/BIO23/AUTOMATION"

# Step 1: Search for the sequence in NCBI using the provided accession number
echo "Searching for the sequence with accession number: $accession_number in database $db"
url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=$db&id=$accession_number&rettype=fasta&retmode=text"

# Use the "curl" command to fetch the data and save it directly to the desired path
if curl --fail -o "$output_directory/$accession_number.fasta" "$url"; then
  echo "Sequence $accession_number retrieved from database $db and saved to $output_directory/$accession_number.fasta"
else
  echo "Error: Unable to retrieve sequence $accession_number from database $db. Please check that the accession number and database name are correct."
  exit 1
fi

# Check if alignment_results.txt exists, if not perform Step 2
alignment_results_file="$output_directory/alignment_results.txt"

if [ ! -f "$alignment_results_file" ]; then
  # Step 2: Perform Pairwise Sequence Alignment using BLAST+
  echo "Performing Pairwise Sequence Alignment using BLAST+"
  blastn -query "$output_directory/$accession_number.fasta" -db nt -outfmt '7' -remote -num_alignments "$num_alignments" > "$alignment_results_file"
else
  echo "Skipping Step 2 as alignment_results.txt already exists."
fi

# Array to store unique Subject accession.version values
declare -a subject_accessions

# Extract unique Subject accession.version values from the alignment_results.txt file
while IFS=$'\t' read -r _ subject_accession _; do
  # Add the accession to the array if it's not empty and not already in the array
  if [[ -n $subject_accession && ! " ${subject_accessions[@]} " =~ " $subject_accession " ]]; then
    subject_accessions+=("$subject_accession")
  fi
done < "$alignment_results_file"

# Step 3: Fetch the sequence files for each unique Subject accession.version and save them in a single file readyForMSA.fasta
ready_for_msa_file="$output_directory/readyForMSA.fasta"
echo "" > "$ready_for_msa_file" # Clear the file if it already exists

for subject_accession in "${subject_accessions[@]}"; do
  subject_url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=$db&id=$subject_accession&rettype=fasta&retmode=text"

  if curl --fail -o - "$subject_url" >> "$ready_for_msa_file"; then
    echo "Sequence $subject_accession retrieved from database $db and added to $ready_for_msa_file"
  else
    echo "Error: Unable to retrieve sequence $subject_accession from database $db. Please check the accession number and database name."
    exit 1
  fi
done

# Step 4: Perform Multiple Sequence Alignment based on the chosen algorithm if msa_output.fasta does not exist
msa_output_file="$output_directory/msa_output.fasta"

if [ ! -f "$msa_output_file" ]; then
  if [ "$msa_algorithm" == "clo" ]; then
    echo "Performing Multiple Sequence Alignment using Clustal Omega"
    clustalo -i "$ready_for_msa_file" -o "$msa_output_file" --output-order=input --verbose --force
  elif [ "$msa_algorithm" == "mft" ]; then
    echo "Performing Multiple Sequence Alignment using MAFFT"
    mafft --auto "$ready_for_msa_file" > "$msa_output_file" 2>/dev/null
  else
    echo "Error: Invalid value for msa_algorithm. Please choose either 'mft' (MAFFT) or 'clo' (Clustal Omega)."
    exit 1
  fi

  echo "Multiple Sequence Alignment completed using $msa_algorithm. Results saved to $msa_output_file"
else
  echo "Skipping Step 4 as msa_output.fasta already exists."
fi

# Step 5: Draw the phylogenetic tree using FastTree
phylogenetic_tree_file="$output_directory/phylogenetic_tree.nwk"

if [ ! -f "$phylogenetic_tree_file" ]; then
  echo "Drawing the phylogenetic tree using FastTree"
  FastTree -nt "$msa_output_file" > "$phylogenetic_tree_file"
  echo "Phylogenetic tree generated and saved to $phylogenetic_tree_file"
else
  echo "Skipping Step 5 as the phylogenetic_tree.nwk file already exists."
fi



# Step 6: Call TreeVis.py and pass the path of phylogenetic_tree.nwk to it
python3 "$output_directory/TreeVis.py" "$output_directory/phylogenetic_tree.nwk"
