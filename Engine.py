import numpy as np
import warnings
import matplotlib.pyplot as plt
import datetime
from NeuralNetworks import NeuralNetwork
from NeuralNetworks import Trainer

class Engine:
	def __init__(self, xfile, yfile):
		self.report = ''
		self.settings()
		self.xfile = xfile
		self.yfile = yfile

	def degrees(self, size):
		for f in range(50):
			n = [2, 2*f, 2*f, 7*f, 1]
			result = 0
			for i in range(len(n)-1):
				result += n[i]*n[i+1]
			if result > size:
				if f == 1: return 1
				else: return f-1

	def degreesValue(self, v):
		n = [2, 2*v, 2*v, 7*v, 1]
		result = 0
		for i in range(len(n)-1):
			result += n[i]*n[i+1]
		return result

	def settings(self):
		warnings.filterwarnings("ignore")
		np.set_printoptions(suppress=True)

	def debug(self, msg):
		self.report += '{}\n'.format(msg)

	def debug_clear(self):
		self.report = ''

	def run(self):
		training = True

		X = np.load(self.xfile)
		Y = np.load(self.yfile)

		# The right amout of factor
		Factor = self.degrees(len(Y))
		NNSize = [2, 2*Factor, 2*Factor, 7*Factor, 1]

		XMAX = np.amax(X, axis=0)
		X /= XMAX

		NN = NeuralNetwork('weights.txt', NNSize)

		if training:
			print('Starting training with {} amount of data.'.format(len(Y)))
			T = Trainer(NN)
			for n in range(12):
				T.train(X, Y)
			print('Complete.')
		else:
			NN.loadWeights()

		self.debug('Neural Network Size: {}'.format(NNSize))
		self.debug('Factor: {} ({})'.format(Factor, self.degreesValue(Factor)))
		self.debug('Data: {}'.format(len(Y)))
		self.debug('Final Error: {}'.format(float(NN.costFunction(X, Y))))
		self.debug('Average Error: {}'.format(NN.costFunction(X, Y)/len(Y)))

		Xf = np.zeros(shape=(0,2), dtype=float)

		today = datetime.datetime.now().weekday()
		for hour in range(24):
			Xf = np.append(Xf, [[today, hour]], axis=0)

		Xf /= XMAX

		Yf = np.zeros(shape=(0,1), dtype=float)
		for i in range(len(Xf)):
			Yf = np.append(Yf, [NN.forward(Xf[i])], axis=0)

		Xf *= XMAX
		Yf *= 100

		fig = plt.figure()                                                               
		ax = fig.add_subplot(1,1,1)                                                      

		ymajor_ticks = np.arange(0, 101, 10)                                              
		yminor_ticks = np.arange(0, 101, 1)           

		xmajor_ticks = np.arange(0, 24, 2)                                              
		xminor_ticks = np.arange(0, 24, 1)                                        

		ax.set_xticks(xmajor_ticks)                                                       
		ax.set_xticks(xminor_ticks, minor=True)                                           
		ax.set_yticks(ymajor_ticks)                                                       
		ax.set_yticks(yminor_ticks, minor=True)                                                                                              

		ax.grid(which='both')                                                            
                            
		ax.grid(which='minor', alpha=0.2)                                                
		ax.grid(which='major', alpha=0.5)  

		plt.plot(Yf)
		plt.axis([0, 23, 0, 100])
		plt.xlabel('{}/{}/{}'.format(datetime.datetime.now().day,
			datetime.datetime.now().month, datetime.datetime.now().year))
		fig = plt.gcf()
		fig.savefig('graph.png', dpi=1000)
		plt.show()

		f = open('report.txt', 'w')
		f.write(self.report)
		f.close()

		print('Program finished.')
