# page width
width = 2486
height = 1920
size(width, height)
margin = 128

# tile width
twidth = 170
# cell width, margin
cwidth = 200
cmargin =  (cwidth - twidth)/2
ncells_x  = int((width - (2*margin)) / cwidth)
ncells_y = int((height - (2*margin))  / cwidth)

print('ncells_x: ', ncells_x)
print('ncells_y: ', ncells_y)

def page_prep():
    # clear page
    fill(1)
    rect(0, 0, width, height)

    # draw cut guides
    stroke(0)
    for k in range(ncells_x+1):
        x = margin + k*cwidth
        line((x,0),(x,height)) # vert line
    
    for k in range(ncells_y+1):
        y = margin + k*cwidth
        line((0,y),(width,y)) # vert line
        
    fill(1)
    stroke(1)
    rect(0+.8*margin,0+.8*margin,width-1.6*margin,height-1.6*margin)

def rgb(r, g, b):
    return (r/255.0, g/255.0, b/255.0)
    
def rgbhex(v):
    return rgb(v>>16, (v>>8)&0xFF, v&0xff)

# queue and go
bglookup = {
    'radio_mil_tile_p75in.png':rgb(128,128,128),
    'water_tile_p75in.png':rgbhex(0xAFEEEE),
    'apple_tile_p75in.png':rgbhex(0xdd6c6c),
    'banana_tile_p75in.png':rgbhex(0xfff8dc),
    'grapes_tile_p75in.png':rgbhex(0xdda0dd),
    'egg_tile_p75in.png':rgbhex(0xffffff),
    'fish_tile_p75in.png':rgbhex(0x98FB98),
    'spear_tile_p75in.png':rgbhex(0xdeb887),
    'diamond_tile_p75in.png':rgbhex(0xFFFFFF),
    'leisure_tile_p75in.png':rgbhex(0xe6beff),
    'radio_cb_tile_p75in.png':rgbhex(0xff8c00),
    'radio_mil_tile_p75in.png':rgbhex(0xff8c00),
    'radio_t40_tile_p75in.png':rgbhex(0xff8c00),
}

queue = []
if True:
    queue += ['water_tile_p75in.png']*10
    queue += ['apple_tile_p75in.png']*20
    queue += ['banana_tile_p75in.png']*20
    queue += ['grapes_tile_p75in.png']*10
    queue += ['egg_tile_p75in.png']*28
    queue += ['fish_tile_p75in.png']*20
    queue += ['spear_tile_p75in.png']*20
    queue += ['diamond_tile_p75in.png']*12
    queue += ['leisure_tile_p75in.png']*40
    queue += ['radio_cb_tile_p75in.png']*14
    queue += ['radio_mil_tile_p75in.png']*14
    queue += ['radio_t40_tile_p75in.png']*12
else:
    queue += ['water_tile_p75in.png']*5
    queue += ['apple_tile_p75in.png']*5
    queue += ['banana_tile_p75in.png']*5
    queue += ['grapes_tile_p75in.png']*5
    queue += ['egg_tile_p75in.png']*5
    queue += ['fish_tile_p75in.png']*5
    queue += ['spear_tile_p75in.png']*5
    queue += ['diamond_tile_p75in.png']*5
    queue += ['leisure_tile_p75in.png']*5
    queue += ['radio_cb_tile_p75in.png']*5
    queue += ['radio_mil_tile_p75in.png']*5
    queue += ['radio_t40_tile_p75in.png']*5

for page_num in range(100):
    page_prep()

    for row in range(ncells_y):
        for col in range(ncells_x):
            if not queue:
                continue            
            
            x = margin + col*cwidth
            y = margin + row*cwidth

            fname = queue.pop()
            stroke(*bglookup[fname])        
            fill(*bglookup[fname])
            #fill(*rgbhex(0xc0c0c0))
            rect(x, y, cwidth, cwidth)
            image(fname, (x+cmargin, y+cmargin))
    
            
    
    fname = 'tilesheet%d.png' % page_num
    print('saving %s' % fname)
    saveImage(fname)
    
    if not queue:
        break
        



