import MySQLdb
import numpy as np
import math

# Connect to mysql database on the server of 202.120.37.78:4420. 
# The port of database service of the server is 3300
db_ip = '202.120.37.78'
db_port=3300
db_user = 'admin'
db_pwd = '2016_NRL_admin123'
db_database = 'shenzhen_metro'


def executeSQL(sql_str):
	'''
	Execute a sql expression and return data.
	'''
	db = MySQLdb.connect(host=db_ip, port=db_port, user=db_user, passwd=db_pwd,
		db=db_database)
	cursor = db.cursor()
	try:
		cursor.execute(sql_str)
		result = cursor.fetchall()
	except:
		print('Error: unable to fecth data. FUNCTION:executeSQL')
		print('SQL expression: {0}'.format(sql_str))
	db.close()
	return result


def getTrafficPerMinute(day, station, flag=0):
	"""
	Get entering/exiting traffic volume of of each minute for the given station 
	for a day.
	@param input:
	day: string, 'YYYYMMDD'. e.g., '20131212'
	station: string, e.g., 'Xixiang'
	flag: int, 0 or 1. 0->entering traffic, 1->exiting traffic.
	"""
	db_table='Commute_{0}'.format(day[-4:]) #table in the database
	if flag==0: # entering traffic
		sqlStr='select TIMESTAMPDIFF(MINUTE,\'{0}\',time1) as enter_minute, \
		count(*) as volume 	from {2} a,Station b \
		where a.station1=b.station_name_cn and station_name_en=\'{1}\' \
		GROUP BY enter_minute;'.format(day,station,db_table)
	else:
		sqlStr='select TIMESTAMPDIFF(MINUTE,\'{0}\',time2) as exit_minute, \
		count(*) as volume from {2} a,Station b \
		where a.station2=b.station_name_cn and station_name_en=\'{1}\' \
		GROUP BY exit_minute;'.format(day,station,db_table)
	results = executeSQL(sqlStr)

	vols=np.zeros(60*24)
	for e in results:
		vols[e[0]]=e[1]
	return list(vols)


def generateSeries(days,station,flag=0):
	'''
	Generate time series data.
	@param input:
	days: list of string, 'YYYYMMDD'. e.g., ['20131212', '20131213']
	station: string, e.g., 'Xixiang'
	flag: int, 0 or 1. 0->entering traffic, 1->exiting traffic.
	'''
	ts=[]
	for d in days:
		vols=getTrafficPerMinute(d,station,flag)
	return ts


def generateTranAndTestData(vols,slotLength=1):
	'''
	Generate data for the ARIMA model.
	@param input
	vols: list. A list of traffic volumes for each minute.
	slotLength: int. The number of minutes in each slot. 
	@param output
	train: list. A list of traffic volumes in each slot.
	test: float. The traffic volume of next slot.
	'''
	train=vols[:-slotLength]
	test=vols[-slotLength:]
	if slotLength>1:
		test=sum(test)
		aggre_train=[]
		for k in range(0,len(train)/slotLength):
			aggre_train.append(sum(train[k*slotLength:k*slotLength+slotLength]))
		train=aggre_train
	return (train,test)


def generateTrainAndTestSamples(vols,slotLength=1,historyLen=10):
	'''
	Generate data for supervised models, such as knn regression, linear 
	regression. Features used for training is historical traffic volumes.
	@param input
	vols: list. A list of traffic volumes for each minute.
	slotLength: int. The number of minutes in each slot. 
	historyLen: int. The number of slots used as features for training models.
	@param output
	trainSamples:list of features. Features are a lot of traffic volumes of 
		former @historyLen slots. 
	trainLabels: list of labels. A label is the traffic volume of next slot for 
		a train sample in @trainSamples.
	testSamples: same as trainSamples.
	testLabels: same as trainLabels.
	'''
	aggregateVols=vols[:]
	if slotLength>1:
		aggregateVols=[]
		for k in range(0,len(vols)/slotLength):
			aggregateVols.append(sum(vols[k*slotLength:k*slotLength+slotLength]))
	samples=[]
	labels=[]
	for k in range(0,len(aggregateVols)/(historyLen+1)):
		sample=aggregateVols[k*(historyLen+1):k*(historyLen+1)+historyLen]
		label=aggregateVols[(k+1)*(historyLen+1)]
		samples.append(sample)
		labels.append(label)
	nTestSamples=60/slotLength
	trainSamples=samples[:-nTestSamples]
	trainLabels=labels[:-nTestSamples]
	testSamples=samples[-nTestSamples:]
	testLabels=labels[-nTestSamples:]
	return (trainSamples,trainLabels,testSamples,testLabels)




if __name__ == '__main__':
	station_en='Xixiang'
	getTrafficPerMinute('20131215',station_en)

	days=['20131213','20131214','20131215']
	ts=generateSeries(days,station_en)
	# print(ts)