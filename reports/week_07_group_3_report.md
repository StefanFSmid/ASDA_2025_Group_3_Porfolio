## 0. Authors of the report

| Name      | Contribution |
|:----------|:-------------|
|Stefan     | Everything   |

## 1. Dataset Overview (of the clean version)

| Item                                                   | Description                                                             |
|:-------------------------------------------------------|:------------------------------------------------------------------------|
| Dataset name                                           | Fish Market                                                                    |
| Number of rows                                         | 159                                                                     |
| Number of columns                                      | 7                                                                       |
| Format file (.csv, .txt, etc)                          | .csv                                                                    |
| Authors of the dataset                                 | Vipul L Rathod (CC0: Public Domain)                                                                       |
| Source (name)                                          | Github                                                                  |
| Source (link)                                          | [Link](https://www.kaggle.com/datasets/vipullrathod/fish-market/data) |

## 2. Dataset Structure

| Feature/variable                  | Data type   | Description               |   # Unique values | Eg. values                      |
|:----------------------------------|:------------|:--------------------------|------------------:|:--------------------------------|
| Species                           | object      | Species name              |               159 | 'Bream'                         |
| Weight                              | float64      | Weight of fish in gram    |               159 | 242                             |
| Length1                            | float64      | Vertical length in CM     |                 159 | 23.2                            |
| Length2                      | float64      | Diagonal length in CM     |                 159 | 25.4                            |
| Length3                  | float64      | Cross length in CM       |                 159 | 30                |
| Height                              | float64       | Height in CM       |                159 | 11.52                    |
| Width             | float64     | Diagonal width in CM |              159 | 4.02              |

## 3. Data cleaning 

_already cleaned dataset_

## 4. Descriptive statistics

### Numeric Columns

|  | Weight | Length1 | Length2 | Length3 | Height | Width |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| count | 159.000000 | 159.000000 | 159.000000 | 159.000000 | 159.000000 | 159.000000 |
| mean | 398.326415 | 26.247170 | 28.415723 | 31.227044 | 8.970994 | 4.417486 |
| std | 357.978317 | 9.996441 | 10.716328 | 11.610246 | 4.286208 | 1.685804 |
| min | 0.000000 | 7.500000 | 8.400000 | 8.800000 | 1.728400 | 1.047600 |
| 25% | 120.000000 | 19.050000 | 21.000000 | 23.150000 | 5.944800 | 3.385650 |
| 50% | 273.000000 | 25.200000 | 27.300000 | 29.400000 | 7.786000 | 4.248500 |
| 75% | 650.000000 | 32.700000 | 35.500000 | 39.650000 | 12.365900 | 5.584500 |
| max | 1650.000000 | 59.000000 | 63.400000 | 68.000000 | 18.957000 | 8.142000 |

### Categorical / Object Columns

|                                  | Species   |
|:---------------------------------|:----------|
| Count                            | 159       |
| Number of unique values          | 7         |
| Most frequent value              | Perch     |
| Most frequent value (frequency)  | 56        |
| Least frequent value             | Whitefish |
| Least frequent value (frequency) | 6         |

### 5. Analysis - Research question
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

### 6. AI Disclaimer
