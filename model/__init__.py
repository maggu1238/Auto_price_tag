import matplotlib.pyplot as plt
import tensorflow as tf
import pandas as pd
import numpy as np
import datetime
import time
import cv2
import os

from options import Options
import modules as model

np.set_printoptions(threshold=np.nan)

class CNN:

	def __init__(self, alpha):
		"""
		defines the architecture of the model
		"""

		"""
		Initialize variables related to training the model
		"""
		# alpha used for leaky relu
		self.options = Options()
		self.alpha = alpha
		self.threshold = 0.15
		self.iou_threshold = 0.5
		self.classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train","tvmonitor"]
		self.image_file = self.options.image_file

		# Input to the model
		self.x = tf.placeholder(tf.float32, shape=[None, 448, 448, 3])

		# Stack the layers of the network
		print "    Stacking layers of the network"
		self.conv_01 = model.conv2d(1, self.x, kernel=[7,7,3,64], stride=2, name='conv_01', alpha=self.alpha)
		self.pool_02 = model.max_pool(2, self.conv_01, name='pool_02')

		self.conv_03 = model.conv2d(3, self.pool_02, kernel=[3,3,64,192], stride=1, name='conv_03', alpha=self.alpha)
		self.pool_04 = model.max_pool(4, self.conv_03, name='pool_04')

		self.conv_05 = model.conv2d(5, self.pool_04, kernel=[1,1,192,128], stride=1, name='conv_05', alpha=self.alpha)
		self.conv_06 = model.conv2d(6, self.conv_05, kernel=[3,3,128,256], stride=1, name='conv_06', alpha=self.alpha)
		self.conv_07 = model.conv2d(7, self.conv_06, kernel=[1,1,256,256], stride=1, name='conv_07', alpha=self.alpha)
		self.conv_08 = model.conv2d(8, self.conv_07, kernel=[3,3,256,512], stride=1, name='conv_08', alpha=self.alpha)
		self.pool_09 = model.max_pool(9, self.conv_08, name='pool_09')

		self.conv_10 = model.conv2d(10, self.pool_09, kernel=[1,1,512,256], stride=1, name='conv_10', alpha=self.alpha)
		self.conv_11 = model.conv2d(11, self.conv_10, kernel=[3,3,256,512], stride=1, name='conv_11', alpha=self.alpha)
		self.conv_12 = model.conv2d(12, self.conv_11, kernel=[1,1,512,256], stride=1, name='conv_12', alpha=self.alpha)
		self.conv_13 = model.conv2d(13, self.conv_12, kernel=[3,3,256,512], stride=1, name='conv_13', alpha=self.alpha)
		self.conv_14 = model.conv2d(14, self.conv_13, kernel=[1,1,512,256], stride=1, name='conv_14', alpha=self.alpha)
		self.conv_15 = model.conv2d(15, self.conv_14, kernel=[3,3,256,512], stride=1, name='conv_15', alpha=self.alpha)
		self.conv_16 = model.conv2d(16, self.conv_15, kernel=[1,1,512,256], stride=1, name='conv_16', alpha=self.alpha)
		self.conv_17 = model.conv2d(17, self.conv_16, kernel=[3,3,256,512], stride=1, name='conv_17', alpha=self.alpha)
		self.conv_18 = model.conv2d(18, self.conv_17, kernel=[1,1,512,512], stride=1, name='conv_18', alpha=self.alpha)
		self.conv_19 = model.conv2d(19, self.conv_18, kernel=[3,3,512,1024],stride=1, name='conv_19', alpha=self.alpha)
		self.pool_20 = model.max_pool(20, self.conv_19, name='pool_20')

		self.conv_21 = model.conv2d(21, self.pool_20, kernel=[1,1,1024,512],  stride=1, name='conv_21', alpha=self.alpha)
		self.conv_22 = model.conv2d(22, self.conv_21, kernel=[3,3,512,1024],  stride=1, name='conv_22', alpha=self.alpha)
		self.conv_23 = model.conv2d(23, self.conv_22, kernel=[1,1,1024,512],  stride=1, name='conv_23', alpha=self.alpha)
		self.conv_24 = model.conv2d(24, self.conv_23, kernel=[3,3,512,1024],  stride=1, name='conv_24', alpha=self.alpha)
		self.conv_25 = model.conv2d(25, self.conv_24, kernel=[3,3,1024,1024], stride=1, name='conv_25', alpha=self.alpha)
		self.conv_26 = model.conv2d(26, self.conv_25, kernel=[3,3,1024,1024], stride=2, name='conv_26', alpha=self.alpha)
		self.conv_27 = model.conv2d(27, self.conv_26, kernel=[3,3,1024,1024], stride=1, name='conv_27', alpha=self.alpha)
		self.conv_28 = model.conv2d(28, self.conv_27, kernel=[3,3,1024,1024], stride=1, name='conv_28', alpha=self.alpha)

		# Reshape 'self.conv_28' from 4D to 2D
		shape = self.conv_28.get_shape().as_list()
		flat_shape = int(shape[1])*int(shape[2])*int(shape[3])
		inputs_transposed = tf.transpose(self.conv_28, (0,3,1,2))
		fully_flat = tf.reshape(inputs_transposed, [-1, flat_shape])		
		self.fc_29 = model.fully_connected(29, fully_flat, 512, name='fc_29', alpha=self.alpha, activation=tf.nn.relu)
		self.fc_30 = model.fully_connected(30, self.fc_29, 4096, name='fc_30', alpha=self.alpha, activation=tf.nn.relu)
		# skip the dropout layer
		self.fc_31 = model.fully_connected(31, self.fc_30, 1470, name='fc_31', alpha=self.alpha, activation=None)
 		
 		self.init_operation = tf.initialize_all_variables()
 		self.saver = tf.train.Saver()

	def model_variables(self):
		architecture = ''
		for variable in tf.trainable_variables():
			architecture += str(variable.name) 
			architecture += '\n'
		return architecture

	def count_params(self):
		total_parameters = 0
		for variable in tf.trainable_variables():
			count = 1
			for dimension in variable.get_shape().as_list():
				count *= dimension
			total_parameters += count

		return total_parameters


	def train(self):
		"""
		train the model
		"""
		pass

	def validate(self):
		"""
		validate the model
		"""
		pass


	def test(self, test_image):
		"""
		test the model
		"""
		with tf.Session() as sess:
			print 'Initializing the variables'
			sess.run(self.init_operation)
			checkpoint = self.options.checkpoint_dir+'YOLO_small.ckpt'																						
			print 'Restoring the saved model_architecture'
			self.saver.restore(sess, checkpoint)
			print 'Restored the model successfully from "{}"!!'.format(checkpoint)

			img = cv2.imread(test_image)
			s = time.time()
			
			# print 'Infering shape of the image'
			self.h_img,self.w_img,_ = img.shape
			# print 'Height : {}\tWidth : {}'.format(self.h_img, self.w_img)

			# print '\nReshaping the image'
			img_resized = cv2.resize(img, (448, 448))
			img_RGB = cv2.cvtColor(img_resized,cv2.COLOR_BGR2RGB)
			img_resized_np = np.asarray( img_RGB )
			inputs = np.zeros((1,448,448,3),dtype='float32')
			inputs[0] = (img_resized_np/255.0)*2.0-1.0

			print '\nDoing the forward pass over the network'
			net_output = sess.run(self.fc_31, feed_dict={self.x : inputs})
			self.result = self.interpret_output(net_output[0])
			self.show_results(img, self.result)

	def interpret_output(self, output):
		
		# these are the final class specific probability scores for each of the box - 
		probs = np.zeros((7,7,2,20))

		# [980] class specific probability for each grid cell
		class_probs = np.reshape(output[0:980],(7,7,20))
		
		# [98] 
		scales = np.reshape(output[980:1078],(7,7,2))
		
		# [392] 
		boxes = np.reshape(output[1078:],(7,7,2,4))
		
		# 
		offset = np.transpose(np.reshape(np.array([np.arange(7)]*14),(2,7,7)),(1,2,0))

		# 
		boxes[:,:,:,0] += offset												# x-center of the box
		boxes[:,:,:,1] += np.transpose(offset,(1,0,2))					# y-center of the box
		boxes[:,:,:,0:2] = boxes[:,:,:,0:2] / 7.0                   #
		boxes[:,:,:,2] = np.multiply(boxes[:,:,:,2],boxes[:,:,:,2]) # height of the box
		boxes[:,:,:,3] = np.multiply(boxes[:,:,:,3],boxes[:,:,:,3]) #  width of the box
		
		boxes[:,:,:,0] *= self.w_img
		boxes[:,:,:,1] *= self.h_img
		boxes[:,:,:,2] *= self.w_img
		boxes[:,:,:,3] *= self.h_img

		# Generate the class specific probability scores for each of the bounding box in each of the grid cell
		for i in range(2):
			for j in range(20):
				probs[:,:,i,j] = np.multiply(class_probs[:,:,j],scales[:,:,i])

		# Threshold the probability values for each bounding box
		filter_mat_probs = np.array(probs>=self.threshold,dtype='bool')
		filter_mat_boxes = np.nonzero(filter_mat_probs) # 4D tensor

		boxes_filtered = boxes[filter_mat_boxes[0],filter_mat_boxes[1],filter_mat_boxes[2]]
		probs_filtered = probs[filter_mat_probs]
		classes_num_filtered = np.argmax(filter_mat_probs,axis=3)[filter_mat_boxes[0],filter_mat_boxes[1],filter_mat_boxes[2]] 

		# print boxes_filtered 		# (x,y,w,h) for each of the fitered box
		# print probs_filtered 		# probability for each of the predicted class
		# print classes_num_filtered # class index of the predicted probability


		argsort = np.array(np.argsort(probs_filtered))[::-1]
		boxes_filtered = boxes_filtered[argsort]
		probs_filtered = probs_filtered[argsort]
		classes_num_filtered = classes_num_filtered[argsort]

		# print 'After sorting'
		# print boxes_filtered 		# (x,y,w,h) for each of the fitered box
		# print probs_filtered 		# probability for each of the predicted class

		# Loop over each of the predicted bounding box
		for i in range(len(boxes_filtered)):
			if probs_filtered[i] == 0 : 
				continue
			for j in range(i+1,len(boxes_filtered)):
				if self.iou(boxes_filtered[i],boxes_filtered[j]) > self.iou_threshold : 
					probs_filtered[j] = 0.0
		
		filter_iou = np.array(probs_filtered>0.0,dtype='bool')
		boxes_filtered = boxes_filtered[filter_iou]
		probs_filtered = probs_filtered[filter_iou]
		classes_num_filtered = classes_num_filtered[filter_iou]

		result = []
		for i in range(len(boxes_filtered)):
			result.append([self.classes[classes_num_filtered[i]],boxes_filtered[i][0],boxes_filtered[i][1],boxes_filtered[i][2],boxes_filtered[i][3],probs_filtered[i]])

		# Each of the result : ['person', 248.64821, 279.18292, 352.34753, 488.08188, 0.61149513721466064]
		return result

	def show_results(self, img, results):
		img_cp = img.copy()
		
		for i in range(len(results)):
			x = int(results[i][1])
			y = int(results[i][2])
			w = int(results[i][3])//2
			h = int(results[i][4])//2
			
			print '    class : ' + results[i][0] + ' , [x,y,w,h]=[' + str(x) + ',' + str(y) + ',' + str(int(results[i][3])) + ',' + str(int(results[i][4]))+'], Confidence = ' + str(results[i][5])
			cv2.rectangle(img_cp, (x-w,y-h), (x+w,y+h), (0,255,0), 2)
			cv2.rectangle(img_cp, (x-w,y-h-20), (x+w,y-h), (125,125,125), -1)
			cv2.putText(img_cp, results[i][0] + ' : %.2f' % results[i][5], (x-w+5,y-h-7), cv2.FONT_ITALIC, 0.5, (0,0,0), 1)
			
		cv2.imwrite(self.image_file, img_cp)			
		cv2.imshow('YOLO detection', img_cp)
		cv2.waitKey(0)


	def iou(self, box1, box2):
		tb = min(box1[0]+0.5*box1[2],box2[0]+0.5*box2[2])-max(box1[0]-0.5*box1[2],box2[0]-0.5*box2[2])
		lr = min(box1[1]+0.5*box1[3],box2[1]+0.5*box2[3])-max(box1[1]-0.5*box1[3],box2[1]-0.5*box2[3])
		if tb < 0 or lr < 0 : 
			intersection = 0
		else : 
			intersection =  tb*lr

		return intersection / (box1[2]*box1[3] + box2[2]*box2[3] - intersection)

		