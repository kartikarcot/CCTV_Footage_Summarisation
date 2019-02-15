import cv2
import numpy as np

def blend_image(bg, fg, mask):
    """
    Poisson blending of the foreground object into the background image 
    using seamless clone function of OpenCV

    Args:
        bg: Colour background image 
        fg: Colour foreground object with same dimensions aas bg
        mask: Greyscale mask of the foreground object

    Returns: The blended image
    """
    
    # We need to find the center of a rectangle that bounds all the white pixels in the mask.
    # The center is passed as a parameter to the seamless blending function to 
    # position the object in the same position as in the mask.
    
    width, height, _ = np.shape(bg)
    _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # find the bounding points of the contour
    x,y,w,h = cv2.boundingRect(contours[0])
    
    # bottom right co-ordinates
    x1 = x + w
    y1 = y + h

    # if more then 1 contour is found, draw a bounding rectangle 
    # around the entire set of countours
    for i in range(1, len(contours)):

        # find bounding rectangle
        x_, y_, w_, h_ = cv2.boundingRect(contours[i])

        # convert from (x,w) to (x,y) system
        # new end point
        x2 = x_ + w_
        y2 = y_ + h_

        # update top edge
        if x_ < x:
            x = x_
        # update left edge
        if y_ < y:
            y = y_
        # update bottom edge
        if x2 > x1:
            x1 = x2 
        # update right line
        if y2 > y1:
            y1 = y2
    
    # Find the updated width and height using the new bottom-right point
    w = x1 - x
    h = y1 - y

    result = cv2.seamlessClone(fg, bg, mask, (int(x+w/2), int(y+h/2)), cv2.NORMAL_CLONE)
    
    return result

