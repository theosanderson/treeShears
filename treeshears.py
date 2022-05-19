import treeswift
import subprocess
import sys
import random
import argparse
import tempfile
import os
from alive_progress import alive_it

parser = argparse.ArgumentParser(description='Treeshears')
parser.add_argument('-i', '--input', help='Input MAT file', required=True)
parser.add_argument('-o', '--output', help='Output MAT file', required=True)
parser.add_argument('-T', '--threshold', help='Threshold', default=1000)

args = parser.parse_args()

threshold = int(args.threshold)
treefile = args.input

temp_dir = tempfile.mkdtemp()

command = f"matUtils extract -i {treefile} -d {temp_dir} -t tree.nwk"

subprocess.call(command, shell=True)

# Read file with treeswift
contents = open(f"{temp_dir}/tree.nwk", "r").read()

tree = treeswift.read_tree_newick(contents)

for node in tree.traverse_postorder():
    node.total_descendants = node.num_children() + sum(
        [x.total_descendants for x in node.children])

to_remove = set()

for node in alive_it(tree.traverse_preorder()):
    if node.num_children() > 1 and node != tree.root:
        largest_child = max(node.children, key=lambda x: x.total_descendants)
        for child_node in node.children:
                if ( child_node.total_descendants +1)* threshold < largest_child.total_descendants:
                    if child_node.is_leaf():
                        to_remove.add(child_node.label)
                    else:
                        for leaf in child_node.traverse_leaves():
                            to_remove.add(leaf.label)

to_remove_file = open(f"{temp_dir}/to_remove.txt", "wt")
for item in to_remove:
    to_remove_file.write(f"{item}\n")
to_remove_file.close()

#split args.output into directory and filename
output_dir, output_file = os.path.split(args.output)
output_dir = output_dir if output_dir.strip() != "" else "."

command = f"matUtils extract -i {treefile} -p -s {temp_dir}/to_remove.txt -d {output_dir} -o {output_file} -O"
print("Running",command)

subprocess.call(command, shell=True)
