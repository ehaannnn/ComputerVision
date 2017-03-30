import cv2
import numpy as np
from matplotlib import pyplot as plt
import operator

img = cv2.imread('lotto.jpg',0)
rows,cols = img.shape

_,thresh=cv2.threshold(img,230,255,cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)


maxArea = 0
cntIndex = 0
for i in range(len(contours)):
	cnt = contours[i]
	area = cv2.contourArea(cnt)
	if (maxArea < area):
		maxArea = area
		cntIndex = i

cnt = contours[cntIndex]
#cv2.drawContours(img, contours, -1, (0,255,0), 3)
#cv2.drawContours(img, [cnt], 0, (0,255,0), 3)


rect = cv2.minAreaRect(cnt)
M = cv2.getRotationMatrix2D((cols/2,rows/2),rect[2],1)

cx,cy = rect[0]
width,height = rect[1]
cx = int(cx)
cy = int(cy)
width = int(width)
height = int(height)
dst = cv2.warpAffine(img,M,(cols,rows))
_,dst=cv2.threshold(dst,200,255,cv2.THRESH_BINARY)
dst = dst[cy-height/2+10:cy+height/2-10,cx-width/2:cx+width/2]
#cv2.imwrite('test2.png',dst)

def horizontalProjection(image):
	maxNum = 0
	line = {}
	rows,cols = image.shape
	for i in range(rows):
		tmp = 0
		for j in range(cols):
			if image[i,j]==0:
				tmp = tmp + 1
		line[i] = tmp
	return line

def verticalProjection(image):
	maxNum = 0
	line = {}
	rows,cols = image.shape
	for i in range(cols):
		tmp = 0
		for j in range(rows):
			if image[j,i]==0:
				tmp = tmp + 1
		line[i] = tmp
	return line

line = horizontalProjection(dst)

line = sorted(line.items(),key=operator.itemgetter(1))
low = line[len(line)-1][0]
high = line[len(line)-2][0]

if low < high:
	dst = dst[low:high,:]
else:
	dst = dst[high:low,:]

dst = dst[10:168,179:586]


ver = verticalProjection(dst)
hor = horizontalProjection(dst)

rows,cols = dst.shape

verLine = []
horLine = []
for i in range(1,len(ver)-2):
	if (ver[i-1]<=5 and ver[i] > 5) or (ver[i+1]<=5 and ver[i]> 5):
		#cv2.line(dst,(i,0),(i,rows),(0,0,255),1)
		verLine.append(i)
		#print (i,low),(i,high)

for i in range(1,len(hor)-2):
	if (hor[i-1]<=5 and hor[i] > 5) or (hor[i+1]<=5 and hor[i]> 5):
		#cv2.line(dst,(0,i),(cols,i),(0,0,255),1)
		horLine.append(i)
		#print (i,low),(i,high)

#cv2.imwrite("test.png",dst)
#print len(horLine), len(verLine)

numOfLine = 0

for i in range(0,len(horLine),2):
	numOfLine += 1
	y=0
	for j in range(0,len(verLine),2):
		y+=1
		cv2.imwrite(str(numOfLine)+str(y)+'.png',dst[horLine[i]:horLine[i+1],verLine[j]:verLine[j+1]])


'''
plt.bar(ver.keys(),ver.values())
plt.show()
'''



'''
for i in range(5):
	colCount = 173
	rowCount = 16 + (i*29)
	for j in range(6):
		name1 = str(i+1)+str(j+1)+'-1.png'
		name2 = str(i+1)+str(j+1)+'-2.png'
		cv2.imwrite(name1,binImg[rowCount:rowCount+25,colCount:colCount+21])
		cv2.imwrite(name2,binImg[rowCount:rowCount+25,colCount+21:colCount+42])
		colCount = colCount + 42 + 22
'''
'''
#------------First line------------------
cv2.imwrite('1.png',binImg[16:40,173:194])
cv2.imwrite('5.png',binImg[16:40,194:215])

#cv2.imwrite('.png',binImg[16:40,237:258])
cv2.imwrite('8.png',binImg[16:40,258:279])

cv2.imwrite('2.png',binImg[16:40,301:322])
cv2.imwrite('0.png',binImg[16:40,322:343])

#cv2.imwrite('.png',binImg[16:40,365:386])
cv2.imwrite('6.png',binImg[16:40,386:407])

cv2.imwrite('3.png',binImg[16:40,429:450])
cv2.imwrite('7.png',binImg[16:40,450:471])

#cv2.imwrite('3.png',binImg[16:40,493:514])
cv2.imwrite('4.png',binImg[16:40,514:535])
'''
