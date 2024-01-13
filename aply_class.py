import numpy as np
from scipy import signal
from collections import deque
import joblib

#importanto modelo já treinado.
clf = joblib.load('modelo_treinado.pkl')

#função para efetuar a soma das frequencias de interesse
def som_win(data):
		fz = 512
		faixa = []
		faixa_x = []
		n = 0
		f, p = signal.welch(data, fz, nperseg=fz*0.4, noverlap=fz/30)
		for j in f:
			if 6.0 <= j <= 16.0:
				faixa.append(n)
				faixa_x.append(j)
			n = n + 1
		soma_welch = []
		f, p = signal.welch(data, fz, nperseg=fz*0.4, noverlap=fz/30)
		faixa_p = []
		for n in faixa:
			faixa_p.append(p[n])
		return np.sum(faixa_p)

class MyOVBox(OVBox):

	def __init__(self):
		OVBox.__init__(self)
		self.signalHeader = None
		self.signalInputBCI = deque([], 16)
		self.signalChannelsOverlap = deque([], 16)
		self.currentStart = 0
		self.currentEnd = 0
		self.countOverlap = 1

	#Processando os dados recebidos
	def process(self):
		for chunkIdx in range( len(self.input[0]) ):
			if(type(self.input[0][chunkIdx]) == OVSignalHeader):
				self.signalHeader = self.input[0].pop()
				outputHeader = OVSignalHeader(self.signalHeader.startTime, self.signalHeader.endTime, [1, self.signalHeader.dimensionSizes[1]], ['Mean']+self.signalHeader.dimensionSizes[1]*[''], self.signalHeader.samplingRate)
				self.output[0].append(outputHeader)

			elif(type(self.input[0][chunkIdx]) == OVSignalBuffer):
				chunk = self.input[0].pop()
				self.currentStart = chunk.startTime
				self.currentEnd = chunk.endTime
				numpyBuffer = np.array(chunk).reshape(tuple(self.signalHeader.dimensionSizes))
				numpyBufferMean = numpyBuffer.mean(axis=0)
				#Efetuando sobreposição dos dados
				self.signalChannelsOverlap.append(numpyBuffer)
				self.countOverlap += 1
				if self.countOverlap > 16:
					self.signalInputBCI.extend(self.signalChannelsOverlap)
					if len(self.signalInputBCI) == 16:
						signalArray = np.array(self.signalInputBCI)
						signalArray = signalArray.reshape(signalArray.shape[1], -1)
						#efetuando processaimento dos dados
						lista = signalArray.tolist()
						lista = sum(lista, [])
						valor = som_win(lista).reshape(-1, 1)
						#aplicando o classificador
						resultado = clf.predict(valor)
						print(int(resultado[0]))
					self.countOverlap = 1

			elif(type(self.input[0][chunkIdx]) == OVSignalEnd):
				self.output[0].append(self.input[0].pop())
box = MyOVBox()
