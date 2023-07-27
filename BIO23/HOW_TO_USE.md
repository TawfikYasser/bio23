# Instructions for Running the Automation Script and Scripts in the bio23 Project:

## Before you begin:
Make sure you have installed the required libraries and modules for the bio23 project:

- Python3:
Depending on your operating system, Python3 may already be installed. If not, visit the official Python website (https://www.python.org/) and follow the installation instructions for your OS.

- tkinter:
sudo apt-get install python3-tk

- BLAST:
https://blast.ncbi.nlm.nih.gov/Blast.cgi

- MAFFT:
sudo apt-get install mafft

- Clustal Omega:
sudo apt-get install clustalo

- Muscle:
sudo apt-get install muscle

- phyml:
sudo apt-get install phyml

- FastTree:
sudo apt-get install fasttree


## Now, follow the step-by-step instructions for running each script and the graphical user interface (GUI) in the bio23 project:

### 1. GUI: <br>
a. Navigate to the project directory <bio23>. <br>
b. Open the terminal. <br>
c. Execute the following command: python3 gui.py <br>

### 2. Database Retrieval from NCBI: <br>
a. Go to the project directory <bio23/NCBI>. <br>
b. Open the terminal. <br>
c. Run the following command: ./NCBI/ncbi_script.sh <db-name> <accession-number> <br>

### 3. Sequence Alignment: <br>
a. Change to the project directory <bio23/SA>. <br>
b. Open the terminal. <br>
c. For global sequence alignment, run: ./SA/global.sh -s <saQu_filePath> -q <saRef_filePath> -o <sa_output_file_name> <br>
d. For local sequence alignment, run: ./SA/local.sh -d <saRef_filePath> -q <saQu_filePath> -o <sa_output_file_name> <br>

### 4. Multiple Sequence Alignment: <br>
a. Switch to the project directory <bio23/MSA>. <br>
b. Open the terminal. <br>
c. To perform multiple sequence alignment, execute: <br>
With file input: ./MSA/MSA.sh -msaTool <algorithm> -outName <output_file_name> -seqPath <msa_filePath> <br>
With paste input: ./MSA/MSA.sh -msaTool <algorithm> -outName <output_directory> -seqPaste <<EOF EOF> <br>

### 5. Phylogenetic Tree: <br>
a. Move to the project directory <bio23/PTREE>. <br>
b. Open the terminal. <br>
c. Run the following command: ./PTREE/PHYLO.sh --inName <tree_filePath> <br>

### 6. Full Automation: <br>
a. Navigate to the project directory <bio23/AUTOMATION>. <br>
b. Open the terminal. <br>
c. Run the automation script using the command: ./AUTOMATION/auto.sh <db> <accession-number> <alignNumber> <algorithm> <br>

