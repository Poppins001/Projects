import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import Adam

fileName = "C:\\Users\\Genn\\github\\Projects\\RL\\Oanda\\workspace\\historical-data\\EUR_USD-M15-2008-01-01T00_00_00Zto2018-01-01T00_00_00Z"
rawData = pd.read_pickle( path = fileName )

labels = []

for i in range(0, len(rawData) - 1):
    if float(rawData["close"][i + 1]) > float(rawData["close"][i]):
        labels.append( 1 )      #greater than previous
    else:
        labels.append( 0 )      #less than previous
labels.append( 0 )

rawData['labels'] = labels

data = rawData[50 : len(rawData) -1]
'''
train = data[ : len(rawData) - 25000]
test = data[len(rawData) - 25000 : ]

xTrain = np.array(train.drop('labels', 1))
yTrain = np.array(train['labels'])
xTest = np.array(test.drop('labels', 1))
yTest = np.array(test['labels'])
'''
xData = np.array( data.drop('labels', 1) )
yData = np.array( data['labels'] )


model = Sequential()
model.add( Dense(4, input_dim = 8, activation = 'relu') )
model.add( Dense(4, activation = 'relu') )
model.add( Dense(4, activation = 'relu') )
model.add( Dense(4, activation = 'relu') )
model.add( Dense(4, activation = 'relu') )
model.add( Dense(4, activation = 'relu') )
model.add( Dense(4, activation = 'relu') )
model.add( Dense(4, activation = 'relu') )
model.add( Dense(1, activation = 'tanh') )

adam = Adam( lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0 )

model.compile( loss = 'binary_crossentropy', optimizer = 'adam', metrics = ['accuracy'] )

model.fit( xData, yData, epochs = 1000, batch_size = 96, validation_split = 0.1 )

score = model.evaluate( xTest, yTest, batch_size = 96 )
print(score)
