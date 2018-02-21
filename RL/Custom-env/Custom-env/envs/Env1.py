import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import pandas as pd


class ENV1_NAME( gym.Env ):
    '''Fx environment
    Overview:
        * loads historical data from most major pairs with MA and MACD
        * applies +/- random noise to generate additional data
        * simulates p/l, transaction costs
        * returns reward daily (done signal)
    Action space:
        open buy, open sell, close pos, do nothing
    Observation space:
        1) open, 2) high, 3) low, 4) close, 5) MACD, 6) hist, 7) maFast,
        8) maSlow, 9) position( long/short/neutral ), 10) indexDay, 11) plFloating,
    '''
    dataFile = "..\..\..\Oanda\workspace\historical-data\EUR_USD-M15-2008-01-01T00_00_00Zto2018-01-01T00_00_00Z"

    def __init__( self, lengthDay = 96, transCost = 0.03 ):
        '''setup the environment'''
        self.action_space = spaces.Discrete( 4 ) #model output dim
        self.observation_space = spaces.Discrete( 11 ) #model input dim
        self.lengthDay = lengthDay      #number of states in one day
        self.indexDay = 1      #current position in day (1 to self.lengthDay)
        self.position = 0       #start day with neutral position in market
        self.plDay = 0         #start day with no profit/loss
        self.plFloating = 0     #state of open position's profit/loss
        self.openPrice = 0      #price at which position is opened
        self.closePrice = 0     #price at which position is closed
        self.transCost = transCost      #penalty for opening and closing positions

        self.state = None       #clear initial state

        self.rawDataframe = pd.read_pickle( path = dataFile )
        self.lengthData = len( self.rawDataframe )
        self.indexData = 0      #start at first row in df
        self.stateDay = self.rawDataframe.iloc[self.indexData : self.indexData + self.lengthDay]     #one days worth of states
        #create random noise and mix with data
        noise = np.random.normal( 0, 0.001, self.lengthDay )
        noiseOpen, noiseHigh, noiseLow, noiseClose, noiseMACD, noiseHist, noiseMA10, noiseMA50 = []
        for i in range(self.indexData, self.indexData + self.lengthDay):
            noiseClose.append( float(self.stateDay['close'][i]) + noise[i]) )
            noiseHigh.append( float(self.stateDay['high'][i]) + noise[i]) )
            noiseLow.append( float(self.stateDay['low'][i]) + noise[i]) )
            noiseOpen.append( float(self.stateDay['open'][i]) + noise[i]) )
            noiseMACD.append( float(self.stateDay['macd'][i]) + noise[i]) )
            noiseHist.append( float(self.stateDay['hist'][i]) + noise[i]) )
            noiseMA10.append( float(self.stateDay['ma10'][i]) + noise[i]) )
            noiseNA50.append( float(self.stateDay['ma50'][i]) + noise[i]) )

        self.dfState = pd.DataFrame( { "close": noiseClose, "high": noiseHigh, "low": noiseLow, "open": noiseOpen, "macd": noiseMACD, "hist": noiseHist, "ma10": noiseMA10, "ma50": noiseMA50 } )
        #add additional staring info to state
        dfState["position"] = self.position
        dfState["indexDay"] = self.indexDay
        dfState["plFloating"] = self.plFloating
        #set starting state
        self.state = self.dfState.iloc[self.indexDay - 1]   #starting state


        self._seed()


    def _seed( self, seed = None ):
        '''random seed for environment'''
        self.np_random, seed = seeding.np_random( seed )
        return [seed]

    def _step( self, action ):
        assert self.action_space.contains( action )
        '''increment action on environment. Returns new state, reward and observations'''
        if action == 0:
            #open buy
        elif action == 1:
            #open sell
        elif action == 2:
            #close position
        elif action == 3:
            #do nothing

        '''reward and new state'''

    def _reset( self ):

        self.indexData += 96    #increment day
        if self.indexData > self.lengthData - 96:
            self.indexData = 0     #wrap back to start of data
        self.indexDay = 1
        self.position = 0
        self.plDay = 0
        self.plFloating = 0

        self.stateDay = self.rawDataframe.iloc[self.indexData : self.indexData + self.lengthDay]     #one days worth of states
        #create random noise and mix with data
        noise = np.random.normal( 0, 0.001, self.lengthDay )
        noiseOpen, noiseHigh, noiseLow, noiseClose, noiseMACD, noiseHist, noiseMA10, noiseMA50 = []
        for i in range(self.indexData, self.indexData + self.lengthDay):
            noiseClose.append( float(self.stateDay['close'][i]) + noise[i]) )
            noiseHigh.append( float(self.stateDay['high'][i]) + noise[i]) )
            noiseLow.append( float(self.stateDay['low'][i]) + noise[i]) )
            noiseOpen.append( float(self.stateDay['open'][i]) + noise[i]) )
            noiseMACD.append( float(self.stateDay['macd'][i]) + noise[i]) )
            noiseHist.append( float(self.stateDay['hist'][i]) + noise[i]) )
            noiseMA10.append( float(self.stateDay['ma10'][i]) + noise[i]) )
            noiseNA50.append( float(self.stateDay['ma50'][i]) + noise[i]) )

        self.dfState = pd.DataFrame( { "close": noiseClose, "high": noiseHigh, "low": noiseLow, "open": noiseOpen, "macd": noiseMACD, "hist": noiseHist, "ma10": noiseMA10, "ma50": noiseMA50 } )
        #add info to state
        dfState["position"] = self.position
        dfState["indexDay"] = self.indexDay
        dfState["plFloating"] = self.plFloating
        #new starting state
        self.state = self.dfState.iloc[self.indexDay - 1]       #new starting state for next day

    def _render( self ):
        '''displays env state and observations from actions'''
