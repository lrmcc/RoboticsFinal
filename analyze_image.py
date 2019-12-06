
import cv2


colorList = [(157,232,255),(210,155,254),(112,239,207),(84,221,177)]
threshold = 40


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
	# print("(" + str(pixel[0]) + "," + str(pixel[1]) + "," + str(pixel[2]))
	for i in range(0,len(colorList)):
		diff = abs(colorList[i][0] - pixel[0]) + abs(colorList[i][1] - pixel[1]) + abs(colorList[i][2] - pixel[2])
		if diff < threshold:
			return i+1
		# if pixel[0] > colorList[i][0] - threshold and pixel[0] < colorList[i][0] + threshold and pixel[1] > colorList[i][1] - threshold and pixel[1] < colorList[i][1] + threshold and pixel[2] > colorList[i][2] - threshold and pixel[2] < colorList[i][2] + threshold:
		# 	return i+1
	return 0

# def expand(i,j,pixelList,tmpBlobList,maskValue):
# 	if pixelList[i][j] == maskValue and pixelList[i][j] != 0:
# 		print(maskValue)
# 		tmpBlobList.append((i,j))
# 		pixelList[i][j] = 0
# 		if(i > 0):
# 			expand(i-1,j,pixelList,tmpBlobList,maskValue)
# 		if(i < len(pixelList)-1):
# 			expand(i+1,j,pixelList,tmpBlobList,maskValue)
# 		if(j > 0):
# 			expand(i,j-1,pixelList,tmpBlobList,maskValue)
# 		if(j < len(pixelList[i])-1):
# 			expand(i,j+1,pixelList,tmpBlobList,maskValue)

def expand(i,j,pixelList,tmpBlobList,maskValue):
	if pixelList[i][j] == maskValue and pixelList[i][j] != 0:
		tmpBlobList.append((i,j))
		pixelList[i][j] = 0
		queue = []
		if(i > 0):
			queue.append((i-1,j)) #expand(i-1,j,pixelList,tmpBlobList,maskValue)
		if(i < len(pixelList)-1):
			queue.append((i+1,j)) #expand(i+1,j,pixelList,tmpBlobList,maskValue)
		if(j > 0):
			queue.append((i,j-1)) #expand(i,j-1,pixelList,tmpBlobList,maskValue)
		if(j < len(pixelList[i])-1):
			queue.append((i,j+1)) #expand(i,j+1,pixelList,tmpBlobList,maskValue)
		for p in queue:
			x = p[0]
			y = p[1]
			if pixelList[x][y] == maskValue and pixelList[x][y] != 0:
				tmpBlobList.append((x,y))
				pixelList[x][y] = 0
				if(x > 0):
					queue.append((x-1,y)) #expand(i-1,j,pixelList,tmpBlobList,maskValue)
				if(x < len(pixelList)-1):
					queue.append((x+1,y)) #expand(i+1,j,pixelList,tmpBlobList,maskValue)
				if(y > 0):
					queue.append((x,y-1)) #expand(i,j-1,pixelList,tmpBlobList,maskValue)
				if(y < len(pixelList[x])-1):
					queue.append((x,y+1)) #expand(i,j+1,pixelList,tmpBlobList,maskValue)




def analyzeImage(image):
	imageWidth, imageHeight,channels = image.shape
	# format for list: (x,y)
	pixelList = []
	for i in range(imageWidth):
		pixelList.append([0.0]*imageHeight)

	for i in range(0,imageWidth):
		for j in range(0, imageHeight):
			# print(str(image[i,j]))
			pixelList[i][j] = evaluatePixel(image[i,j])

	bloblist = []
	for i in range(0,imageWidth):
		for j in range(0, imageHeight):
			tmpBlobList = []
			maskValue = pixelList[i][j]
			expand(i,j,pixelList,tmpBlobList,maskValue)
			if len(tmpBlobList) > 10:
				bloblist.append(Blob(tmpBlobList,maskValue))
	return bloblist

def debug(bloblist, image):
	imageWidth, imageHeight,channels = image.shape
	# format for list: (x,y)
	pixelList = []
	for i in range(imageWidth):
		pixelList.append([0.0]*imageHeight)
	for i in range(0,imageWidth):
		for j in range(0, imageHeight):
			for b in bloblist:
				if ((i == b.higherBoundingX and j >= b.lowerBoundingY and j <= b.higherBoundingY) or 
					(i == b.lowerBoundingX and j >= b.lowerBoundingY and j <= b.higherBoundingY) or
					(j == b.higherBoundingY and i >= b.lowerBoundingX and i <= b.higherBoundingX) or 
					(j == b.lowerBoundingY and i >= b.lowerBoundingX and i <= b.higherBoundingX)):
					image[i,j] = (colorList[b.maskValue - 1][0]/2.0,colorList[b.maskValue - 1][1]/2.0,colorList[b.maskValue - 1][2]/2.0)#colorList[b.maskValue - 1]
	cv2.imwrite('output.png',image)

testimage = cv2.imread('images-2.png')
debug(analyzeImage(testimage),testimage)




	