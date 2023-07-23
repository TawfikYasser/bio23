#!/bin/bash
# Access the values of db and accession as command-line arguments
db=$1
accession=$2
# Build the URL to retrieve the sequence in FASTA format from the NCBI E-utilities API
url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=$db&id=$accession&rettype=fasta&retmode=text"

if curl --fail -o $accession.fasta $url; then
  # Print a message indicating the sequence has been retrieved
  echo "Sequence $accession retrieved from database $db and saved to $accession.fasta"
  # sequence=$(cat "$accession.fasta")
  # echo "$sequence"
else
  # Print an error message if the URL is missing or invalid
  echo "Error: Unable to retrieve sequence $accession from database $db. Please check that the accession number and database name are correct."
fi