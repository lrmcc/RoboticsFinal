
import cv2
import math
import numpy

# colors should be in BGR, not RGB
colorList = [(133,55,215),(188,214,221),(66,201,133)]
threshold = 50


blobDetectionResolution = (300,300)

class Blob :
	averageX = 0
	averageY = 0
	numPixels = 0
	lowerBoundingX = -1
	lowerBoundingY = -1
	higherBoundingX = -1
	higherBoundingY = -1
	maskValue = 0

	def __init__(self, tmpBlobList, maskValue):
		self.numPixels = len(tmpBlobList)
		self.maskValue = maskValue

		for p in tmpBlobList:
			self.averageX += p[0]
			self.averageY += p[1]

			if(p[0] < self.lowerBoundingX or self.lowerBoundingX == -1):
				self.lowerBoundingX = p[0]

			if(p[1] < self.lowerBoundingY or self.lowerBoundingY == -1):
				self.lowerBoundingY = p[1]

			if(p[0] > self.higherBoundingX or self.higherBoundingX == -1):
				self.higherBoundingX = p[0]

			if(p[1] > self.higherBoundingY or self.higherBoundingY == -1):
				self.higherBoundingY = p[1]

		self.averageX /= self.numPixels
		self.averageY /= self.numPixels

	def __repr__(self):
		return "Blob: Mask:" + str(self.maskValue) + " Average: (" + str(self.averageX) + "," + str(self.averageY) + ") Bounds: (" + str(self.lowerBoundingX) + "," + str(self.lowerBoundingY) + ") (" + str(self.higherBoundingX) + "," + str(self.higherBoundingY) + ")"  


def evaluatePixel(pixel):
	for i in range(0,len(colorList)):
		if pixel[0] > colorList[i][0] - threshold and pixel[0] < colorList[i][0] + threshold and pixel[1] > colorList[i][1] - threshold and pixel[1] < colorList[i][1] + threshold and pixel[2] > colorList[i][2] - threshold and pixel[2] < colorList[i][2] + threshold:
			return i+1
	return 0



def expand(i,j,pixelList,tmpBlobList,maskValue):
	if pixelList[i][j] == maskValue and pixelList[i][j] != 0:
		tmpBlobList.append((i,j))
		pixelList[i][j] = 0
		queue = []
		if(i > 0):
			queue.append((i-1,j))
		if(i < len(pixelList)-1):
			queue.append((i+1,j)) 
		if(j > 0):
			queue.append((i,j-1))
		if(j < len(pixelList[i])-1):
			queue.append((i,j+1))
		for p in queue:
			x = p[0]
			y = p[1]
			if pixelList[x][y] == maskValue and pixelList[x][y] != 0:
				tmpBlobList.append((x,y))
				pixelList[x][y] = 0
				if(x > 0):
					queue.append((x-1,y)) 
				if(x < len(pixelList)-1):
					queue.append((x+1,y))
				if(y > 0):
					queue.append((x,y-1))
				if(y < len(pixelList[x])-1):
					queue.append((x,y+1))



def analyzeImage(image):
	imageWidth, imageHeight,channels = image.shape
	# format for list: (x,y)
	pixelList = []
	for i in range(blobDetectionResolution[0]):
		pixelList.append([0.0]*blobDetectionResolution[1])

	for i in range(0,blobDetectionResolution[0]):
		row = image[int(float(i) / blobDetectionResolution[0] * imageWidth)]
		for j in range(0, blobDetectionResolution[1]):
			pixelList[i][j] = evaluatePixel(row[int(float(j) / blobDetectionResolution[1] * imageHeight)])

	bloblist = []
	for i in range(0,blobDetectionResolution[0]):
		for j in range(0, blobDetectionResolution[1]):
			tmpBlobList = []
			maskValue = pixelList[i][j]
			expand(i,j,pixelList,tmpBlobList,maskValue)
			if len(tmpBlobList) > 10:
				bloblist.append(Blob(tmpBlobList,maskValue))
	return bloblist

def debug(bloblist,image):
	imageWidth, imageHeight,channels = image.shape
	img = numpy.zeros((blobDetectionResolution[0],blobDetectionResolution[1],3),numpy.uint8)#*255
	for i in range(0,blobDetectionResolution[0]):
		for j in range(0, blobDetectionResolution[1]):
			img[i,j] = image[int(float(i) / blobDetectionResolution[0] * imageWidth)][int(float(j) / blobDetectionResolution[1] * imageHeight)]
			for b in bloblist:
				if ((i == b.higherBoundingX and j >= b.lowerBoundingY and j <= b.higherBoundingY) or 
					(i == b.lowerBoundingX and j >= b.lowerBoundingY and j <= b.higherBoundingY) or
					(j == b.higherBoundingY and i >= b.lowerBoundingX and i <= b.higherBoundingX) or 
					(j == b.lowerBoundingY and i >= b.lowerBoundingX and i <= b.higherBoundingX)):
					img[i,j] = (255,255,255)#(colorList[b.maskValue - 1][0]*2.0,colorList[b.maskValue - 1][1]*2.0,colorList[b.maskValue - 1][2]*2.0)#colorList[b.maskValue - 1]
					
	cv2.imwrite('out.png',img)


# testimage = cv2.imread('notes.JPG')
# debug(analyzeImage(testimage),testimage)




	