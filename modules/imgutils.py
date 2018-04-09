"""
Some utility functions for image processing.
Some of these are copies or modifications from https://www.pyimagesearch.com/. Excellent blog!
"""
# coding: utf-8

# Standard imports
import os
import time
import datetime

# External imports
import cv2
import numpy

def detect_pattern(img, cascade, min_rectangle):
    """Pattern detection function.
    
        Args:
            img: a cv2 image.
            cascade: a CascadeClassifier object.
            min_rectangle: a two element tuple containing width and 
                           height of the smaller search window; small 
                           values rise the range of vision of our 
                           turret, but processing may become slower.
        
        Returns:
            Coordinates of the rectangle that contains the pattern 
            described by the classifier.
        
        Raises:
        
    """

    rects = cascade.detectMultiScale(img, 1.2, 3, 1, min_rectangle)

    if len(rects) == 0:
        return [], img
    rects[:, 2:] += rects[:, :2]
    return rects, img


def box(coords, img, color=(0,255,0)):
    """Draw a rectangle in an image.
    
        Args:
            coords: a list of lists. Each sublist has four elements, 
                    respectively, top-left and bottom-right, x and y.
                    examples: [[32, 56, 177, 214]] 
                              [[32, 56, 177, 214], [44, 53, 194, 217]]
            img: a cv2 image.
            color: a tuple of three elements, the BGR representation 
                   of a color for the rectangle.
                   Default is (127, 255, 0).
        
        Returns:
            The input image, with rectangles placed on the specified 
            coordinates.
        
        Raises:
    
    """
    
    for x1, y1, x2, y2 in coords:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
    return img


def rotate(img, degree):
    """Rotate an image.
    
        Args:
            img: a cv2 image.
            degree: the degree of rotation to apply. Rotation is done 
                    counterclockwise.
        
        Returns:
            The input cv2 image, rotated counterclockwise.
        
        Raises:
    
    """
    # Capture the dimensions of the image and compute its center
    (h, w) = img.shape[:2]
    center = (w / 2, h / 2)
    # Rotate image
    M = cv2.getRotationMatrix2D(center, degree, 1.0)
    return cv2.warpAffine(img, M, (w, h))

def rotate_bound(image, angle):
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)
 
    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = numpy.abs(M[0, 0])
    sin = numpy.abs(M[0, 1])
 
    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
 
    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
 
    # perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH))

def resize(img, width=None, height=None):
    """Resize an image.
    
        Args:
            img: a cv2 image.
            width: new width.
            height: new height.
        
        Returns:
            The input cv2 image, resized to new width and height.
        
        Raises:
    
    """
    
    # Get initial height and width
    (h, w) = img.shape[:2]
    
    # If just one of the new size parameters is given, keep aspect ratio
    if width and not height:
        height = h*(100/w)
    elif height and not width:
        width = w*(100/h)
    elif not height and not width:
        return img
    
    # Choose interpolation method based on type of operation, shrink or enlarge
    if width*height < w*h:
        return cv2.resize(img, (width, height), interpolation = cv2.INTER_AREA);
    else:
        return cv2.resize(img, (width, height), interpolation = cv2.INTER_LINEAR);


def crop(img, startx, endx, starty, endy):
    """Crop an image.

        Args:
            img: a cv2 image.
            startx: starting pixel in x direction.
            endx: ending pixel in x direction.
            starty: starting pixel in y direction.
            endy: ending pixel in y direction.

        Returns:
            The input cv2 image, cropped.

        Raises:

    """
    return img[starty:endy, startx:endx]
