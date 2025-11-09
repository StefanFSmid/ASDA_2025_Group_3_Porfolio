## 0. Authors of the report

| Name                          |               Contribution                |
|:------------------------------|:-----------------------------------------:|
|                               |                       |
|                        ||
|              |                                           |
|   |                                           |
|  |                                           |



## 1. Dataset Overview (of the clean version)

| Item                                                   |                                                           Description                                                            |
|:-------------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------:|
| Dataset name                                           |                                                Airbnb Europe _(adapted dataset)_                                                 |
| Number of rows                                         |                                             51707 _(adapted dataset after cleaning)_                                             |
| Number of columns                                      |                                              21 _(adapted dataset after cleaning)_                                               |
| Format file (.csv, .txt, etc)                          |                                             .csv _(adapted dataset after cleaning)_                                              |
| Authors of the dataset                                 |                                        Kristóf Gyódi, Łukasz Nawaro _(original datasets)_                                        |
| Source (name)                                          | Determinants of Airbnb prices in European cities: A spatial econometrics approach (Supplementary Material) _(original datasets)_ |
| Source (link)                                          |     https://docs.google.com/spreadsheets/d/1ecopK6oyyb4d_7-QLrCr8YlgFrCetHU7-VQfnYej7JY/edit?usp=sharing _(adapted dataset)_     |


## 2. Dataset Structure (of the clean version) (STEFAN SMID)

| Feature/Variable   | Data type   | Description                                         |   Unique values | Examples                                        |
|:-------------------|:------------|:----------------------------------------------------|----------------:|:------------------------------------------------|
| base dimensions    | object      | Dimensions of the piece in studs (e.g., 2x4, 1x2)   |              12 | 2x2, 2x2, 2x2, 1x2, 1x2                         |
| base shape         | object      | Shape of the base (e.g., Rectangle, Square, Circle) |               5 | Rectangle, Circle, Square, Rectangle, Rectangle |
| color              | object      | Name of the Lego color                              |              62 | grey, orange, black, brickred, green            |
| has slope?         | object      | Indicates if the piece has a slope (Yes/No)         |               2 | No, No, No, No, No                              |
| is duplo?          | object      | Indicates whether the piece is Duplo or not         |               2 | No, No, No, No, No                              |
| number of studs    | float64     | Total number of studs on the top surface            |              10 | 4.0, 12.0, 2.0, 2.0, 2.0                        |
| size type          | object      | Type of Lego piece (e.g., Brick, Plate)             |               2 | Brick, Plate, Plate, Brick, Brick               |
| slope degree       | float64     | Angle of the slope in degrees (0 if none)           |               4 | 0.0, 0.0, 0.0, 0.0, 0.0                         |
| in stock           | int64       | Availability of the part in stock                   |               3 | 1, 1, 3, 1, 1                                   |


## 3. Descriptive statistics (of the clean version)

### Numeric Columns

|  | price | person\_capacity | cleanliness\_rating | guest\_satisfaction\_overall | bedrooms | citycenter\_dist | metro\_dist | attr\_index | attr\_index\_norm | rest\_index | rest\_index\_norm | lng | lat |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| count | 51707.0 | 51707.0 | 51707.0 | 51707.0 | 51707.0 | 51707.0 | 51707.0 | 51707.0 | 51707.0 | 51707.0 | 51707.0 | 51707.0 | 51707.0 |
| mean | 279.88 | 3.16 | 9.39 | 92.63 | 1.16 | 3.19 | 0.68 | 294.2 | 13.42 | 626.86 | 22.79 | 7.43 | 45.67 |
| std | 327.95 | 1.3 | 0.95 | 8.95 | 0.63 | 2.39 | 0.86 | 224.75 | 9.81 | 497.92 | 17.8 | 9.8 | 5.25 |
| min | 34.78 | 2.0 | 2.0 | 20.0 | 0.0 | 0.02 | 0.0 | 15.15 | 0.93 | 19.58 | 0.59 | -9.23 | 37.95 |
| 25% | 148.75 | 2.0 | 9.0 | 90.0 | 1.0 | 1.45 | 0.25 | 136.8 | 6.38 | 250.85 | 8.75 | -0.07 | 41.4 |
| 50% | 211.34 | 3.0 | 10.0 | 95.0 | 1.0 | 2.61 | 0.41 | 234.33 | 11.47 | 522.05 | 17.54 | 4.87 | 47.51 |
| 75% | 319.69 | 4.0 | 10.0 | 99.0 | 1.0 | 4.26 | 0.74 | 385.76 | 17.42 | 832.63 | 32.96 | 13.52 | 51.47 |
| max | 18545.45 | 6.0 | 10.0 | 100.0 | 10.0 | 25.28 | 14.27 | 4513.56 | 100.0 | 6696.16 | 100.0 | 23.79 | 52.64 |

### Categorical / Object Columns

merged_airbnbdf.select_dtypes(include=['object'])