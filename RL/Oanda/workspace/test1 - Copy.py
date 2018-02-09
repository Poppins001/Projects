import oandapyV20
import pandas as pd

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
	
	dateFrom = "2017-01-01T00:00:00Z"
	dateTo = "2017-03-01T00:00:00Z"
	granularity = "M15"
	
	getHistory( "EUR_USD", granularity, dateFrom, dateTo )
	
	
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
	
def getHistory( instrument, granularity, dateFrom, dateTo ):
	accountID, token = authAPI()
	api = API( access_token = token )

	params = { "from": dateFrom, "to": dateTo, "granularity": granularity, }
	
	for r in InstrumentsCandlesFactory( instrument = instrument, params = params ):
		api.request( r )
		for i in range( 0, len( r.response["candles"] ) ):
			print( r.response["candles"][i]["time"] )
		#print( len( r.response["candles"] ) )
	
	

#call main
main()