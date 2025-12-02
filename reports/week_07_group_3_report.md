# Fish Regression Analysis

## 0. Authors of the report

| Name      | Contribution |
|:----------|:-------------|
|Stefan     | Data Loading, Analysis and Report    |
|Assad      | Analysis and Report                  |


<details>
  <summary><b>1. Dataset Overview</b></summary>
<br>
| Item                                                   | Description                                                             |
|:-------------------------------------------------------|:------------------------------------------------------------------------|
| Dataset name                                           | Fish Market                                                                    |
| Number of rows                                         | 159                                                                     |
| Number of columns                                      | 7                                                                       |
| Format file (.csv, .txt, etc)                          | .csv                                                                    |
| Authors of the dataset                                 | Vipul L Rathod (CC0: Public Domain)                                                                       |
| Source (name)                                          | Github                                                                  |
| Source (link)                                          | [Link](https://www.kaggle.com/datasets/vipullrathod/fish-market/data) |
| Date of download                                       | 27.11.2025                                                           |

</details>


<details>
  <summary><b>2. Dataset Structure</b></summary>
<br>


| Feature/variable                  | Data type   | Description               |   # Unique values | Eg. values                      |
|:----------------------------------|:------------|:--------------------------|------------------:|:--------------------------------|
| Species                           | object      | Species name              |               159 | 'Bream'                         |
| Weight                              | float64      | Weight of fish in gram    |               159 | 242                             |
| Length1                            | float64      | Vertical length in CM     |                 159 | 23.2                            |
| Length2                      | float64      | Diagonal length in CM     |                 159 | 25.4                            |
| Length3                  | float64      | Cross length in CM       |                 159 | 30                |
| Height                              | float64       | Height in CM       |                159 | 11.52                    |
| Width             | float64     | Diagonal width in CM |              159 | 4.02              |



</details>

<details>
  <summary><b>3. Data Cleaning</b></summary>
<br>

_No missing/duplicate values were found in the data set. No issues with column names and data types was observed either_


</details>

<details>
  <summary><b>4. Basic Statistics and Plots</b></summary>
<br>


|       |   Weight |   Length1 |   Length2 |   Length3 |   Height |   Width |
|:------|---------:|----------:|----------:|----------:|---------:|--------:|
| count |   159    |    159    |    159    |    159    |   159    |  159    |
| mean  |   398.33 |     26.25 |     28.42 |     31.23 |     8.97 |    4.42 |
| std   |   357.98 |     10    |     10.72 |     11.61 |     4.29 |    1.69 |
| min   |     0    |      7.5  |      8.4  |      8.8  |     1.73 |    1.05 |
| 25%   |   120    |     19.05 |     21    |     23.15 |     5.94 |    3.39 |
| 50%   |   273    |     25.2  |     27.3  |     29.4  |     7.79 |    4.25 |
| 75%   |   650    |     32.7  |     35.5  |     39.65 |    12.37 |    5.58 |
| max   |  1650    |     59    |     63.4  |     68    |    18.96 |    8.14 |

### Categorical / Object Columns

|                                  | Species   |
|:---------------------------------|:----------|
| Count                            | 159       |
| Number of unique values          | 7         |
| Most frequent value              | Perch     |
| Most frequent value (frequency)  | 56        |
| Least frequent value             | Whitefish |
| Least frequent value (frequency) | 6         |


### Basic Plots to check distribution and count

![7.Histograms.png](../additional_material/figures/7.Histograms.png)
![7.Boxplots.png](../additional_material/figures/7.Boxplots.png)
![7.SpecieCount.png](../additional_material/figures/7.SpecieCount.png)



</details>

<details>
  <summary><b>5. Analysis - Research question</b></summary>
<br>

### Question/hypothesis
**Hypothesis:** 
The weight of fish can be estimated based on their length, width, and height.

### Assumption check: Is weight a normally distributed variable?

![20251201_Fig01.png](../additional_material/figures/20251201_Fig01.png)

**Answer:** 
The dependent variable is not normally distributed and only the sqrt transformation yields a more symmetric distribution. Thus, we will proceed with the sqrt transformed weight and check the residual distributions later.

### Assumption check: Are variables multicollinear, i.e., redundant?

_- based on correlations:_

![20251201_Fig02.png](../additional_material/figures/20251201_Fig02.png)

_- based on the variance inflation factor_

|    | Variable   |      VIF |
|---:|:-----------|---------:|
|  0 | Weight     |    55.11 |
|  1 | Length1    | 13608    |
|  2 | Length2    | 16752.3  |
|  3 | Length3    |  3561.2  |
|  4 | Height     |    91.38 |
|  5 | Width      |    93.16 |

**Answer:** 
Due to the high VIF and the similar correlation, Length1 and Length2 are dropped while Length3 is kept as it is the most representative length measure (combination of both).

### Modelling
**Comment:**
Due to our research hypothesis, we will use a linear regression model to predict the weight of fish based on their Length3 (i.e. cross length), Height, and Width.

#### Evaluation Metrics

|    | Metric                                |   Value |
|---:|:--------------------------------------|--------:|
|  0 | Mean Absolute Error (MAE)             |    1.17 |
|  1 | Root Mean Squared Error (RMSE)        |    1.47 |
|  2 | Mean Absolute Percentage Error (MAPE) |   15.19 |
|  3 | R^2 Score                             |    0.98 |



|    | Metric                                |   Value |
|---:|:--------------------------------------|--------:|
|  0 | Mean Absolute Error (MAE)             |    0.14 |
|  1 | Root Mean Squared Error (RMSE)        |    0.17 |
|  2 | Mean Absolute Percentage Error (MAPE) |    3.97 |
|  3 | R^2 Score                             |    0.98 |

#### Predicted vs Actual values and Residuals

![7.UpdatedGraphs.png](../additional_material/figures/7.UpdatedGraphs.png)


**Answer:**
The two plots above show the predicted vs actual values and the histogram of the residuals. The predicted vs actual values plot indicates that the model performs well, as the points are closely aligned with the diagonal line. The histogram of the residuals appears to be approximately normally distributed, suggesting that the model assumptions are reasonably met.

### Final summary

The linear regression model was trained to predict the square root transformed weight of the fish species under consideration based on their cross length, weight, and height. The model resulted in an R² score of approximately 0.98 on the test set, which can be interpreted as a strong fit. Further improvements could involve exploring non-linear models or incorporating additional features (e.g., species as a dummy variable).


</details>

<details>
  <summary><b>6. AI Disclaimer</b></summary>
<br>
- Use of PyCharm with Github copilot (inline code suggestions) 
</details>