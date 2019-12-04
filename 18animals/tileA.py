width = 256
height = 256
size(width, height)

# background
fill(0xff, 0xff, 0)
rect(0, 0, width, height)

# track background
stroke(255, 255, 255)
strokeWidth(1.4*(width/8))
line((width/2,0), (width/2,height))

# track foreground
stroke(0)
strokeWidth(width/8)
line((width/2,0), (width/2,height))

# done
saveImage('tileA.png')