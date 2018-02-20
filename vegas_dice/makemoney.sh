#!/bin/sh
# use ImageMagick to make printable pages from the individual notes images
# should make 6 pages for 54 notes (5x 60,70,80,90 and 6x of 10,40,50 and 8x of 20,30)

if [ ! -f "canvas.jpg" ]; then convert -size 2052x2580 xc:white canvas.png; fi

# 8x$20
composite -gravity NorthWest -geometry +64+64 cash20.png canvas.png cashpage0.png
composite -gravity NorthWest -geometry +1028+64 cash20.png cashpage0.png cashpage0.png
composite -gravity NorthWest -geometry +64+678 cash20.png cashpage0.png cashpage0.png
composite -gravity NorthWest -geometry +1028+678 cash20.png cashpage0.png cashpage0.png
composite -gravity NorthWest -geometry +64+1292 cash20.png cashpage0.png cashpage0.png
composite -gravity NorthWest -geometry +1028+1292 cash20.png cashpage0.png cashpage0.png
composite -gravity NorthWest -geometry +64+1906 cash20.png cashpage0.png cashpage0.png
composite -gravity NorthWest -geometry +1028+1906 cash20.png cashpage0.png cashpage0.png

# 8x$30
composite -gravity NorthWest -geometry +64+64 cash30.png canvas.png cashpage1.png
composite -gravity NorthWest -geometry +1028+64 cash30.png cashpage1.png cashpage1.png
composite -gravity NorthWest -geometry +64+678 cash30.png cashpage1.png cashpage1.png
composite -gravity NorthWest -geometry +1028+678 cash30.png cashpage1.png cashpage1.png
composite -gravity NorthWest -geometry +64+1292 cash30.png cashpage1.png cashpage1.png
composite -gravity NorthWest -geometry +1028+1292 cash30.png cashpage1.png cashpage1.png
composite -gravity NorthWest -geometry +64+1906 cash30.png cashpage1.png cashpage1.png
composite -gravity NorthWest -geometry +1028+1906 cash30.png cashpage1.png cashpage1.png

# 6x$10 + 2x$40
composite -gravity NorthWest -geometry +64+64 cash10.png canvas.png cashpage2.png
composite -gravity NorthWest -geometry +1028+64 cash10.png cashpage2.png cashpage2.png
composite -gravity NorthWest -geometry +64+678 cash10.png cashpage2.png cashpage2.png
composite -gravity NorthWest -geometry +1028+678 cash10.png cashpage2.png cashpage2.png
composite -gravity NorthWest -geometry +64+1292 cash10.png cashpage2.png cashpage2.png
composite -gravity NorthWest -geometry +1028+1292 cash10.png cashpage2.png cashpage2.png
composite -gravity NorthWest -geometry +64+1906 cash40.png cashpage2.png cashpage2.png
composite -gravity NorthWest -geometry +1028+1906 cash40.png cashpage2.png cashpage2.png

# 4x$40 + 4x$50
composite -gravity NorthWest -geometry +64+64 cash40.png canvas.png cashpage3.png
composite -gravity NorthWest -geometry +1028+64 cash40.png cashpage3.png cashpage3.png
composite -gravity NorthWest -geometry +64+678 cash40.png cashpage3.png cashpage3.png
composite -gravity NorthWest -geometry +1028+678 cash40.png cashpage3.png cashpage3.png
composite -gravity NorthWest -geometry +64+1292 cash50.png cashpage3.png cashpage3.png
composite -gravity NorthWest -geometry +1028+1292 cash50.png cashpage3.png cashpage3.png
composite -gravity NorthWest -geometry +64+1906 cash50.png cashpage3.png cashpage3.png
composite -gravity NorthWest -geometry +1028+1906 cash50.png cashpage3.png cashpage3.png

# 2x$50 + 5x$60 + 1x$70
composite -gravity NorthWest -geometry +64+64 cash50.png canvas.png cashpage4.png
composite -gravity NorthWest -geometry +1028+64 cash50.png cashpage4.png cashpage4.png
composite -gravity NorthWest -geometry +64+678 cash60.png cashpage4.png cashpage4.png
composite -gravity NorthWest -geometry +1028+678 cash60.png cashpage4.png cashpage4.png
composite -gravity NorthWest -geometry +64+1292 cash60.png cashpage4.png cashpage4.png
composite -gravity NorthWest -geometry +1028+1292 cash60.png cashpage4.png cashpage4.png
composite -gravity NorthWest -geometry +64+1906 cash60.png cashpage4.png cashpage4.png
composite -gravity NorthWest -geometry +1028+1906 cash70.png cashpage4.png cashpage4.png

# 4x$70 + 4x$80
composite -gravity NorthWest -geometry +64+64 cash70.png canvas.png cashpage5.png
composite -gravity NorthWest -geometry +1028+64 cash70.png cashpage5.png cashpage5.png
composite -gravity NorthWest -geometry +64+678 cash70.png cashpage5.png cashpage5.png
composite -gravity NorthWest -geometry +1028+678 cash70.png cashpage5.png cashpage5.png
composite -gravity NorthWest -geometry +64+1292 cash80.png cashpage5.png cashpage5.png
composite -gravity NorthWest -geometry +1028+1292 cash80.png cashpage5.png cashpage5.png
composite -gravity NorthWest -geometry +64+1906 cash80.png cashpage5.png cashpage5.png
composite -gravity NorthWest -geometry +1028+1906 cash80.png cashpage5.png cashpage5.png

# 1x$80 + 5x$90
composite -gravity NorthWest -geometry +64+64 cash80.png canvas.png cashpage6.png
composite -gravity NorthWest -geometry +1028+64 cash90.png cashpage6.png cashpage6.png
composite -gravity NorthWest -geometry +64+678 cash90.png cashpage6.png cashpage6.png
composite -gravity NorthWest -geometry +1028+678 cash90.png cashpage6.png cashpage6.png
composite -gravity NorthWest -geometry +64+1292 cash90.png cashpage6.png cashpage6.png
composite -gravity NorthWest -geometry +1028+1292 cash90.png cashpage6.png cashpage6.png


