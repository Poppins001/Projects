import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

s = pd.Series( np.random.randn(100),
               index=pd.date_range('1/1/2000',
               periods=100) )

s = s.cumsum()
'''
r5 = s.rolling( window = 5 )
r10 = s.rolling( window = 10 )
r20 = s.rolling( window = 20 )

r5.mean().plot( style = 'b--' )
r10.mean().plot( style = 'r--' )
r20.mean().plot( style = 'g--' )
s.plot( style = 'k' )
'''

ema10 = EMA( s, 10 )
ema50 = EMA( s, 50 )

macd, hist = MACD( s, 12, 26, 9 )

s.plot( style = 'r' )
macd.plot( style = 'k' )
hist.plot( style = 'b--' )

ema10.plot( style = 'g' )
ema50.plot( style = 'g--' )

plt.show()
