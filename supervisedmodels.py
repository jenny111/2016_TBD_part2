class SupervisedModel(object):
	'''
	Basic class for supervised models.
	'''


	def __init__(self):
		self.model=None
		pass


	def train(self,trainSamples,trainLabels):
		pass


	def predict(self,testSamples):
		pass


	def evaluate(self,predictions,testLabels):
		if len(predictions)!=len(testLabels):
			print('The numbers of predictions and groundtruth doesn\'t match.')
			return None
		e=[]
		for k in range(0,len(predictions)):
			error=abs(predictions[k]-testLabels[k])
			if testLabels[k]==0:
				if predictions[k]!=0:
					error=1
				else:
					error=0
			else:
				e.append(error*1./max(predictions[k],testLabels[k]))
		e=1.*sum(e)/len(e)
		return e


	def run(self,trainSamples,trainLabels,testSamples,testLabels):
		self.train(trainSamples,trainLabels)
		predictions=self.predict(testSamples)
		predictionError=self.evaluate(predictions,testLabels)
		return predictionError