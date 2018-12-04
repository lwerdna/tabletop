#!/bin/bash

# echo commands
set -x

for file in tiles*.png; do
	# this is from imagemagick
	convert $file -units "PixelsPerInch" -density 300 $file
done
