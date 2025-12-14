# World Bank Report Analysis

| Name      | Contribution                         |
|:----------|:-------------------------------------|
|Assad      |                                      |
|Zeyad      | Random Forest Model                  |
|Raghavendra|                                      |
|Stefan     |                                      |
|Sumeet     |                                      |


### Random Forest Model

Random Forest regression model is trained using the training dataset. Random Forest is a learning method that builds many decision trees on samples of the data and averages their predictions. Unlike linear regression, it does not rely on strict assumptions such as linearity or normality, making it suitable for capturing complex, non-linear relationships between housing characteristics and sale prices, the following shows three decision trees from the Random Forest.

![9.RF_3Trees.png](../additional_material/figures/9.RF0.png)

The Random Forest model predicts house sale prices with good accuracy. On the test set, the model’s predictions have an RMSE of about €29,450 and an R² of 0.887, meaning it captures roughly 89% of the variation in actual home prices. The following figure compares the predicted prices to the actual sale prices, showing that most predictions align closely with the observed values.

![9.RF_AcutalvsPred.png](../additional_material/figures/9.RF4.png)

To simplify the model while retaining predictive power, we performed feature selection using a stepwise procedure based on the AIC. This method iteratively added the most informative variables, selecting a subset that balances model complexity and goodness of fit. The figure below compares actual versus predicted sale prices for the full and reduced models. As shown, the reduced model performs similarly to the full model.

![9.RF_FullvsReduced.png](../additional_material/figures/9.RF5.png)

The residual histogram is roughly bell‑shaped and centered near zero, and the residuals‑vs‑fitted plot shows points scattered fairly evenly around zero without a clear pattern, while the QQ‑plot lies close to the reference line except for a few tail points, so together these graphs suggest that the model errors are approximately normal with no strong misspecification.

![9.Residuals.png](../additional_material/figures/9.RF6.png)