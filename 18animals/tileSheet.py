margin = 128
margin = 128

width = margin + 256*8 + margin
height = margin + 256*9 + margin
size(width, height)

fill(1)
rect(0, 0, width, height)

x_start = margin
y_start = margin

def cut_guides(x, y):
    stroke(0)
    strokeWidth(1)
    
    # intersecting at bottom left corner
    line((0, y), (margin, y)) # W mark
    line((width-margin, y), (width, y)) # E mark
    line((x, 0), (x, margin)) # S mark
    line((x, height-margin), (x, height)) # N mark
    
    # intersecting at top right corner
    line((0, y+256), (margin, y+256)) # W mark
    line((width-margin, y+256), (width, y+256)) # E mark
    line((x+256, 0), (x+256, margin)) # S mark
    line((x+256, height-margin), (x+256, height))
     
# straights   
y = y_start
for col in range(3):
    x = x_start
    
    for row in range(8): 
        cut_guides(x, y)
            
        image('tileA.png', (x+1,y))
        image('tileA.png', (x+1,y+1))
        image('tileA.png', (x,y))
        image('tileA.png', (x,y+1))
                        
        x += 256
        
    y += 256

y += 0

# elbows
for col in range(3):
    x = x_start
    
    for row in range(8): 
        cut_guides(x, y)
            
        image('tileB.png', (x+1,y))
        image('tileB.png', (x+1,y+1))
        image('tileB.png', (x,y))
        image('tileB.png', (x,y+1))
                        
        x += 256
        
    y += 256

# tees
for col in range(3):
    x = x_start
    
    for row in range(8): 
        cut_guides(x, y)
            
        image('tileC.png', (x+1,y))
        image('tileC.png', (x+1,y+1))
        image('tileC.png', (x,y))
        image('tileC.png', (x,y+1))
                        
        x += 256
        
    y += 256

# done
saveImage('tileSheet.png')

