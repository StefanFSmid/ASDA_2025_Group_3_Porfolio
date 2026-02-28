import marimo

__generated_with = "0.20.2"
app = marimo.App(width="medium", auto_download=["html"])


@app.cell
def _():
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import tabulate
    import math
    import numpy as np
    from sklearn.model_selection import train_test_split
    from scipy.stats import chi2_contingency
    from scipy.stats import ttest_ind
    import pingouin as pg
    import statsmodels.api as sm
    import statsmodels.formula.api as smf
    from sklearn.metrics import confusion_matrix, classification_report
    from sklearn.metrics import roc_curve, roc_auc_score
    import warnings
    warnings.filterwarnings(action='ignore')
    from sklearn.metrics import roc_curve, roc_auc_score, confusion_matrix
    pd.set_option('display.max_columns', None)
    plt.rcParams["figure.figsize"] = (15, 8)
    return np, pd, plt, sns, tabulate


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Load Data Set
    """)
    return


@app.cell
def _(pd):

    username = "StefanFSmid"
    repository = "ASDA_2025_Group_3_Porfolio"
    directory = "48-hour-exam/group_3_faa_data_subset/group_3_faa_data_subset/faa_data_subset.xlsx"

    github_url = f"https://raw.githubusercontent.com/{username}/{repository}/master/{directory}"
    df = pd.read_excel(github_url)

    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Basic Data Inspection and Cleaning
    """)
    return


@app.cell
def _(df):
    #Checking the columns in the dataframe
    df.columns
    return


@app.cell
def _(df):
    # Display the shape of the dataframe
    df.shape
    return


@app.cell
def _(df):
    # Display the info of the dataframe
    df.info()
    return


@app.cell
def _(df):
    # Understanding the shape of the data.
    print('Total rows:',df.shape[0])
    print('Total columns:',df.shape[1])
    return


@app.cell
def _(df):
    # Display the first few rows of the dataframe
    df.head()
    return


@app.cell
def _(df):
    # Checking the categorical columns
    df.select_dtypes(include=object).head()
    return


@app.cell
def _(df, np):
    # Checking the numerical columns
    df.select_dtypes(include=np.number).head()
    return


@app.cell
def _(df):
    # Display the summary statistics of the dataframe
    df.describe().round(0)
    return


@app.cell
def _(df, pd, tabulate):
    # display missing values

    missing_values = df.isnull().sum()
    missing_values_percentage = (missing_values / len(df)) * 100
    missing_values_df = pd.DataFrame({'Missing Values': missing_values, 'Percentage': missing_values_percentage})
    missing_values_df = missing_values_df[missing_values_df['Missing Values'] > 0]
    missing_values_df = missing_values_df.sort_values(by='Missing Values', ascending=False)
    print(tabulate.tabulate(missing_values_df, headers='keys', tablefmt='psql'))

    return


@app.cell
def _(df):
    df.columns = (
        df.columns
          .str.replace('$', '', regex=False)
          .str.strip()
          .str.lower()
          .str.replace(':', '', regex=False)  
          .str.replace('(', '', regex=False)
          .str.replace(')', '', regex=False)
          .str.replace(' ', '_', regex=False)
    )

    # Print the cleaned column names
    print(df.columns)

    return


@app.cell
def _(df):
    #Check for duplicates
    df[df.duplicated()]
    duplicates = df.duplicated().sum()
    print(f"Number of duplicate rows: {duplicates}")
    return


@app.cell
def _(df):
    df["collision_date_and_time"].dtype
    return


@app.cell
def _(df):
    df.columns
    return


@app.cell
def _(df):
    df.head()
    return


@app.cell
def _(df):
    # Dropping unnecessary columns from the dataset
    cols_to_drop = [
        "airport_code",
        "airport_name",
        "origin_state",
        "origin_state_code",
        "country",
        "wildlife_species_id",
        "record_id",
        "wildlife_species",
        "wildlife_species_group",
        "wildlife_species_order",
        "effect_amount_of_damage_detailed",
        "effect_impact_to_flight",
        "cost_aircraft_time_out_of_service_hours",
        "cost_total",
        "days",
        "number_of_strikes"
    ]

    df1 = df.drop(columns=cols_to_drop)
    return (df1,)


@app.cell
def _(df1):
    df1
    return


@app.cell
def _(df1):
    # Checking the dataframe columns left
    df1.columns
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Reason for dropping the columns
    Identifiers (no predictive value)

    airport_code: unique airport identifier with no explanatory meaning.
    airport_name: descriptive airport label redundant with airport_code.
    record_id: unique incident identifier with zero analytical relevance.

    Geographic Detail (not central to research question & adds high dimensionality)

    origin_state: geographic category not directly related to operational/environmental mechanisms of damage.
    origin_state_code: coded version of origin_state with no additional explanatory value.
    country: near-constant geographic variable offering minimal variation in this dataset.

    Overly Granular Wildlife Taxonomy (risk of overfitting & poor interpretability)

    wildlife_species: highly detailed species variable creating excessive dummy variables.
    wildlife_species_group: intermediate taxonomy level still too granular for stable modeling.
    wildlife_species_order: higher taxonomy grouping duplicating information captured by broader categories.
    wildlife_species_id: coded species identifier with no independent predictive meaning.

    Post-Outcome / Target Leakage Variables (occur after damage)

    effect_amount_of_damage_detailed: describes severity after damage occurs, causing leakage.
    effect_impact_to_flight: consequence of damage rather than a cause, leading to leakage bias.

    Economic Consequence Variables (not relevant to damage probability)

    cost_aircraft_time_out_of_service_hours: reflects post-incident operational impact, not damage likelihood.
    cost_total: financial outcome variable unrelated to modeling physical damage occurrence.
    days: duration of impact after incident, not a causal predictor of damage.

    number_of_strikes: removed due to zero variance (all observations equal to 1), providing no explanatory power.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exploratory Data Analysis
    """)
    return


@app.cell
def _(df1):
    # Create binary target
    df1["damage_flag"] = (df1["effect_indicated_damage"] == "Caused damage").astype(int)

    # Class balance
    df1["damage_flag"].value_counts()
    df1["damage_flag"].value_counts(normalize=True)
    return


@app.cell
def _(df1):
    # Create month variable
    df1["month"] = df1["collision_date_and_time"].dt.month
    return


@app.cell
def _(df1):
    # Numeric Variables
    # Summary Statistics
    num_cols = [
        "aircraft_number_of_engines",
        "feet_above_ground",
        "miles_from_airport"
    ]

    df1[num_cols].describe()
    return (num_cols,)


@app.cell
def _(df1, num_cols, plt, sns):
    # Distribution Plots (Check Skewness)
    for col_iter1 in num_cols:
        plt.figure(figsize=(6,4))
        sns.histplot(df1[col_iter1], bins=40)
        plt.title(f"Distribution of {col_iter1}")
        plt.tight_layout()
        plt.show()
    return


@app.cell
def _(df1, num_cols, plt, sns):
    # Numeric Variables vs Damage
    for col_iter2 in num_cols:
        plt.figure(figsize=(6,4))
        sns.boxplot(data=df1, x="damage_flag", y=col_iter2)
        plt.title(f"{col_iter2} vs Damage")
    
        if col_iter2 in ["feet_above_ground", "miles_from_airport"]:
            plt.yscale("log")
    
        plt.tight_layout()
        plt.show()
    return


@app.cell
def _(df1, plt):
    # Categorical Variables: Damage Rate by Categorical Variables
    cat_cols = [
        "aircraft_type",
        "when_phase_of_flight",
        "when_time_of_day",
        "wildlife_animal_category",
        "month"
    ]

    for col_iter3 in cat_cols:
        plt.figure(figsize=(6,4))
    
        damage_rates = (
            df1.groupby(col_iter3)["damage_flag"]
              .mean()
              .sort_values(ascending=False)
        )
    
        damage_rates.plot(kind="bar")
        plt.title(f"Damage Probability by {col_iter3}")
        plt.ylabel("Damage Rate")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    return


@app.cell
def _(df1, pd, plt):
    # Phase of Flight — Stacked Percentage Plot
    phase_damage = (
        pd.crosstab(
            df1["when_phase_of_flight"],
            df1["damage_flag"],
            normalize="index"
        ) * 100
    )

    phase_damage = phase_damage.sort_values(by=1, ascending=False)

    ax = phase_damage.plot(kind="bar", stacked=True, figsize=(7,5))
    ax.set_title("Damage Probability by Phase of Flight")
    ax.set_ylabel("Percentage (%)")
    ax.set_xlabel("Phase of Flight")
    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(df1, num_cols, plt, sns):
    # Correlation Check (Numeric Only)
    plt.figure(figsize=(6,5))
    sns.heatmap(df1[num_cols].corr(), annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Matrix of Numeric Predictors")
    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(df1):
    df1.columns.tolist()
    return


@app.cell
def _(df1, pd, plt):
    # Aircraft type vs damage
    pd.crosstab(
        df1['aircraft_type'],
        df1['effect_indicated_damage'],
        normalize='index'
    ).plot(kind='bar', stacked=True)

    plt.title("Damage Rate by Aircraft Type")
    plt.ylabel("Proportion")
    plt.xlabel("Aircraft Type")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Category: Operational factor

    A normalized cross-tabulation between aircraft type and indicated damage was plotted using a stacked bar chart, showing the proportion of damage outcomes within each aircraft category. This approach allows comparison of damage likelihood conditional on aircraft type rather than raw incident counts. The results indicate that airplanes experience a lower proportion of damage outcomes, whereas helicopters show a relatively higher damage rate during wildlife strikes. This suggests aircraft design and operational characteristics may influence strike severity. These findings provide preliminary evidence supporting the role of operational factors in wildlife strike damage risk.
    """)
    return


@app.cell
def _(df1, pd, plt, sns):
    # Damage Probability by Animal Category
    ct = pd.crosstab(
        df1['wildlife_animal_category'],
        df1['effect_indicated_damage'],
        normalize='index'
    )

    sns.heatmap(ct, annot=True, cmap="Blues")
    plt.title("Damage Probability by Animal Category")
    plt.xlabel("Damage Level")
    plt.ylabel("Animal Category")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Category: Environmental factor

    This plot shows the relationship between wildlife animal category and whether a strike caused damage. A normalized cross-tab was used and visualized as a heatmap, meaning each row represents the probability of damage within that animal category. The results indicate that terrestrial mammals have the highest likelihood of causing damage, birds show moderate damage probability, while bats and reptiles rarely lead to damage. This suggests that the type of wildlife involved is an important environmental factor influencing strike severity. These insights help explain differences in damage risk across wildlife categories.
    """)
    return


@app.cell
def _(df1, plt, sns):
    # Number of engines vs damage
    sns.countplot(
        data=df1,
        x='aircraft_number_of_engines',
        hue='effect_indicated_damage'
    )

    plt.title("Damage vs Number of Engines")
    plt.xlabel("Number of Engines")
    plt.ylabel("Count")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Category: Operational factor

    This plot examines how the number of aircraft engines relates to damage occurrence during wildlife strikes. A count plot was used to compare the frequency of damage vs no damage across different engine counts. The results show that most incidents involve aircraft with two engines, which is expected due to their higher presence in the dataset, but damage still occurs across all engine categories. Aircraft with fewer engines appear to have a slightly higher proportion of damage cases, suggesting engine configuration may influence vulnerability. Overall, the number of engines is a relevant operational characteristic contributing to damage risk.
    """)
    return


@app.cell
def _(df1):
    # Checking null values again
    df1.isnull().sum()/len(df1)*100
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Intermediate break as next section is t5he model building and thus will be continued lateron
    """)
    return


if __name__ == "__main__":
    app.run()
