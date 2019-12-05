from tile import *

size(width, height)

# background
fill(1, 1, 0)
rect(0, 0, width, height)

# track background
stroke(1)
strokeWidth(width_track_bg)
line((xcenter, 0), (ycenter, height))

# track foreground
stroke(0)
strokeWidth(width_track)
line((xcenter, 0), (ycenter,height))

# done
saveImage('tileA.png')