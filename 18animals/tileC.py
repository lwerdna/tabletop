from tile import *
size(width, height)

# background
fill(0x38/256.0, 0xac/256.0, 0)
rect(0, 0, width, height)

# track background
stroke(1)
fill(1)
strokeWidth(width_track_bg)
# middle to North
line((xcenter, ycenter), (xcenter,height))
# West to East
line((0, ycenter), (width,ycenter))

# track foreground
stroke(0)
strokeWidth(width_track)
# middle to North
line((xcenter, ycenter), (xcenter,height))
# West to East
line((0, ycenter), (width,ycenter))

# done
saveImage('tileC.png')