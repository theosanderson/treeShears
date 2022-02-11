# TreeShears

Trees made with huge numbers of sequences tend to accumulate spurious small clades which claim to be intermediates on the way to big clades, but are almost always in fact sequencing artifacts. TreeShears applies a heuristic to remove these by looking at each node of the tree and seeing if one child clade makes up more than (e.g.) 99.9% of the descendant sequences. If so it removes the others as spurious.
