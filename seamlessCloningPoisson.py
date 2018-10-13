'''
  File name: seamlessCloningPoisson.py
  Author:
  Date created:
'''


import numpy as np
from getIndexes import getIndexes
from getCoefficientMatrix import getCoefficientMatrix
from reconstructImg import reconstructImg
from scipy.signal import convolve2d
from getSolutionVect import getSolutionVect
import matplotlib.pyplot as plt
from mask import maskImage
from numpy.linalg import inv


from PIL import Image


def seamlessCloningPoisson(sourceImg, targetImg, mask, offsetX, offsetY):

	targetH, targetW = targetImg.shape[:2]
	indexes = getIndexes(mask, targetH, targetW, offsetX, offsetY)

	coeffA = getCoefficientMatrix(indexes)

	print(coeffA.shape)
	
	SolVectorb_r = getSolutionVect(indexes, I_Source[:,:,0], I_Target[:,:,0], offsetX, offsetY)
	print("hi " , SolVectorb_r.shape)
	SolVectorb_g = getSolutionVect(indexes, I_Source[:,:,1], I_Target[:,:,1], offsetX, offsetY)
	SolVectorb_b = getSolutionVect(indexes, I_Source[:,:,2], I_Target[:,:,2], offsetX, offsetY)

	inv_coeffA = inv(coeffA)
	f_r = np.dot(SolVectorb_r, inv_coeffA)
	f_g = np.dot(SolVectorb_g, inv_coeffA)
	f_b = np.dot(SolVectorb_b, inv_coeffA)

	plt.figure(num = 'source')
	plt.imshow(I_Source)


	resultImg = reconstructImg(indexes, f_r, f_g, f_b, I_Target)

	#plt.imshow(resultImg)
	#plt.show()

	return resultImg


if __name__ == "__main__":

	import time
	start_time = time.time()
	I_Target = np.array(Image.open('TargetImage.png').convert('RGB'))
	I_Source = np.array(Image.open('SourceImage.png').convert('RGB'))

	#I_Target = np.array(Image.open('targetBush.jpeg').convert('RGB'))
	#I_Source = np.array(Image.open('sourceClooney2.jpeg').convert('RGB'))
	I_Source1 = I_Source.copy() 

	mask = maskImage(I_Source1)
	#mask = np.array(Image.open('Masked_SourceImage.png').convert('RGB'))
	#mask = mask[mask!=0][:0]

	targetH,targetW,depth=I_Target.shape
	print(targetH,targetW)
	offsetX = int(targetW / 2)
	offsetY = int(targetH / 2)
	print('00',offsetY, offsetX)

	finalImage = seamlessCloningPoisson(I_Source, I_Target, mask, offsetX, offsetY)

	end_time = time.time()
	result = Image.fromarray((finalImage).astype(np.uint8))
	result.save('blended_Image.bmp')

	plt.imshow(finalImage)
	plt.show()