'''
  File name: getIndexes.py
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



def getIndexes(mask, targetH, targetW, offsetX, offsetY):
	mask_padded = np.zeros([targetH,targetW])
	
	mask_padded[offsetY : offsetY + int(mask.shape[0]), offsetX : offsetX + int(mask.shape[1])] = mask.astype('int')
	#mask_padded[0:10,0:10] = 255
	mask_ones=mask_padded.copy()
	#print(mask_ones[offsetY+50 : offsetY + mask.shape[0], offsetX+30 : offsetX + mask.shape[1]])

	#print('len1',len(mask_ones[mask_padded>0]))
	#print('len_index',len(list_index))
	mask_ones[mask_padded>0]=[i + 1 for i in range(len(mask_ones[mask_padded>0])) ]
	#print(mask_ones[offsetY+50 : offsetY + mask.shape[0]-20, offsetX+30 : offsetX + mask.shape[1]-20])

	#print(mask_padded[0:10,0:10])
	print(mask.shape)
	indexes = mask_ones.copy().astype(int)


	return indexes







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