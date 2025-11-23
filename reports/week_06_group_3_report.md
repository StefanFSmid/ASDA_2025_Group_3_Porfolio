# World Bank Report Analysis

| Name      | Contribution                         |
|:----------|:-------------------------------------|
|Assad      | Corruption vs Gov Effectiveness, Final Report Creation |
|Zeyad     | Political Stability vs Inflation                |
|Shiva     | Life expectancy vs GDP    |
|Stefan      |CO2 vs Renewable Energies                 |
|Sumeet     |                           |





<details>
  <summary><b>Background</b></summary>
<br>

This project uses World Bank indicators across governance, environmental sustainability, economic performance, and human well-being to understand how countries develop around the world. One important observation is that the data for most indicators is **not normally distributed**, which affects statistical testing but does not hide the overall trends.

Across all themes, a consistent trend appears: **A country's income level makes a big difference**. Wealthier nations generally have stronger institutions, better social services, and more stable economies. Poorer countries face bigger challenges but often rely more on agriculture and renewable resources. Middle-income countries are somewhere in between, balancing growth, development, and environmental pressures.

A brief summary of analysis as follows:

| **Theme** | **Indicators Selected** | **Key Patterns Observed** | **Overall Analysis** |
|----------|--------------------------|----------------------------|-----------------------------|
| **Governance** | Government effectiveness, control of corruption, rule of law, voice & accountability, political stability | None of the indicators are normally distributed; higher-income countries consistently score higher; variance is lowest in high-income countries. | Governance strength and institutional quality rise with income levels. |
| **Environment** | CO₂ emissions, renewable energy consumption %, forest land %, agricultural land % | High-income countries emit the most CO₂ but maintain stable forests; low-income countries rely heavily on agriculture and renewables; middle-income countries are transitioning. | Environmental outcomes reflect stages of development and industrialization. |
| **Economic Performance** | GDP, inflation %, tax revenue % | High-income = strong GDP and stable inflation; low-income = weak tax capacity and high inflation; middle-income = transitioning. | Higher income is linked with economic stability and stronger fiscal systems. |
| **Human Well-Being** | Life expectancy, education spending %, health spending %, access to electricity %, population density | High-income countries lead in health, education spending, and electrification; low-income countries show large gaps; population density varies independently of income. | Human well-being improves with income, except density which depends on geography. |


</details>

---

_A further analysis is done by the group to independently study the correlation between various indicators from the data set and draw individual inferences._

<details>
  <summary><b>Control of Corruption vs Government Effectiveness</b></summary>
<br>

**How does control of corruption relate to government effectiveness across countries from 2000 to 2024, and does this relationship vary across income groups?**

The data consist of two governance indicators: **control_of_corruption_estimate** and **gov_effectiveness_estimate**. Inspection of the distributions shows that neither variable follows a normal distribution, even after attempts at log transformation. Some countries exhibit extreme values due to political crises or exceptionally stable governance systems. Given the non-normality between the two indicators, the Spearman correlation is chosen as the most appropriate statistical test for this analysis.


![1.Histogram.png](../additional_material/1.Histogram.png)

A scatter plot grouped by income level shows a clear positive trend, with high-income countries clustering at high values for both indicators, middle-income countries showing moderate values, and low-income countries appearing at lower levels. The spearman correlation is strongest for high-income countries **(0.9)** and weakest for lower-middle income countries **(0.7)**

![1.Scatterplot.png](../additional_material/1.Scatterplot.png)

The Spearman correlation for the overall dataset is **0.918** with a p-value < 1e-10, indicating a very strong and statistically significant positive relationship between control of corruption and government effectiveness.

As expected, a temporal analysis showed similar trends pre and post 2008 as can be seen below:

![1.Temporal.png](../additional_material/1.Temporal.png)

Additional analysis for selected countries highlight the two extreme dynamics: 

1. **Yemen** is a country that has had political instability, civil war, and governance challenges over the past 20+ years. Because of this instability, both corruption control and government effectiveness fluctuate together (mostly both deteroriate together) and hence correlation is one of the highest.

2. **Thailand** is a relatively stable country and small changes in corruption and government effectiveness don’t always happen together. In some years, government effectiveness may improve slightly due to reforms, while corruption stays nearly the same. In other years, corruption may worsen a bit, but overall government effectiveness does not change much. This uncoordinated movement means that year-to-year fluctuations are not aligned, which is why the correlation between the two indicators is low.

![1.Pattern.png](../additional_material/1.Pattern.png)

</details>

---

<details>
  <summary><b>Political_Stability vs Inflation</b></summary>

<br>

**How does Political Stability relate to Inflation across countries?**

Given the non-normal data distribution, our analysis examines the relationship between political stability and inflation using Spearman correlation



</details>

---

<details>
  <summary><b>GDP vs Life Expectancy</b></summary>

----

**Does higher economic output (GDP) relate to higher life expectancy across countries, and does this relationship differ by income group and over time?**

---

### Data Inspection
The distributions of GDP and life expectancy were explored using histograms and boxplots. GDP showed a highly right-skewed distribution, with a small number of extremely wealthy countries. Life expectancy showed a more balanced distribution with fewer extreme outliers.

Because GDP was highly skewed, a logarithmic transformation was applied to improve interpretability.

**Figures:**  
 ![s_1.png](../additional_material/s_1.png)
![s_2.png](../additional_material/s_2.png)

---

### Visualization
A scatter plot of log(GDP) against life expectancy shows a clear upward trend. Countries with higher GDP tend to have higher life expectancy. However, the pattern flattens at very high income levels, suggesting diminishing returns.

A grouped scatter plot shows high-income countries clustering at high GDP and life expectancy, while low-income countries cluster at lower values.

**Figures:**  
![s_5.png](../additional_material/s_5.png)

---

### Statistical Test
Both Pearson and Spearman correlations were computed:

- **Pearson r = 0.443 (p < 0.001)**
- **Spearman ρ = 0.471 (p < 0.001)**

The Spearman correlation for GDP and life expectancy is ρ = 0.471, indicating a moderate positive relationship.

Spearman was preferred because GDP was strongly skewed even after transformation.

---

### Group-Level Analysis (Income Groups)
Correlation by income group:

- Low income: ρ = 0.351  
- Lower-middle income: ρ = 0.331  
- Upper-middle income: ρ = 0.295  
- High income: ρ = 0.474  
**Figures:**  
![s_7.png](../additional_material/s_7.png)

This shows the relationship is strongest in lower-income countries.

---

### Temporal Analysis (Pre vs Post 2008)
The relationship was tested before and after the 2008 financial crisis:

- **Pre-2008: ρ = 0.422**  
- **Post-2008: ρ = 0.450**

The positive relationship remained stable over time.

**Figures:**  
![s_6.png](../additional_material/s_6.png)

---





### Interpretation
Countries with higher economic resources tend to have higher life expectancy. This effect is stronger in poorer countries. The results show correlation, not causation as GDP alone does not cause better health. Factors like governance, healthcare systems, and education also play important roles.

---

### Main Takeaway
Economic growth and human well-being are strongly connected, but wealth alone is not enough. How resources are used becomes more important as countries become richer.

</details>

---

<details>
  <summary><b>CO₂ emissions vs Renewable Energy Use</b></summary>
<br>

**Is there a correlation between CO₂ emissions per capita and renewable energy consumption across different countries and times?**

This analysis investigates how CO₂ emissions per capita relate to renewable energy consumption globally. The analysis was performed only for the year 2023 as a subset of the entire data. Initially, outliers were identified and stripped off with a threshold value of 18.45:


![4.Boxplots.png](../additional_material/4.Boxplots.png)

The histograms showing the spread were as follows:

![4.Histogram.png](../additional_material/4.Histogram.png)






The two world maps show opposing trends: In the Global North high CO₂ per capita emissions are observed while renewable energy consumption is, relatively speaking, low. In contrast, in the Global South, and especially in sub-Saharan Africa, low CO₂ emissions and moderate to high renewable energy consumption are seen.

![4.Worldmap.png](../additional_material/4.Worldmap.png)



The scatterplot reflects the spatial distribution and trend that was already visible in the world map. As the data is not normally distributed (Poisson-like), the Spearman's correlation coefficient was used for obtaining the correlation coefficient. The correlation is negative and high (=-0.76), i. e., the higher the CO₂-per-capita-emissions, the lower the market share / consumption of renewables.

![4.Scatterplot.png](../additional_material/4.Scatterplot.png)



As can be seen in the figure, Germany has experienced a steady decrease in CO₂ emissions while investing in renewable energy. The correlation is very high (=-0.98). This clear trend seems to reflect the country's ambition regarding energy transition ("Energiewende") in face of climate change and, hence, even a causality might be implied here. However, this cannot be understood from the data alone but needs 

![4.Linegraph.png](../additional_material/4.Linegraph.png)

</details>

---

<details>
  <summary><b>AI Disclaimar</b></summary>
<br>

