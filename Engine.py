import numpy as np
import warnings
import matplotlib.pyplot as plt
import time
import math
import random
import datetime
from NeuralNetworks import *

class Engine:
	def __init__(self, xfile, yfile):
		self.report = ''
		self.settings()
		self.xfile = xfile
		self.yfile = yfile

	def settings(self):
		warnings.filterwarnings("ignore")
		np.set_printoptions(suppress=True)

	def debug(self, msg):
		print(msg)
		self.report += '{}\n'.format(msg)

	def debug_clear(self):
		self.report = ''

	def run(self):

		training = True

		X = np.load(self.xfile)
		Y = np.load(self.yfile)

		Factor = int(len(Y)/60)
		if Factor == 0: Factor = 1
		NNSize = [2, 2*Factor, 2*Factor, 7*Factor, 1]

		X /= 23

		NN = NeuralNetwork('w.txt', NNSize)
		if NN.weightFileExist():
			training = False

		if training:
			T = Trainer(NN)
			for n in range(12):
				T.train(X, Y)
		else:
			NN.loadWeights()

		self.debug('-'*45)
		self.debug('Neural Network Size: {}'.format(NNSize))
		self.debug('Factor: {}'.format(Factor))
		self.debug('Data: {}'.format(len(Y)))
		self.debug('Final Error: {}'.format(float(NN.costFunction(X, Y))))
		self.debug('Average Error: {}'.format(NN.costFunction(X, Y)/len(Y)))

		Xf = np.zeros(shape=(0,2), dtype=float)

		hour = 0 #datetime.datetime.now().hour
		today = datetime.datetime.now().weekday()
		while hour <= 23:
			Xf = np.append(Xf, [[today, hour]], axis=0)
			hour += 1

		Xf /= 23

		Yf = np.zeros(shape=(0,1), dtype=float)
		for i in range(len(Xf)):
			Yf = np.append(Yf, [NN.forward(Xf[i])], axis=0)

		Xf *= 23
		Yf *= 100

		# TEMP
		fig = plt.figure()                                                               
		ax = fig.add_subplot(1,1,1)                                                      

		# major ticks every 20, minor ticks every 5                                      
		ymajor_ticks = np.arange(0, 101, 20)                                              
		yminor_ticks = np.arange(0, 101, 5)           

		xmajor_ticks = np.arange(0, 24, 4)                                              
		xminor_ticks = np.arange(0, 24, 1)                                        

		ax.set_xticks(xmajor_ticks)                                                       
		ax.set_xticks(xminor_ticks, minor=True)                                           
		ax.set_yticks(ymajor_ticks)                                                       
		ax.set_yticks(yminor_ticks, minor=True)                                           

		# and a corresponding grid                                                       

		ax.grid(which='both')                                                            

		# or if you want differnet settings for the grids:                               
		ax.grid(which='minor', alpha=0.2)                                                
		ax.grid(which='major', alpha=0.5)  

		plt.plot(Xf, Yf)
		plt.axis([0, 23, 0, 100])
		plt.xlabel('{}/{}/{}'.format(datetime.datetime.now().day,
			datetime.datetime.now().month, datetime.datetime.now().year))
		fig = plt.gcf()
		fig.savefig('graph.png', dpi=1000)
		plt.show()

		f = open('report.txt', 'w')
		f.write(self.report)
		f.close()

		print('Complete')
