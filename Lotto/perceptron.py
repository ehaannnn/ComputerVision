import numpy as np
import cv2
from lotto import numOfLine

#[0,1,2,3,4,5,6,7,8,9]
number = np.array([[-1,-1,-1,-1],
		[-1,-1,-1,1],
		[-1,-1,1,-1],
		[-1,-1,1,1],
		[-1,1,-1,-1],
		[-1,1,-1,1],
		[-1,1,1,-1],
		[-1,1,1,1],
		[1,-1,-1,-1],
		[1,-1,-1,1]],dtype=int)
eta = np.random.random()

numData = {0:['./number/0-1.png','./number/0-2.png','./number/0-3.png','./number/0-4.png',
			'./number/0-5.png'],
			1:['./number/1-1.png','./number/1-2.png','./number/1-3.png','./number/1-4.png'
			,'./number/1-5.png'],
			2:['./number/2-1.png','./number/2-2.png','./number/2-3.png','./number/2-4.png'
			,'./number/2-5.png'],
			3:['./number/3-1.png','./number/3-2.png','./number/3-3.png','./number/3-4.png'
			,'./number/3-5.png'],
			4:['./number/4-1.png','./number/4-2.png','./number/4-3.png','./number/4-4.png'
			,'./number/4-5.png'],
			5:['./number/5-1.png','./number/5-2.png','./number/5-3.png'],
			6:['./number/6-1.png','./number/6-2.png','./number/6-3.png','./number/6-4.png'],
			7:['./number/7-1.png','./number/7-2.png'],
			8:['./number/8-1.png','./number/8-2.png','./number/8-3.png','./number/8-4.png',
			'./number/8-5.png']}

W = np.random.rand(4,20*25)*10-3

class NN:
	def __init__(self,num):
		self.eta = eta
		self.D = number[num]
		self.isCorrect = [False,False,False,False]
		self.num = num
		img = [cv2.imread(numData[num][i],0) for i in range(len(numData[num]))]
		img = [cv2.resize(img[i],(20,25)) for i in range(len(img))]
		self.X = []
		for index in range(len(img)):
			rows, cols = img[index].shape
			self.X.append(np.empty([rows,cols]))
			for i in range(rows):
				for j in range(cols):
					if img[index][i,j]==255:
						self.X[index][i,j]=0
					else:
						self.X[index][i,j]=1

			self.X[index] = self.X[index].reshape((1,rows*cols))

	def changeWeight(self,index,itx):
		W[index] = W[index]+self.eta*(self.D[index]-self.Y[0,index])*self.X[itx]

	def numXLearning(self):
		for itx in range(len(self.X)):
			self.Y = np.dot(self.X[itx],W.T)
			for i in range(4):
				if self.Y[0,i] >= 0:
					self.Y[0,i] = 1
				else:
					self.Y[0,i] = -1

			for i in range(4):
				if self.Y[0,i]!=self.D[i]:
					self.changeWeight(i,itx)
				else:
					self.isCorrect[i] = True

numOf = [NN(i) for i in range(9) ]
print "learning..."
for iteration in range(10000):
	for index in range(9):
		numOf[index].numXLearning()

'''learning is over'''

'''test start'''
print "learning is over!"
print "Recognizing lotto number..."

for i in range(1,numOfLine+1):
	testImg = [[cv2.imread(str(i)+str(j)+'.png',0) for j in range(1,13,2)],
			[cv2.imread(str(i)+str(j)+'.png',0) for j in range(2,13,2)]]
	for it in range(6):
		string = ""
		for lottoNumIndex in range(2):
			maxNum = 0
			testImg[lottoNumIndex][it] = cv2.resize(testImg[lottoNumIndex][it],(20,25))
			rows, cols = testImg[lottoNumIndex][it].shape
			X = np.empty([rows,cols])
			for i in range(rows):
				for j in range(cols):
					if testImg[lottoNumIndex][it][i,j]==255:
						X[i,j]=0
					else:
						X[i,j]=1
			X = X.reshape((1,rows*cols))
			result = -1
			Y = np.dot(X,W.T)
			#print Y
			for i in range(4):
				if Y[0,i]>=0:
					Y[0,i] = 1
				else:
					Y[0,i] = -1

			isBreak = False
			for num in range(9):
				count = 0
				for i in range(4):
					if number[num][i] == Y[0,i]:
						count = count+1
					if maxNum <= count:
						result = num
						maxNum = count
				if isBreak==True:
					break
				
			string = string + str(result)
		print string, 
	print '\n'

print "Recognizing is over"