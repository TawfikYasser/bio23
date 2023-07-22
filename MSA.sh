#!/bin/bash

# Function to print the help message
print_help() {
  echo "Usage: $0 [OPTIONS]"
  echo "Perform multiple sequence alignment using Clustal Omega or MAFFT."
  echo "OPTIONS:"
  echo "  -h, --help                 Show this help message and exit."
  echo "  -msaTool   <TOOL>          Choose the MSA tool: 'clo' for Clustal Omega or 'mft' for MAFFT."
  echo "                             Use 'progressive' for Clustal Omega or 'iterative' for MAFFT."
  echo "  -seqPath   <FILE-PATH>     Provide the path of the sequence file."
  echo "  -seqPaste                  Specify if you want to paste the sequences as stdin, should be the last argument (optional if -seqPath is used)."
  echo "  -aloutput  <DIRECTORY>     Provide the path of the output directory (optional)."
  echo "  -outName   <FILENAME>      Specify the name of the output file (optional)."
  echo "  -algoOut                   Show the output of the algorithm itself (optional)."
}

# Function to perform MSA using Clustal Omega
clustal_omega_msa() {
  local input_file=$1
  local output_file=$2
  echo "Performing Clustal Omega MSA..."
  if [[ "$algo_out" == "true" ]]; then
    clustalo -i "$input_file" -o "$output_file" --output-order=input --verbose --force
  else
    clustalo -i "$input_file" -o "$output_file" --output-order=input --force > /dev/null 2>&1
  fi
  echo "Clustal Omega MSA completed."
}

mafft_msa() {
  local input_file=$1
  local output_file=$2
  echo "Performing MAFFT MSA..."
  if [[ "$algo_out" == "true" ]]; then
    mafft --auto "$input_file" > "$output_file" 2>/dev/null
  else
    mafft --auto "$input_file" > "$output_file" 2>/dev/null
  fi
  echo "MAFFT MSA completed."
}

# Main script
msaTool=""
seqPath=""
seqPaste=false
aloutput=""
outName=""
algo_out=false

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)
      print_help
      exit 0
      ;;
    -msaTool)
      shift
      case "$1" in
        clo|progressive)
          msaTool="clustal"
          ;;
        mft|iterative)
          msaTool="mafft"
          ;;
        *)
          echo "Invalid value for -msaTool: $1"
          print_help
          exit 1
          ;;
      esac
      shift
      ;;
    -seqPath)
      seqPath=$2
      shift 2
      ;;
    -seqPaste)
      seqPaste=true
      shift
      ;;
    -aloutput)
      aloutput=$2
      shift 2
      ;;
    -outName)
      outName=$2
      shift 2
      ;;
    -algoOut)
      algo_out=true
      shift
      ;;
    *)
      echo "Unknown argument: $1"
      print_help
      exit 1
      ;;
  esac
done

# Check if no arguments provided, show help message
if [[ -z "$msaTool" && -z "$seqPath" && "$seqPaste" == "false" && -z "$aloutput" && -z "$outName" ]]; then
  print_help
  exit 0
fi

if [[ "$seqPaste" == "true" ]]; then
  # Check if sequences were provided via standard input
  if ! [ -t 0 ]; then
    input_seq=$(cat -)
    input_file=$(mktemp)

    # If "outName" is not provided, generate a temporary name
    if [[ -z "$outName" ]]; then
      outName="ALOUT_$(date +%Y%m%d_%H%M%S)"
    fi

    # Save the input sequences to the temporary file
    echo "$input_seq" > "$input_file"
  else
    echo "No sequences provided. Please use -seqPaste followed by the full sequence content as <<EOF SEQUENCE EOF."
    exit 1
  fi
else
  if [[ -n "$seqPath" ]]; then
    input_file=$seqPath

    # If "outName" is not provided, use the input file name without extension
    if [[ -z "$outName" ]]; then
      outName=$(basename "${input_file%.*}")
    fi
  else
    echo "Please provide the path of the sequence file using -seqPath or use the -seqPaste option (if -seqPaste is used it should be the last argument)."
    exit 1
  fi
fi

output_file="${aloutput:-.}/$outName.fasta"   # Add .fasta extension to the output file name


# Perform MSA based on the chosen tool
if [[ "$msaTool" == "clustal" ]]; then
  clustal_omega_msa "$input_file" "$output_file"
else
  mafft_msa "$input_file" "$output_file"
fi

# Display ending message
echo "Multiple Sequence Alignment completed successfully!"
