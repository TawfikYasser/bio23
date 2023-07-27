#!/bin/bash

# Access the values of db and accession as command-line arguments
db=$1
accessions=$2

# Specify the output directory
output_directory="NCBI"

# Determine the output file name based on the number of accession numbers provided
if [[ $(echo "$accessions" | wc -w) == 1 ]]; then
  output_file="${accessions//./_}.fasta"
else
  output_file="sequences.fasta"
fi

# Loop over each accession number and retrieve its sequence
for accession in $accessions; do
  # Build the URL to retrieve the sequence in FASTA format from the NCBI E-utilities API
  url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=$db&id=$accession&rettype=fasta&retmode=text"

  # Use the "curl" command to fetch the data and append it to the output file
  if curl --fail $url >> "$output_directory/$output_file"; then
    # Print a message indicating the sequence has been retrieved and saved
    success_message+="$accession"$' '
  else
    # Print an error message if the URL is missing or invalid
    echo "Error: Unable to retrieve sequence $accession from database $db. Please check that the accession number and database name are correct."
  fi
done
echo "Sequence ${success_message}retrieved from database $db and appended to $output_directory/$output_file"
