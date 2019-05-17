import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import glob

#load all our of years of data from out data folder
all_files = glob.glob("data/*.csv")
all_data = pd.concat((pd.read_csv(f, index_col=None, header=0) for f in all_files),ignore_index=True,sort=True)

#Use Net points per drive as our predictor and we're trying to predict Wins
x = all_data.NPD.values.reshape(-1, 1)
y = all_data.Wins.values.reshape(-1, 1)

xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size = 1/3, random_state = 0)

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

#draw the sccatter plot
plt.scatter(x, y,  color='blue')
plt.plot(xTest, fit, color='black', linewidth=3)
plt.xticks(())
plt.yticks(())
plt.title("NCAA Wins as a function of NPD")
plt.xlabel("Net Points per drive")
plt.ylabel("Wins")
plt.show()