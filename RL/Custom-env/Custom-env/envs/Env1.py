import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np


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

    def __init__( self, day = 96, transCost = 0.03 ):
        '''setup the environment'''
        self.action_space = spaces.Discrete( 4 ) #model output dim
        self.observation_space = spaces.Discrete( 11 ) #model input dim
        self.day = day      #number of states in one day
        self.indexDay = 1      #current position in day (1 to self.day)
        self.position = 0       #start day with neutral position in market
        self.plDay = 0         #start day with no profit/loss
        self.plFloating = 0     #state of open position's profit/loss
        self.openPrice = 0      #price at which position is opened
        self.closePrice = 0     #price at which position is closed
        self.transCost = transCost      #penalty for opening and closing positions

        self._seed()
        self._reset()


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
        '''load data for day,
            reset position variables,
        '''
        #resets env on done signal
        self.indexDay = 1
        self.position = 0
        self.plDay = 0
        self.plFloating = 0

    def _render( self ):
        '''displays env state and observations from actions'''
