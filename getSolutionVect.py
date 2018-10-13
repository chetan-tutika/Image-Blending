'''
  File name: getSolutionVect.py
  Author:
  Date created:
'''
from PIL import Image
import matplotlib.pyplot as plt
from scipy import signal
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.mlab import dist_point_to_segment
from matplotlib.path import Path
from mask import maskImage
from getIndexes import getIndexes
from getCoefficientMatrix import getCoefficientMatrix



def getSolutionVect(indexes, source, target, offsetX, offsetY):
	print('index shape',indexes.shape)
	print('target_shape',target.shape)

	filterLaplacian = np.array([[0,-1,0],[-1,4,-1],[0,-1,0]])

	mask_of_1aplace = indexes[offsetY : offsetY + source.shape[0], offsetX : offsetX + source.shape[1]]
	mask_of_1aplace = mask_of_1aplace > 0 
	n = len(mask_of_1aplace[ mask_of_1aplace>0])
	#mask_of_1aplace1 = source * mask_of_1aplace


	#sourceLaplace = signal.convolve2d(mask_of_1aplace1, filterLaplacian,'same')
	sourceLaplace = signal.convolve2d(source, filterLaplacian,'same')


	print('Maskeoflaplace',len(mask_of_1aplace))

	#laplaceMasked = mask_of_1aplace1 * sourceLaplace

	laplaceMasked_1D = sourceLaplace[mask_of_1aplace == True]
	#laplaceMasked_1D = sourceLaplace[mask_of_1aplace > 0]
	#print('laplaceMasked',len(laplaceMasked_1D))
	#print('laplaceMasked',laplaceMasked_final.shape)

	#index_values = indexes[indexes>0]
	indexes_list = np.argwhere(indexes > 0)
	#l = []


	#print('y', y.shape)
	#print('x', x.shape)

	c = np.zeros((len(laplaceMasked_1D), 4))
	for i, j in indexes_list:

		if indexes[i + 1, j] == 0:
			c[indexes[i,j] - 1, 0] = target[i + 1, j]

		if indexes[i - 1, j] == 0:
			c[indexes[i,j] - 1, 1] = target[i - 1, j]

		if indexes[i,j + 1] == 0:
			c[indexes[i,j] - 1, 2] = target[i, j + 1]

		if indexes[i, j - 1] == 0:
			c[indexes[i,j] - 1, 3] = target[i, j - 1]


	SolVectorb = np.sum(c, axis=1) + laplaceMasked_1D
	SolVectorb = SolVectorb.reshape((1, laplaceMasked_1D.shape[0]))

	#SolVectorb = sourceLaplace[sourceLaplace_mask>0]
	print(len(SolVectorb)) 



	return SolVectorb


if __name__ == '__main__':
	mask = maskImage()
	print('mask_shape', mask.shape)
	I_Target = np.array(Image.open('TargetImage.png').convert('RGB'))
	I_Source = np.array(Image.open('SourceImage.png').convert('RGB'))

	targetH,targetW=I_Target.shape[:2]
	print(targetH,targetW)
	offsetX = int(targetW/2)
	offsetY = int(targetH/2)
	#print(offsetY,offsetX)

	indexes = getIndexes(mask, targetH, targetW, offsetX, offsetY)

	coeffA = getCoefficientMatrix(indexes)

	#print(coeffA.shape)
	
	SolVectorb = getSolutionVect(indexes, I_Source[:,:,0], I_Target[:,:,0], offsetX, offsetY)

	#print('len',len(SolVectorb))