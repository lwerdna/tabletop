from tile import width as twidth
from tile import height as theight

print('using tile width: %d' % twidth)
width = 2486
height = 1920

margin = 256

size(width, height)

fill(1)
rect(0, 0, width, height)

x_start = margin
y_start = margin

def cut_guides(x, y):
    stroke(0)
    strokeWidth(1)
    
    margin_mod = .75 * margin 
    
    # intersecting at bottom left corner
    line((0, y), (margin_mod, y)) # W mark
    line((width-margin_mod, y), (width, y)) # E mark
    line((x, 0), (x, margin_mod)) # S mark
    line((x, height-margin_mod), (x, height)) # N mark
    
    # intersecting at top right corner
    line((0, y+twidth), (margin_mod, y+twidth)) # W mark
    line((width-margin_mod, y+twidth), (width, y+twidth)) # E mark
    line((x+twidth, 0), (x+twidth, margin_mod)) # S mark
    line((x+twidth, height-margin_mod), (x+twidth, height))
     
rows = int((height-2*margin)/twidth)
cols = int((width-2*margin)/twidth)

queue = []
queue += ['tileA.png']*24
queue += ['tileB.png']*24
queue += ['tileBlank.png']*(cols+1)
queue += ['tileC.png']*24     

for row in range(rows):
    for col in range(cols):
        x = margin + col*twidth
        y = margin + row*twidth
        
        if not queue:
            continue
        fname = queue.pop()
            
        cut_guides(x, y)
            
        #image(fname, (x+1,y))
        #image(fname, (x+1,y+1))
        image(fname, (x,y))
        #image(fname, (x,y+1))
        
# done
saveImage('tileSheet.png')

