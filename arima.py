from basicts import BasicTimeSeriesAnalysis
import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima_model import ARIMA


class ARIMATS(BasicTimeSeriesAnalysis):

	def predict(self,groundtruth):
		vols=self.hist[:]
		#difference to get stationary time series
		vols_diff=list(np.array(vols[1:])-np.array(vols[:-1])) 

		arima_model=ARIMA(vols_diff,order=(1,0,1))
		arima_model_fit=arima_model.fit(disp=0)
		nextVol_diff=arima_model_fit.forecast()[0][0]
		nextVol=nextVol_diff+vols[-1]
		nextVol=max(0,nextVol)
		err=abs(nextVol-groundtruth)
		if groundtruth == 0:
			if nextVol >0:
				err=1
			else:
				err=0
		else:
			err=err/max(nextVol,groundtruth)
		# print('The err is {0}'.format(err))
		return err


	def rollingPredict(self,length):
		vols=self.hist
		vols_diff=list(np.array(vols[1:])-np.array(vols[:-1]))
		predictions=[]
		for k in range(0,length):
			arima_model=ARIMA(vols_diff,order=(1,0,1))
			arima_model_fit=arima_model.fit(disp=0)
			nextVol_diff=arima_model_fit.forecast()[0][0]
			nextVol=nextVol_diff+vols[-1]
			if nextVol<0:
				nextVol=0
			predictions.append(nextVol)
			vols.append(nextVol)
			vols_diff.append(nextVol_diff)
		print(predictions)
		return predictions




from preparedata import generateSeries,generateTranAndTestData
if __name__ == '__main__':
	station='Xixiang'
	days=['20131216','20131217','20131218','20131219','20131220']
	# ts=generateSeries(days,station)
	ts=generateSeries(days,station,flag=1)

	# length=30
	# ts_train=ts[:-60*6]
	# ts_test_groundtruth=ts[-60*6:-60*6+length]
	# arima_test=ARIMATS(ts_train)
	# arima_test.rollingPredict(length)
	# print(ts_test_groundtruth)

	
	for t in range(1,7):
		print(t)
		slotLength=t
		results=[]
		for k in range(0,60):
			end=-60*17
			ts_used=ts[k:end+k]
			history,groundtruth=generateTranAndTestData(ts_used,slotLength)
			arima_test=ARIMATS(history)
			err=arima_test.predict(groundtruth)
			print(err)
			results.append(err)
		e=sum(results)*1./len(results)
		print('The err for slot={1} is {0}'.format(e,slotLength))
		with open('output_exit.txt','a+') as fh:
			fh.write('{0}\r\n'.format(e))