import cv2
import numpy as np
from matplotlib import pyplot as plt

class EdgeDecectionandGaussianBlur():

    def __init__(self, minval=0, maxval=0, kernalX=5, kernalY=5, sigmaX=0):
        self.minval = minval
        self.maxval = maxval
        self.kernalX = kernalX
        self.kernalY = kernalY
        self.sigmaX = sigmaX


    def edge_detection(self):
        img = cv2.imread('images/single_rose.jpg',0)
        edges = cv2.Canny(img,self.minval,self.maxval)
        return edges
        #
        # plt.subplot(121),plt.imshow(img,cmap = 'gray')
        # plt.title('Original Image'), plt.xticks([]), plt.yticks([])
        # plt.subplot(122),plt.imshow(edges,cmap = 'gray')
        # plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
        # plt.show()

    def gaussian_blur(self):
        #sigmaY is the same as sigmaX
        img = cv2.imread('images/single_rose.jpg', 0)
        blur = cv2.GaussianBlur(img, (self.kernalX, self.kernalY), self.sigmaX)
        return blur

        # plt.subplot(121), plt.imshow(img, cmap='gray')
        # plt.title('Original Image'), plt.xticks([]), plt.yticks([])
        # plt.subplot(122), plt.imshow(blur, cmap='gray')
        # plt.title('Blur Image'), plt.xticks([]), plt.yticks([])
        # plt.show()

