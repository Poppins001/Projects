import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np


class ENV1_NAME( gym.Env ):

    def __init__( self ):
        '''setup the environment'''
        self.action_space = spaces.Discrete( ) #model output dim
        self.observation_space = spaces.Discrete( ) #model input dim


        self._seed()

    def _seed( self, seed = None ):
        '''random seed for environment'''
        self.np_random, seed = seeding.np_random( seed )
        return [seed]

    def _step( self, action ):
        '''increment action on environment. Returns new state, reward and observations'''

        '''reward'''
        

    def _reset( self ):
        '''resets env on done signal'''

    def _render( self ):
        '''displays env state and observations from actions'''
