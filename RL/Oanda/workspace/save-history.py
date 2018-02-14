import oandapyV20
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from oandapyV20 import API
import oandapyV20.endpoints.pricing as pricing
from oandapyV20.contrib.factories import InstrumentsCandlesFactory
from oandapyV20.endpoints.instruments import InstrumentsCandles

#main
def main():

	accountID, token = authAPI()

	api = API( access_token = token )

	#params = { "instruments": "EUR_USD" }

	#r = pricing.PricingInfo( accountID = accountID, params = params)

	#rv = api.request( r )

	#print( r.response["time"], type(r.response["time"]) )
	#print( float(r.response["prices"][0]["asks"][0]["price"]) )

	dateFrom = "2017-01-03T00:00:00Z"
	dateTo = "2017-01-04T00:00:00Z"
	granularity = "M15"
	freq = "15Min"		#Pandas freq for series

	getHistory( "EUR_USD", granularity, dateFrom, dateTo, freq )


	# params2 = { "from": dateFrom, "to": dateTo, "granularity": granularity, } #"from": dateFrom, "granularity": granularity, "count": 5000

	# r = InstrumentsCandles( instrument = "EUR_USD", params = params2 )
	# api.request( r )

	# for i in range( 0, len(r.response["candles"]) ):
		# print( r.response["candles"][i]["time"], "l", r.response["candles"][i]["mid"]['l'], "o", r.response["candles"][i]["mid"]['o'], "c", r.response["candles"][i]["mid"]['c'], "h", r.response["candles"][i]["mid"]['h'] )

	# print(len(r.response["candles"]))


#function definitions
def authAPI():
	with open("C:/Winpy_Keras/WinPython-64bit-3.5.2.3Qt5/Oanda/oandapyV20-examples/account.txt" ) as fp:
		accountID = fp.read().strip()
	with open("C:/Winpy_Keras/WinPython-64bit-3.5.2.3Qt5/Oanda/oandapyV20-examples/token.txt" ) as fp:
		token = fp.read().strip()
	return accountID, token

def getHistory( instrument, granularity, dateFrom, dateTo, freq ):
	history = []
	historyOpen = []
	historyHigh = []
	historyLow = []
	historyClose = []
	accountID, token = authAPI()
	api = API( access_token = token )

	params = { "from": dateFrom, "to": dateTo, "granularity": granularity, }

	for r in InstrumentsCandlesFactory( instrument = instrument, params = params ):
		api.request( r )
		for i in range( 0, len( r.response["candles"] ) ):
			history.append( r.response["candles"][i]["mid"] )
		#print( len( r.response["candles"] ) )


	sHistory = pd.Series( history, index = pd.date_range( start = dateFrom, periods= len(history), freq = freq ))

	for i in range( 0, len( history ) ):
		historyOpen.append( sHistory.values[i]["o"] )	#add open values to list
		historyHigh.append( sHistory.values[i]["h"] )	#add high values to list
		historyLow.append( sHistory.values[i]["l"] )	#add low values to list
		historyClose.append( sHistory.values[i]["c"] )	#add close values to list

	#print( historyOpen[0], historyHigh[0], historyLow[0], historyClose[0] )

	dfHistory = pd.DataFrame( { "open": historyOpen, "high": historyHigh, "low": historyLow, "close": historyClose },
	 							index = pd.date_range( start = dateFrom, periods= len(history), freq = freq ) )
	#print( dfHistory )

	macdHistory, histHistory = MACD( dfHistory.close, fast = 12, slow = 26, signal = 9 )

	'''
	macdHistory.plot( style = 'k' )
	histHistory.plot( style = 'b--' )
	plt.show()
	'''

	ma10 = EMA( dfHistory.close, 10 )
	ma50 = EMA( dfHistory.close, 50 )

	'''
	ma10.plot( style = 'k' )
	ma50.plot( style = 'b--' )
	plt.show()
	'''

	dfHistory["macd"] = macdHistory		#add macd column to dataframe
	dfHistory["hist"] = histHistory		#add histograph column to dataframe

	dfHistory["ma10"] = ma10			#add ma10 to DataFrame
	dfHistory["ma50"] = ma50			#add ma50 to DataFrame

	print( dfHistory.index )



'''-----------------------------------END MAIN-------------------------------'''
#returns series, slowEMA - fastEMA and histogram; EMA of MACD
def MACD( series, fast, slow, signal ):
    slowEMA = series.ewm( span = slow ).mean()
    fastEMA = series.ewm( span = fast ).mean()
    MACD = slowEMA - fastEMA
    histogram = MACD.ewm( span = signal ).mean()

    return( MACD, histogram )

#returns exponential moving average
def EMA( series, n ):
    ema = series.ewm( span = n ).mean()

    return( ema )

#call main
main()
