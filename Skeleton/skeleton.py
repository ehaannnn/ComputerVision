import numpy as np
import cv2
import copy

img = cv2.imread("skeleton.jpg",0)
_,thresh = cv2.threshold(img,150,255,cv2.THRESH_BINARY)

rows,cols = thresh.shape
for i in range(rows):
	for j in range(cols):
		if thresh[i,j] == 0:
			thresh[i,j] = 1
		else:
			thresh[i,j] = 0


def distanceTransform(img):
	rows,cols = img.shape
	ret = copy.deepcopy(img)
	it = cols/2
	for _ in range(it):
		for i in range(1,rows-1):
			for j in range(1,cols-1):
				tmp = min(ret[i,j],ret[i-1,j],ret[i+1,j],ret[i,j-1],ret[i,j+1])
				if ret[i,j] == tmp:
					ret[i,j] = img[i,j] + tmp
	return ret

dist_transform = cv2.distanceTransform(thresh,cv2.cv.CV_DIST_L2,5)
#dist_transform = distanceTransform(thresh)
#print img[165,197]
cv2.imwrite("test1.jpg",dist_transform)

def getSkeleton(img):
	rows,cols = img.shape
	ret = copy.deepcopy(img)
	for i in range(1,rows-1):
		for j in range(1,cols-1):
			tmp = max(img[i][j],img[i-1,j],img[i+1,j],img[i,j-1],img[i,j+1])
			if img[i,j] == tmp:
				ret[i,j] = 0
			else:
				ret[i,j] = 255
	return ret

skeleton = getSkeleton(dist_transform)
cv2.imwrite("test2.jpg",skeleton)