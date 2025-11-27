Fish regression analysis - Instruction Guidelines
Data: see GitHub 
Data documentation: [see Kaggle](https://www.kaggle.com/datasets/vipullrathod/fish-market/data)

Weight: (Weight in grams) This column represents the weight of the fish. It is a numerical variable that is typically measured in grams. The weight is the dependent variable we want to predict using polynomial regression.

Length1: (Vertical length in CM) This column represents the first measurement of the fish's length. It is a numerical variable, typically measured in centimetres.

Length2: (Diagonal length in CM) This column represents the second measurement of the fish's length. It is another numerical variable, typically measured in centimetres.

Length3: (Cross length in CM) This column represents the third measurement of the fish's length. Similar to the previous two columns, it is a numerical variable, usually measured in centimetres.

Height: (Height in CM) This column represents the height of the fish. It is a numerical variable, typically measured in centimetres.

Width: (Width in CM) This column represents the width of the fish. Like the other numerical variables, it is also typically measured in centimetres.

General instructions
Create a Report in markdown that predicts Fish Weight and submit it with the respective notebook to GitHub.

Notebook:
→ Some basic initial inspections
Import the data
display the first, the last and a random sample of 7 entries
check data types
check duplicates and missing values
basic summary statistics for both categorical and numerical variables
basic plots for categorical and numerical variables to check distributions and counts (histogram, barplot)

→ Linear regression steps
Question/hypothesis
Check assumptions: normal distribution of dependent variable? --> if not transform
Check assumptions: multicollinearity (= redundancies among predictors)?
 	- with correlations
	- with the variance inflation factor
--> throw out redundant variables
Split the data in train and test data
Preprocess the data: 
scale the numerical predictors - if you include multiple numerical predictors
one hot encode the categorical predictors - if you include categorical predictors
Train linear regression on training set
Predict on test set and evaluate with metrics (e.g. MAE, RMSE, MAPE, R2)
Plots
- scatterplot with regression line
- actual vs. predicted values
- histogram of residuals: normal distribution? → if not, investigate why not?


→ Optional: try a Mixed Effect Model (Wanja can assist)


