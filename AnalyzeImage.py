
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
			averageX += p[0]
			averageY += p[1]

			if(p[0] < lowerBoundingX or lowerBoundingX == -1):
				lowerBoundingX = p[0]

			if(p[1] < lowerBoundingY or lowerBoundingY == -1):
				lowerBoundingY = p[1]

			if(p[0] > higherBoundingX or higherBoundingX == -1):
				higherBoundingX = p[0]

			if(p[1] > higherBoundingY or higherBoundingY == -1):
				higherBoundingY = p[1]

		averageX /= self.numPixels
		averageY /= self.numPixels


def evaluatePixel(pixel):

def expand(i,j,pixelList,tmpBlobList,maskValue):
	if pixelList[i][j] == maskValue and pixelList[i][j] != 0:
		tmpBlobList.append((i,j))
		pixelList[i][j] = 0
		expand(x-1,y,pixelList,tmpBlobList,maskValue)



def analyzeImage(image):
	imageWidth = 
	imageHeight = 

	# format for list: (x,y)
	pixelMask = [[0.0]*imageHeight]*imageWidth

	for i in range(0,imageWidth):
		for j in range(0, imageHeight):
			pixelMask[i][j] = evaluatePixel(thispixel)

	bloblist = []
	for i in range(0,imageWidth):
		for j in range(0, imageHeight):
			tmpBlobList = []
			maskValue = pixelList[i][j]
			expand(i,j,pixelList,tmpBlobList,maskValue)
			if len(tmpBlobList) > 10:
				bloblist.append(Blob(tmpBlobList,maskValue))





	