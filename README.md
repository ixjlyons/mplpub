mplpub
======

mplpub is a collection of functions for taking a carefully made matplotlib
figure and getting it ready for showtime in a document.

Currently implemented functions:

- `tight_layout`: Uses matplotlib's `tight_layout`, but centers the "plot
  contents" within the figure to counteract y axis labels and y axis tick
  labels pushing the plot axes too far to the right.
