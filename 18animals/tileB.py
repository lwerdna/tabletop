from tile import *

size(width, height)

# background
fill(0xFF, 0xac, 0)
rect(0, 0, width, height)

width_track = width/8
width_track_bg = 1.4 * width_track


lineCap('round')

# track background
stroke(1)
fill(1)
strokeWidth(width_track_bg)
# middle to North
line((xcenter, ycenter), (xcenter, height))
# middle to East
line((xcenter, ycenter), (width, ycenter))

# track foreground
stroke(0)
strokeWidth(width_track)
# middle to North
line((xcenter, ycenter), (xcenter, height))
# middle to East
line((xcenter, ycenter), (width, ycenter))


# done
saveImage('tileB.png')