#load all our of years of data from out data folder
import glob

import pandas as pd
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

all_files = glob.glob("fpi-data/*.csv")
all_data = pd.concat((pd.read_csv(f, index_col=None, header=0) for f in all_files),ignore_index=True,sort=True)

# add wins column to df
print(all_data)

# add wins column to df
all_data['Wins'] = all_data.apply(lambda row: int(str(row['w-l']).split('-')[0]), axis=1)

#Use FPI as our predictor and we're trying to predict Wins
x = all_data.fpi.values.reshape(-1, 1)
y = all_data.Wins.values


xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size=1/4, random_state=0)

#Simple Linear regression from sklearn
regr = LinearRegression()
regr.fit(xTrain,yTrain)
score = regr.score(xTrain, yTrain)

#create the data to draw our line
fit = regr.predict(xTest)

#Basic components of our linear reg fit
print("intercept: " + str(regr.intercept_))
print("coefficient: " + str(regr.coef_))
print("R^2: " + str(score))
print("Mean Squared Error: " + str(mean_squared_error(fit, yTest)))

#draw our sccatter plot
plt.scatter(x, y,  color='blue')
plt.plot(xTest, fit, color='black', linewidth=3)
plt.xticks((-30.0,-25,-20,-15,-10,-5,0,5,10,15,20,25,30))
plt.yticks((0,2,4,6,8,10,12,14,16))
plt.ylim([-1,16])
plt.title("NCAA Wins as a function of FPI")
plt.xlabel("FPI")
plt.ylabel("Wins")
plt.show()
