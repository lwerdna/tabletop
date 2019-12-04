width = 256
height = 256
size(width, height)

xcenter = width/2
ycenter = height/2

# background
fill(0xFF, 0xac, 0)
rect(0, 0, width, height)

def rect_centered(x, y, width, height):
    rect(x - width/2, y - width/2, width, height)

width_track = width/8
width_track_bg = 1.4 * width_track


lineCap('round')

# track background
stroke(255, 255, 255)
fill(255, 255, 255)
strokeWidth(width_track_bg)
# middle to North
line((width/2, height/2), (width/2,height))
# middle to East
line((width/2, height/2), (width,height/2))

# track foreground
stroke(0)
strokeWidth(width_track)
# middle to North
line((width/2, height/2), (width/2,height))
# middle to East
line((width/2, height/2), (width,height/2))


# done
saveImage('tileB.png')