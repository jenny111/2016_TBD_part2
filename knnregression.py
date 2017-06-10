from supervisedmodels import SupervisedModel
from sklearn.neighbors import KNeighborsRegressor

class KNNRegression(SupervisedModel):
	def train(self,trainSamples,labels):
		self.model=KNeighborsRegressor(n_neighbors=5)
		self.model.fit(trainSamples,labels)

	def predict(self,testSamples):
		predictions=self.model.predict(testSamples)
		predictions=[max(0,value) for value in predictions]
		return predictions


from preparedata import generateSeries,generateTrainAndTestSamples
if __name__ == '__main__':
	station='Xixiang'
	days=['20131216','20131217','20131218','20131219','20131220']
	# ts=generateSeries(days,station)
	ts=generateSeries(days,station,flag=1)

	for slotLength in range(1,7): #varing the length of slot
		end=-60*17
		ts_used=ts[:end]
		trainSamples,trainlabels,testSamples,testlabels=generateTrainAndTestSamples(ts_used,slotLength)
		knn=KNNRegression()
		e=knn.run(trainSamples,trainlabels,testSamples,testlabels)

		print('The error for slot={1} is {0}'.format(e,slotLength))
		with open('output_knn_exit.txt','a+') as fh:
			fh.write('{0}\r\n'.format(e))