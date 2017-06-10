class BasicTimeSeriesAnalysis(object):
	'''
	Basic time series analysis class.
	'''
	def __init__(self,hist=None):
		self.hist=hist
		self.prediction=None
		self.model=None

	def train(self):
		pass

	def predict(self):
		pass

	def evaluate(self, predictions, labels):
		pass