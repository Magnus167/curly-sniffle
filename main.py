# %%
#imports
from PIL import Image
import numpy as np
from numpy import array
from os import path
import cv2
import matplotlib.pyplot as plt
from time import sleep

# %%
def load_png_to_array(fileName='./img.png'): # loads and returns png as a numpy array
    img = Image.open(fileName)
    img = img.convert('L') # convert to grayscale
    img = np.array(img)
    return img

# %%
def reduce_line_thickness(img, factor=2): # applies gaussian blur to img
    img = cv2.GaussianBlur(img, (3, 3), 0)
    # save image
    #cv2.imwrite('blurred.png', img)
    return img

# %%
def is_approximately_equal(a, b, epsilon=0.0001): # boolean, if a and b are approximately equal
    return abs(a - b) < epsilon

# %%
def fits_in_line(line=[[0, 0], [1, 1]], point=[0, 0]):
    '''
    (y3-y2)/(x3-x2) = (y2-y1)/(x2-x1)
    ->(y3-y2)*(x2-x1) = (y2-y1)*(x3-x2) avoids division by zero explosive values
    '''
    return is_approximately_equal((point[0] - line[-1][0])*(line[-1][1] - line[-2][1]) , (line[-1][0] - line[-2][0])*(point[1] - line[-1][1]))

# %%
def pts_to_lines(p): # converts a list of points to a list of lines, where each line is a list of points.   
    lines = [[p[0], p[1] if len(p)>1 else p[0]]]
    for i in range(2, len(p)-2):
        if fits_in_line(lines[-1], p[i]):
            lines[-1].append(p[i])
        else:
            lines.append([p[i-1],p[i]])
    for l in range(len(lines))[::-1]:
        if len(lines[l]) < 2:
            lines.pop(l)
    return lines

# %%
def get_centre_of_mass(pts): # gets com of a list of points
    x = 0
    y = 0
    for p in pts:
        x += p[0]
        y += p[1]
    return [int(x/len(pts)), int(y/len(pts))]

# %%
def get_polar_coordinates(pts, centre): # gets polar coordinates of a list of points, with respect to a centre=get_centre_of_mass(pts)
    polar_pts = []
    for p in pts:
        polar_pts.append([np.sqrt((p[0]-centre[0])**2 + (p[1]-centre[1])**2), np.arctan2(p[1]-centre[1], p[0]-centre[0])])
    return polar_pts
    # get_centre_of_mass(pts) can be called here as well, however this allows you to set a centre without editing this fx.

# %%
def sort_by_angle(pts): 

    plrcrds = get_polar_coordinates(pts, get_centre_of_mass(pts))
    combined = [[plrcrds[i], pts[i]] for i in range(len(pts))]
    combined = sorted(combined, key=lambda x: x[0][1])
    return [p[1] for p in combined]

# %%
def trace_line(img):
    ''' find all black pixels in image '''
    black_pixels = []
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i][j] == 0:
                black_pixels.append((i,j))
    print('Found {} black pixels'.format(len(black_pixels)))
    print('Ratio to white',len(black_pixels)/(img.shape[0]*img.shape[1]))  
    print ('!Sorted by angle') 
    print (black_pixels)
    black_pixels = sort_by_angle(black_pixels)   
    print ('Sorted by angle') 
    print (black_pixels)
    lines = pts_to_lines(black_pixels)
    print('As lines')
    print(lines)
    return lines
    

# %%
def create_new_img(img, lines):
    new_img = np.zeros(img.shape)
    pts = np.where(img == 0)
    img[pts] = 255
    plt.plot(pts[1], pts[0], 'r.')
    return new_img

# %%
imgArr=load_png_to_array()
x = create_new_img(imgArr, trace_line(reduce_line_thickness(imgArr)))


