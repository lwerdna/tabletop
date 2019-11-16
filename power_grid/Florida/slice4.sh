#!/bin/sh

# input image is 1980x1530 so slices are each 990x765
convert -crop 990x765+0+0 power_grid_fl.png page1.png
convert -crop 990x765+990+0 power_grid_fl.png page2.png
convert -crop 990x765+0+765 power_grid_fl.png page3.png
convert -crop 990x765+990+765 power_grid_fl.png page4.png
