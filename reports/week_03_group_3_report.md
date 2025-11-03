## 1. Dataset Overview (of the clean version)

| Item                              | Description |
|:----------------------------------|:-----------:|
| Dataset name                      |Lego Dataset |
| Authors                           |Combined dataset of all groups in the class|
| Number of entries                 |204rows, 10 columns|
| Number of features/variables      |10           |
| Format file (.csv, .txt, etc)     |.xlsx        |

## 2. Dataset Structure (of the clean version) (STEFAN SMID)

| Feature/variable | Data type  | Description | Number of Unique values |      Example values       |
|:-----------|:-----------:|:-----------:|:-----------------------:|:-------------------------:|
| base dimensions | object |      The dimensions of the base using number of studs as the unit. Avoid to use length units.       |           12            |         1x1, 1x4          |
| base shape | object |      The shape of the base       |            5            |     Circle, Trapezium     |
| color | object |        The color of the piece     |           62            | neonlightyellow, darkblue |
| has slope? | object |     Whether the piece has a slope or not        |            2            |          No, Yes          |
| is duplo? | object |      Whether the piece is duplo or not       |            2            |          No, Yes          |
| number of studs | float64 |       The number of studs on the piece      |           10            |         1.0, 4.0          |
|            size type     |     object    |         The type of piece: brick or plate    |            2            |       Plate, Brick        |
|     slope degree            |     float64    |      The degree of the piece with slope       |            4            |         0.0, 45.0         |
|            in stock     |     int64    |         How many pieces are in the bag.    |            3            |             1             |


## 3. Descriptive statistics (of the clean version)

**HINT: instead of formatting by hand or AI copy output of respective functions as markdown and copy paste here**

### Numeric Columns
|                    | number of studs      | slope degree         | in stock|
|--------------------|----------------------|----------------------|-------|
| Count              | 204.000000	                | 204.000000                | 204.0 |
| Mean               | 4.906863 | 5.073529 | 1.0 |
| Standard deviation | 4.996171    | 14.111431    | 0.0 |
| Min                | 0.000000	 | 0.000000	 | 1     |
| 25%                | 2.000000	 | 0.000000 |1.0     |
| 50%                | 4.000000	 | 0.000000 | 1.0    |
| 75%                | 6.000000	 | 0.000000 | 1.0    |
| Max                | 24.000000	 | 45.000000	 | 1.0   |

### Categorical / Object Columns

|                                  | color | is duplo?	 | size type | base shape	 | base dimensions | has slope? | 
|----------------------------------|-------|----------------|--------|----------------|----------|----------|
| Count                            | 204 | 204          | 204  | 204          | 204    | 204    |    
| Number of unique values          | 62     | 2              | 2      | 5            | 14     | 2     |
| Most frequent value              | yellow  | No         | Plate  | Rectangle          | 2x2  | No  |
| Most frequent value (frequency)  | 16 | 171          | 108  | 109           | 47       | 180       |
| Least frequent value             | transparentskyblue | Yes           | Brick    | Triangle           | 3x2      | Yes     |
| Least frequent value (frequency) | 1  | 33            | 96      | 2           | 2       | 24      |




## 3. _Exploratory plots (optional)_
_Feel free to create some basic plots if they are necessary to understand the dataset._

## 4. Data cleaning procedure
### 4.1 Major data inconsistencies:

Column labeling was generally consistent, except for one unnecessary column, Transparent, which was used by only one of the five groups. To maintain consistency, this column was removed.

Data types varied across groups. For example, yes/no responses were recorded inconsistently as 1/0/True/False, and the slope degree column was sometimes left blank instead of using 0. Additionally, the base dimensions column contained interchangeable values, such as 2x4 and 4x2, which represent the same dimension. All such discrepancies were standardized and unified according to the conventions established by our group during data collection.

The most inconsistent category was color, due to the subjective nature of this attribute. Differences included capitalization, extra spaces, and spelling errors. While some colors were very similar (e.g., dark blue vs. navy blue), only basic cleaning was performed, and all original color values were retained to reflect the true inputs from each group.


### 4.2 Minor data inconsistencies _(if some issues cannot be reported in the above table)_
One of the listed shapes, “Wadge” (or “Wedge”), was replaced with “Trapezium” at our discretion, as a wedge represents a 3D shape, while base dimensions should correspond to 2D shapes.

## 5. Recommendations for good practices regarding data collection (Raghavendra)
To make data collection easier and more accurate, all groups should agree on one common format for each variable before starting. Having the same structure for things like colors, shapes, and dimensions would keep the data consistent and save a lot of time during cleaning. Using the same color names, for example, would help avoid duplicate entries caused by small spelling or capitalization differences. It would also help to set clear rules for how to enter data, such as always using “X” in base dimensions and using the same yes/no format, so that to make the dataset more reliable and easier to compare.

## 6. AI Disclaimer:
Took help from AI in standardizing the base dimension column to get the desired output.
