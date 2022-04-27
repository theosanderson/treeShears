import treeswift
import subprocess
import sys
import random
import argparse

parser = argparse.ArgumentParser(description='Treeshears')
parser.add_argument('-i', '--input', help='Input MAT file', required=True)
parser.add_argument('-o', '--output', help='Output MAT file', required=True)
parser.add_argument('-T', '--threshold', help='Threshold', default=1000)

args = parser.parse_args()

threshold = int(args.threshold)
treefile = args.input

random_text_name = random_text_name = random.randint(1, 1000000)
command = f"matUtils extract -i {treefile} -t ./{random_text_name}.nwk"

subprocess.call(command, shell=True)

# Read file with treeswift
contents = open(f"./{random_text_name}.nwk", "r").read()

tree = treeswift.read_tree_newick(contents)

for node in tree.traverse_postorder():
    node.total_descendants = node.num_children() + sum(
        [x.total_descendants for x in node.children])

to_remove = set()
import tqdm
for node in tqdm.tqdm(tree.traverse_preorder()):
    if node.num_children() > 1:
        largest_child = max(node.children, key=lambda x: x.total_descendants)
        others = node.total_descendants - (largest_child.total_descendants + 1)
        if largest_child.total_descendants / others > threshold:
            for child_node in node.children:
                if child_node != largest_child:
                    if child_node.is_leaf():
                        to_remove.add(child_node.label)
                    else:
                        for leaf in child_node.traverse_leaves():
                            to_remove.add(leaf.label)

to_remove_file = open(f"./{random_text_name}_to_remove.txt", "wt")
for item in to_remove:
    to_remove_file.write(f"{item}\n")
to_remove_file.close()

command = f"matUtils extract -i {treefile} -p -s ./{random_text_name}_to_remove.txt -o {args.output} -O"
subprocess.call(command, shell=True)

command = f" matUtils extract -i {args.output} -l {args.output}.taxonium.pb -g ncbiGenes.gtf -f wuhCor1.fa -M public-latest.metadata.tsv -G 0.15"
subprocess.call(command, shell=True)

# clean up
command = f"rm ./{random_text_name}.nwk"
subprocess.call(command, shell=True)
command = f"rm ./{random_text_name}_to_remove.txt"
subprocess.call(command, shell=True)
