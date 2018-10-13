'''
  File name: getCoefficientMatrix.py
  Author:
  Date created:
'''
from PIL import Image
import matplotlib.pyplot as plt
import scipy
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.mlab import dist_point_to_segment
from matplotlib.path import Path
from mask import maskImage
from getIndexes import getIndexes


def getCoefficientMatrix(indexes):

	coeffA = np.zeros((np.max(indexes),np.max(indexes)),dtype ='int')

	index_coord = np.argwhere(indexes > 0)


	for i,j in index_coord:
		k = indexes[i,j]
		coeffA[k-1, k-1] = 4

		if indexes[i+1, j] != 0:
			coeffA[k-1, indexes[i+1,j]-1] = -1

		if indexes[i-1, j] != 0:
			coeffA[k-1, indexes[i-1,j]-1] = -1

		if indexes[i,j+1] != 0:
			coeffA[k-1, indexes[i,j+1]-1] = -1


		if indexes[i,j-1] != 0:
			coeffA[k-1, indexes[i,j-1]-1] = -1


	#print(np.argwhere(coeffA==-1))
	return coeffA





if __name__ == '__main__':
	mask = maskImage()
	print(mask.shape)
	I_Target = np.array(Image.open('TargetImage.png').convert('RGB'))
	#mask = np.array(Image.open('cropped_image.bmp').convert('RGB'))

	targetH,targetW=I_Target.shape[:2]
	print(targetH,targetW)
	offsetX = int(targetW/2)
	offsetY = int(targetH/2)
	print(offsetY,offsetX)

	indexes = getIndexes(mask, targetH, targetW, offsetX, offsetY)

	coeffA = getCoefficientMatrix(indexes)
	print('coeffA', coeffA.shape)

	#print(coeffA)