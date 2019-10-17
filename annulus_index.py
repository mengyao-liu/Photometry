import numpy as np
import matplotlib.pyplot as plt

def go(size,center,r_out,r_in=0,deg=None):
    '''
    Return the pixel index within a given circle of a 2D image 
    grid.shape = (y,x)
    
    size - image size [x,y]
    center - cener in pixel [x0,y0]
    r - radius of the circle in pixel
    deg - [start, span]
          start: [-180, 180]
          span: (0, 180], counter clockwise
    
    '''

    #grid = np.zeros((size[1],size[0]), dtype=np.bool)
    
    # Generate arrays of indices/coordiates so we can do the calculations the Numpy way, without resorting to loops
    xx = np.arange(size[0])
    yy = np.arange(size[1])

    # Calling Mr Pythagoras: Find the pixels that lie inside this circle
    limit_out = (yy[:,None] - center[1]) ** 2 + (xx[None, :] - center[0]) ** 2 <= (r_out ** 2) 
    limit_in = (yy[:,None] - center[1]) ** 2 + (xx[None, :] - center[0]) ** 2 >= (r_in ** 2)
    # do grid & inside and initialize grid with ones for intersection instead of union
    grid = limit_out & limit_in

    #plt.imshow(grid)
    #plt.show()

    
    if deg != None:
        if deg[0]>-90 and deg[0]<90:
            sector1 = (yy[:,None] - center[1]) > (xx[None, :] - center[0])*np.tan(deg[0]*np.pi/180.)
            if deg[0]+deg[1]<90:                 
                sector2 = (yy[:,None] - center[1]) < (xx[None, :] - center[0])*np.tan((deg[0]+deg[1])*np.pi/180.)
            elif deg[0]+deg[1]==90:
                sector2 = xx[None, :] > center[0]
            else:                
                sector2 = (yy[:,None] - center[1]) > (xx[None, :] - center[0])*np.tan((deg[0]+deg[1])*np.pi/180.)

        if deg[0] == -90:
            sector1 = xx[None, :] > center[0]
            if deg[0]+deg[1]==90:   
                sector2 = xx[None, :] > center[0]
            else:
                sector2 = (yy[:,None] - center[1]) < (xx[None, :] - center[0])*np.tan((deg[0]+deg[1])*np.pi/180.)

        if deg[0] == 90:
            sector1 = xx[None, :] < center[0]
            if deg[0]+deg[1]==270:   
                sector2 = xx[None, :] < center[0]
            else:
                sector2 = (yy[:,None] - center[1]) > (xx[None, :] - center[0])*np.tan((deg[0]+deg[1])*np.pi/180.)
                                
                
        else:
            sector1 = (yy[:,None] - center[1]) < (xx[None, :] - center[0])*np.tan(deg[0]*np.pi/180.) 
            if deg[0]+deg[1]<270 and deg[0]+deg[1]>90:                
                sector2 = (yy[:,None] - center[1]) > (xx[None, :] - center[0])*np.tan((deg[0]+deg[1])*np.pi/180.)
            elif deg[0]+deg[1]==270:
                sector2 = xx[None, :] < center[0]
            else:
                sector2 = (yy[:,None] - center[1])< (xx[None, :] - center[0])*np.tan((deg[0]+deg[1])*np.pi/180.)
                
                
        print sector1
        sector = sector1 & sector2       
        grid = grid & sector
                
                
        
    plt.imshow(grid)
    plt.gca().invert_yaxis()
    plt.show()
    
    
    
    
    return grid