mplpub
======

mplpub is a collection of functions for taking a carefully made matplotlib
figure and getting it ready for showtime in a document.

Currently implemented functions:

- `vertical_aspect`: Adjust figure height and vertical spacing so a sub-plot 
  plotting area has a specified aspect ratio and the overall figure has 
  top/bottom margins from tight_layout.
- `horizontal_center`: Apply matplotlib's tight_layout to the left margin while
   keeping the plot contents centered.