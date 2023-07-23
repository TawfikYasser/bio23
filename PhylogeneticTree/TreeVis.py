from newick import loads
from Bio import Phylo
import matplotlib
import matplotlib.pyplot as plt
from sys import argv

tree = argv[1]

vis_tree = Phylo.read(tree,"newick")

fig = plt.figure(figsize=(10, 7), dpi=100) # create figure and set the size 

matplotlib.rc('font', size=12)             # fontsize of the leaf and node labels 
matplotlib.rc('xtick', labelsize=10)       # fontsize of x tick labels
matplotlib.rc('ytick', labelsize=10)       # fontsize of y tick labels

axes = fig.add_subplot(1, 1, 1)

Phylo.draw(vis_tree, axes=axes)
fig.savefig(tree.split(".")[0])

with open(tree,'r') as f:
    s=f.read()
s.replace('\n','')
print(loads(s)[0].ascii_art())