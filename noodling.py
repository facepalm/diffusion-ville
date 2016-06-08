import numpy as np
import cv2
import skimage.filters




field = np.zeros((300,200),np.float32)


while True:
    field[100,100] = 1.0
    
    field = skimage.filters.gaussian(field,2)
    
    cv2.imshow('field', field)
    cv2.waitKey(10)
