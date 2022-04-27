# TreeShears

Trees made with huge numbers of sequences tend to accumulate spurious small clades which claim to be intermediates on the way to big clades, but are almost always in fact sequencing artifacts. TreeShears applies a heuristic to remove these by looking at each node of the tree and seeing if any sub-clades are completely dwarfed by sibling clades. If so it removes the tiny clades as spurious.
