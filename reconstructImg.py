'''
  File name: reconstructImg.py
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
from getSolutionVect import getSolutionVect
from numpy.linalg import inv


def reconstructImg(indexes, red, green, blue, targetImg):

	
	indexes1 = indexes.copy()
	TargetImage_Final = targetImg.copy()
	TargetImage_Final[:,:,0][indexes1 > 0] = np.clip(red.flatten(), 0, 255).astype('uint8')

	TargetImage_Final[:,:,1][indexes1 > 0] = np.clip(green.flatten(), 0, 255).astype('uint8')

	TargetImage_Final[:,:,2][indexes1 > 0] = np.clip(blue.flatten(), 0, 255).astype('uint8')

	return TargetImage_Final








if __name__ == '__main__':
	
	#print('mask_shape', mask.shape)
	I_Target = np.array(Image.open('TargetImage.png').convert('RGB'))
	I_Source = np.array(Image.open('SourceImage.png').convert('RGB'))

	#I_Target = np.array(Image.open('targetBush.jpeg').convert('RGB'))
	#I_Source = np.array(Image.open('sourceClooney2.jpeg').convert('RGB'))

	mask = maskImage(I_Source.copy())
	#mask = np.array(Image.open('Masked_SourceImage.png').convert('RGB'))
	#mask = np.load('mask_array.npy')

	targetH,targetW=I_Target.shape[:2]
	print(targetH,targetW)
	offsetX = int(targetW / 2)
	offsetY = int(targetH / 2)

	#offsetX = int(1)
	#offsetY = int(1)

	#print(offsetY,offsetX)

	indexes = getIndexes(mask, targetH, targetW, offsetX, offsetY)

	coeffA = getCoefficientMatrix(indexes)

	print(coeffA.shape)
	
	SolVectorb_r = getSolutionVect(indexes, I_Source[:,:,0], I_Target[:,:,0], offsetX, offsetY)
	print(SolVectorb_r.shape)
	SolVectorb_g = getSolutionVect(indexes, I_Source[:,:,1], I_Target[:,:,1], offsetX, offsetY)
	SolVectorb_b = getSolutionVect(indexes, I_Source[:,:,2], I_Target[:,:,2], offsetX, offsetY)

	inv_coeffA = inv(coeffA)
	f_r = np.dot(SolVectorb_r, inv_coeffA)
	f_g = np.dot(SolVectorb_g, inv_coeffA)
	f_b = np.dot(SolVectorb_b, inv_coeffA)

	plt.figure(num = 'source')
	plt.imshow(I_Source)


	resultImg = reconstructImg(indexes, f_r, f_g, f_b, I_Target)

	plt.imshow(resultImg)
	plt.show()


	#print('len',len(SolVectorb))