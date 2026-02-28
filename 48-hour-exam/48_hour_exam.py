import marimo

__generated_with = "0.20.2"
app = marimo.App(width="medium", auto_download=["html"])


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import tabulate
    import math
    import numpy as np
    import pingouin as pg
    from scipy.stats import chi2_contingency
    import statsmodels.api as sm
    import statsmodels.formula.api as smf
    from sklearn.metrics import roc_curve, roc_auc_score

    return (
        chi2_contingency,
        mo,
        np,
        pd,
        plt,
        roc_auc_score,
        roc_curve,
        sm,
        smf,
        sns,
        tabulate,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Load Data Set
    """)
    return


@app.cell
def _(pd):
    #from github
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
    # Display the first few rows of the dataframe
    df.head()
    return


@app.cell
def _(df):
    # Checking the categorical columns
    df.select_dtypes(include=["object", "string"]).head()
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

    return missing_values, missing_values_df, missing_values_percentage


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
    duplicates = df.duplicated().sum()
    print(f"Number of duplicate rows: {duplicates}")
    return


@app.cell
def _(df):
    # Create month column from the date column
    df["month"] = df["collision_date_and_time"].dt.month
    return


@app.cell
def _(df):
    num_cols = [
        "aircraft_number_of_engines",
        "feet_above_ground",
        "miles_from_airport"
    ]

    df[num_cols].describe().round(2)
    return (num_cols,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Basic Plots
    """)
    return


@app.cell
def _(df, plt, sns):
    sns.countplot(data=df, x="effect_indicated_damage")
    plt.title("Distribution of Damage Occurrence")
    plt.xticks(rotation=20)
    plt.show()
    return


@app.cell
def _(df, np, plt, sns):
    fig1, axes1 = plt.subplots(1, 2, figsize=(12, 4))

    # Left: All costs (including zeros)
    sns.histplot(df["cost_total"], bins=50, ax=axes1[0])
    axes1[0].set_title("Total Cost (Including Zeros)")
    axes1[0].set_xlabel("Cost")

    # Right: Log-transformed positive costs
    log_positive_costs = np.log10(df.loc[df["cost_total"] > 0, "cost_total"])

    sns.histplot(log_positive_costs, bins=40, ax=axes1[1])
    axes1[1].set_title("Log10 Positive Costs")
    axes1[1].set_xlabel("log10(Cost)")

    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(df, num_cols, plt, sns):
    fig2, axes2 = plt.subplots(1, len(num_cols), figsize=(15, 4))

    for ax1, col1 in zip(axes2, num_cols):
        sns.histplot(df[col1], bins=40, ax=ax1)
        ax1.set_title(f"{col1}")
        ax1.set_xlabel("")
        ax1.set_ylabel("Count")

    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(df, np):
    # Apply Log-Transformation to Altitude
    df['Log_Altitude'] = np.log1p(df['feet_above_ground'])
    return


@app.cell
def _(df, plt, sns):
    # Damage flag
    tmp1 = df.copy()
    tmp1["damage_flag"] = (tmp1["effect_indicated_damage"] == "Caused damage").astype(int)

    # Damage rate by month
    damage_by_month = (
        tmp1.groupby("month")["damage_flag"]
           .mean()
           .reindex(range(1, 13)) * 100
    )

    fig3, axes3 = plt.subplots(1, 2, figsize=(14, 5))

    # Frequency
    sns.countplot(data=df, x="month", order=range(1, 13), ax=axes3[0])
    axes3[0].set_title("Strike Frequency by Month")
    axes3[0].set_xlabel("Month")
    axes3[0].set_ylabel("Number of Strikes")
    axes3[0].set_xticks(range(0, 12))
    axes3[0].set_xticklabels(range(1, 13))

    # Damage rate
    axes3[1].bar(damage_by_month.index, damage_by_month.values)
    axes3[1].set_title("Damage Rate by Month")
    axes3[1].set_xlabel("Month")
    axes3[1].set_ylabel("Damage Rate (%)")
    axes3[1].set_xticks(range(1, 13))

    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(df, plt, sns):
    # Order by frequency
    time_order1 = df["when_time_of_day"].dropna().value_counts().index

    # Damage flag
    tmp2 = df.copy()
    tmp2["damage_flag"] = (tmp2["effect_indicated_damage"] == "Caused damage").astype(int)

    damage_by_time1 = (
        tmp2.groupby("when_time_of_day")["damage_flag"]
           .mean()
           .loc[time_order1] * 100
    )

    fig4, axes4 = plt.subplots(1, 2, figsize=(14, 5))

    # Frequency
    sns.countplot(data=df, x="when_time_of_day", order=time_order1, ax=axes4[0])
    axes4[0].set_title("Strike Frequency by Time of Day")
    axes4[0].set_ylabel("Strikes")
    axes4[0].tick_params(axis="x", rotation=25)

    # Damage rate
    axes4[1].bar(damage_by_time1.index.astype(str), damage_by_time1.values)
    axes4[1].set_title("Damage Rate by Time of Day")
    axes4[1].set_ylabel("Damage rate (%)")
    axes4[1].tick_params(axis="x", rotation=25)

    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(df, plt, sns):
    # Damage flag
    tmp3 = df.copy()
    tmp3["damage_flag"] = (tmp3["effect_indicated_damage"] == "Caused damage").astype(int)

    fig5, axes5 = plt.subplots(1, 2, figsize=(12, 5))

    # Top airports by strikes
    top_strikes1 = df["airport_name"].fillna("Unknown").value_counts().head(5)
    sns.barplot(x=top_strikes1.values, y=top_strikes1.index, ax=axes5[0])
    axes5[0].set_title("Top 5 Airports by Strikes")
    axes5[0].set_xlabel("Strikes")
    axes5[0].set_ylabel("")

    # Top airports by damage
    top_damage1 = (
        tmp3.groupby("airport_name")["damage_flag"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )
    sns.barplot(x=top_damage1.values, y=top_damage1.index, ax=axes5[1])
    axes5[1].set_title("Top 5 Airports by Damage")
    axes5[1].set_xlabel("Damaging Strikes")
    axes5[1].set_ylabel("")

    plt.tight_layout()
    plt.show()
    return (tmp3,)


@app.cell
def _(df, plt, sns, tmp3):
    fig6, axes6 = plt.subplots(1, 2, figsize=(12, 5))

    # Top states by strikes
    top_strikes2 = df["origin_state"].fillna("Unknown").value_counts().head(5)
    sns.barplot(x=top_strikes2.values, y=top_strikes2.index, ax=axes6[0])
    axes6[0].set_title("Top 5 States by Strikes")
    axes6[0].set_xlabel("Strikes")
    axes6[0].set_ylabel("")

    # Top states by damage
    top_damage2 = (
        tmp3.groupby("origin_state")["damage_flag"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )
    sns.barplot(x=top_damage2.values, y=top_damage2.index, ax=axes6[1])
    axes6[1].set_title("Top 5 States by Damage")
    axes6[1].set_xlabel("Damaging Strikes")
    axes6[1].set_ylabel("")

    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(df, plt, sns):
    # Create damage flag
    tmp4 = df.copy()
    tmp4["damage_flag"] = (tmp4["effect_indicated_damage"] == "Caused damage").astype(int)

    # Order by frequency (for consistency)
    order = df["aircraft_type"].value_counts().index

    # Damage percentage by aircraft type
    damage_pct = (
        tmp4.groupby("aircraft_type")["damage_flag"]
           .mean()
           .reindex(order) * 100
    )

    fig7, axes7 = plt.subplots(1, 2, figsize=(14, 5))

    # Left — Distribution
    sns.countplot(data=df, x="aircraft_type", order=order, ax=axes7[0])
    axes7[0].set_title("Aircraft Type Distribution")
    axes7[0].set_ylabel("Number of Strikes")
    axes7[0].set_xlabel("")
    axes7[0].tick_params(axis="x", rotation=25)

    # Right — Damage %
    sns.barplot(x=damage_pct.index, y=damage_pct.values, ax=axes7[1])
    axes7[1].set_title("Damage Rate by Aircraft Type")
    axes7[1].set_ylabel("Damage Rate (%)")
    axes7[1].set_xlabel("")
    axes7[1].tick_params(axis="x", rotation=25)

    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(df, plt, sns):
    # Create damage flag
    tmp5 = df.copy()
    tmp5["damage_flag"] = (tmp5["effect_indicated_damage"] == "Caused damage").astype(int)

    # Order categories by frequency
    cat_order1 = df["wildlife_animal_category"].value_counts().index

    # Damage rate within each category (%)
    cat_damage_rate1 = (
        tmp5.groupby("wildlife_animal_category")["damage_flag"]
        .mean()
        .reindex(cat_order1) * 100
    )

    # Plot
    fig8, axes8 = plt.subplots(1, 2, figsize=(14, 5))

    # Left — Frequency
    sns.countplot(
        data=df,
        x="wildlife_animal_category",
        order=cat_order1,
        ax=axes8[0]
    )
    axes8[0].set_title("Animal Categories (Strikes)")
    axes8[0].set_ylabel("Strikes")
    axes8[0].set_xlabel("")
    axes8[0].tick_params(axis="x", rotation=45)

    # Right — Damage rate within category
    sns.barplot(
        x=cat_damage_rate1.index,
        y=cat_damage_rate1.values,
        ax=axes8[1]
    )
    axes8[1].set_title("Animal Categories (Damage Rate)")
    axes8[1].set_ylabel("Damage Rate (%)")
    axes8[1].set_xlabel("")
    axes8[1].tick_params(axis="x", rotation=45)

    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(df, plt, sns):
    tmp6 = df.copy()
    tmp6["damage_flag"] = (tmp6["effect_indicated_damage"] == "Caused damage").astype(int)

    # Top 5 species by strikes
    top_species_strikes = (
        df["wildlife_species"]
        .fillna("Unknown")
        .value_counts()
        .head(5)
    )

    # Top 5 species by damage
    top_species_damage = (
        tmp6.groupby("wildlife_species")["damage_flag"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )

    fig9, axes9 = plt.subplots(1, 2, figsize=(12, 5))

    # Left — Strikes
    sns.barplot(x=top_species_strikes.index, y=top_species_strikes.values, ax=axes9[0])
    axes9[0].set_title("Top 5 Species (Strikes)")
    axes9[0].set_ylabel("Strikes")
    axes9[0].set_xlabel("")
    axes9[0].tick_params(axis="x", rotation=45)

    # Right — Damage
    sns.barplot(x=top_species_damage.index, y=top_species_damage.values, ax=axes9[1])
    axes9[1].set_title("Top 5 Species (Damaging Strikes)")
    axes9[1].set_ylabel("Damaging strikes")
    axes9[1].set_xlabel("")
    axes9[1].tick_params(axis="x", rotation=45)

    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(df, pd, plt):
    phase_damage = (
        pd.crosstab(
            df["when_phase_of_flight"],
            df["effect_indicated_damage"],
            normalize="index"
        ) * 100
    )

    # Sort by "Caused damage" if present; otherwise sort by first column
    sort_col = "Caused damage" if "Caused damage" in phase_damage.columns else phase_damage.columns[0]
    phase_damage = phase_damage.sort_values(by=sort_col, ascending=False)

    ax2 = phase_damage.plot(kind="bar", stacked=True, figsize=(12, 6))
    ax2.set_title("Probability of Damage by Phase of Flight")
    ax2.set_ylabel("Percentage of Incidents (%)")
    ax2.set_xlabel("Phase of Flight")
    ax2.legend(title="Outcome", bbox_to_anchor=(1.02, 1), loc="upper left")

    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(df, num_cols, plt, sns):
    fig10, axes10 = plt.subplots(1, len(num_cols), figsize=(15, 4))

    titles = {
        "aircraft_number_of_engines": "Aircraft Engines vs Damage",
        "feet_above_ground": "Altitude vs Damage",
        "miles_from_airport": "Distance from Airport vs Damage"
    }

    for ax3, col3 in zip(axes10, num_cols):
        sns.boxplot(data=df, x="effect_indicated_damage", y=col3, ax=ax3)
        ax3.set_title(titles[col3])
        ax3.set_xlabel("")
        ax3.tick_params(axis="x", rotation=25)
    
        # Log scale for skewed variables
        if col3 in ["feet_above_ground", "miles_from_airport"]:
            ax3.set_yscale("log")

    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(df):
    # Dropping unnecessary columns from the dataset for modeling
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Reasons for droppoing columns in df1

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


@app.cell
def _(df1):
    df1
    return


@app.cell
def _(
    df1,
    missing_values,
    missing_values_df,
    missing_values_percentage,
    pd,
    tabulate,
):
    # display missing values on the cleaned dataframe

    missing_values1 = df1.isnull().sum()
    missing_values_percentage1 = (missing_values / len(df1)) * 100
    missing_values_df1 = pd.DataFrame({'Missing Values': missing_values, 'Percentage': missing_values_percentage})
    missing_values_df1 = missing_values_df[missing_values_df['Missing Values'] > 0]
    missing_values_df1 = missing_values_df.sort_values(by='Missing Values', ascending=False)
    print(tabulate.tabulate(missing_values_df, headers='keys', tablefmt='psql'))

    return


@app.cell
def _(df1):
    # Create binary target
    df1["damage_flag"] = (df1["effect_indicated_damage"] == "Caused damage").astype(int)

    # Class balance
    df1["damage_flag"].value_counts()
    df1["damage_flag"].value_counts(normalize=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exploring missingness of miles_from_airport column
    """)
    return


@app.cell
def _(df1):
    df1["miles_missing"] = df1["miles_from_airport"].isna().astype(int)
    df1.groupby("miles_missing")["damage_flag"].mean()
    return


@app.cell
def _(chi2_contingency, df1, pd):
    ct_1 = pd.crosstab(df1["miles_missing"], df1["damage_flag"])
    chi2_1, p_1, dof_1, expected_1 = chi2_contingency(ct_1)

    print("Contingency Table:\n", ct_1)
    print("\nChi-square =", chi2_1)
    print("p-value =", p_1)
    return


@app.cell
def _(df1):
    cont_cols = [
        "Log_Altitude",
        "miles_from_airport",
        "aircraft_number_of_engines"
    ]

    corr_spearman = df1[cont_cols].corr(method="spearman")
    corr_spearman
    return (corr_spearman,)


@app.cell
def _(corr_spearman, plt, sns):
    plt.figure(figsize=(6,5))

    sns.heatmap(
        corr_spearman, 
        annot=True,         
        cmap="coolwarm", 
        vmin=-1, vmax=1, 
        linewidths=0.5, 
        square=True, 
        fmt=".2f"          
    )

    plt.title("Spearman Correlation Matrix (Continuous Predictors)", fontsize=14)
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The variable miles_from_airport was dropped because it had 30% missing values, and those missing values were strongly associated with damage outcomes, meaning keeping the variable would remove a large, biased portion of the dataset and distort the model.
    """)
    return


@app.cell
def _(df1):
    df_model1 = df1.drop(columns=["miles_from_airport"])
    return (df_model1,)


@app.cell
def _(chi2_contingency, df_model1, pd):
    cat_vars = [
        "when_time_of_day",
        "when_phase_of_flight",
        "aircraft_type",
        "wildlife_animal_category",
        "month"
    ]

    chi_results = []

    for var_1 in cat_vars:
        sub = df_model1[[var_1, "damage_flag"]].dropna()
        ct_2 = pd.crosstab(sub[var_1], sub["damage_flag"])

        # Need at least 2 categories
        if ct_2.shape[0] < 2:
            continue
    
        chi2_2, p_2, dof_2, expected_2 = chi2_contingency(ct_2)
        chi_results.append([var_1, sub.shape[0], chi2_2, p_2])

    chi_df = pd.DataFrame(chi_results, columns=["Variable", "N Used", "Chi2", "p-value"])
    chi_df.sort_values("p-value")
    return


@app.cell
def _(df_model1, np, pd, sm):
    def univariate_logit(df, x, y="damage_flag"):
        sub = df_model1[[x, y]].dropna()
        X = sm.add_constant(sub[x])
        model = sm.Logit(sub[y], X).fit(disp=False)
    
        coef = model.params[x]
        se = model.bse[x]
        p = model.pvalues[x]
        OR = np.exp(coef)
        CI_low, CI_high = np.exp(coef - 1.96*se), np.exp(coef + 1.96*se)
    
        return [x, sub.shape[0], OR, CI_low, CI_high, p]

    num_vars = ["Log_Altitude", "aircraft_number_of_engines"]

    uni_num_results = []

    for var in num_vars:
        try:
            uni_num_results.append(univariate_logit(df_model1, var))
        except Exception as e:
            print("Skipped", var, "because:", e)

    num_df = pd.DataFrame(
        uni_num_results, 
        columns=["Variable", "N Used", "Odds Ratio", "CI Low", "CI High", "p-value"]
    )

    num_df.sort_values("p-value")
    return


@app.cell
def _(df_model1):
    for col4 in ["when_phase_of_flight", "when_time_of_day", "wildlife_animal_category", "aircraft_type", "month"]:
        print("\n", col4)
        print(df_model1[col4].value_counts(dropna=False).head(20))
    return


@app.cell
def _(df_model1):
    major_phases = ["Approach", "Landing Roll", "Take-off run", "Climb", "Descent"]
    df_model1["when_phase_of_flight"] = df_model1["when_phase_of_flight"].fillna("Other")

    df_model1.loc[~df_model1["when_phase_of_flight"].isin(major_phases),
                 "when_phase_of_flight"] = "Other"


    df_model1["wildlife_animal_category"] = df_model1["wildlife_animal_category"].replace({
        "Bats": "Other Wildlife",
        "Reptiles": "Other Wildlife",
   
    })


    df_model1["aircraft_type"] = df_model1["aircraft_type"].fillna("Unknown")
    df_model1["when_time_of_day"] = df_model1["when_time_of_day"].fillna("Unknown")

    df_model1["season"] = df_model1["month"].replace({
        12:"Winter", 1:"Winter", 2:"Winter",
        3:"Spring", 4:"Spring", 5:"Spring",
        6:"Summer", 7:"Summer", 8:"Summer",
        9:"Fall", 10:"Fall", 11:"Fall"
    })
    return


@app.cell
def _(df_model1):
    for col5 in ["when_phase_of_flight", "when_time_of_day", "wildlife_animal_category", "aircraft_type", "season"]:
        print("\n", col5)
        print(df_model1[col5].value_counts(dropna=False).head(20))
    return


@app.cell
def _(df_model1):
    for col6 in ["when_phase_of_flight", "when_time_of_day", 
                "wildlife_animal_category", "aircraft_type", "season"]:
        print("\n\n====>", col6)
        print(df_model1.groupby(col6)["damage_flag"].agg(['count','sum','mean']))
    return


@app.cell
def _(df_model1):
    df_model2 = df_model1[df_model1["wildlife_animal_category"] != "Other Wildlife"]
    return (df_model2,)


@app.cell
def _(df_model2):
    for col7 in ["when_phase_of_flight", "when_time_of_day", 
                "wildlife_animal_category", "aircraft_type", "season"]:
        print("\n\n====>", col7)
        print(df_model2.groupby(col7)["damage_flag"].agg(['count','sum','mean']))
    return


@app.cell
def _(df_model2, sm, smf):
    formula = """
    damage_flag ~ 
        Log_Altitude +
        aircraft_number_of_engines +
        C(aircraft_type) +
        C(when_phase_of_flight) +
        C(when_time_of_day) +
        C(wildlife_animal_category) +
        C(season)
    """

    glm_model = smf.glm(
        formula=formula,
        data=df_model2,
        family=sm.families.Binomial()
    ).fit()

    print(glm_model.summary())
    return (glm_model,)


@app.cell
def _(glm_model, np, pd):
    # Extract basic values
    coef = glm_model.params
    stderr = glm_model.bse
    pvals = glm_model.pvalues
    conf = glm_model.conf_int()
    conf.columns = ['ci_lower', 'ci_upper']

    # Compute odds ratios + CI
    odds = np.exp(coef)
    odds_ci_lower = np.exp(conf['ci_lower'])
    odds_ci_upper = np.exp(conf['ci_upper'])

    # Identify "significant" predictors where CI does NOT cross 1
    significant = ~((odds_ci_lower <= 1) & (odds_ci_upper >= 1))

    # Combine into one table
    summary_table = pd.DataFrame({
        'Coefficient': coef,
        'Std_Error': stderr,
        'p_value': pvals,
        'CI_lower_coef': conf['ci_lower'],
        'CI_upper_coef': conf['ci_upper'],
        'Odds_Ratio': odds,
        'CI_lower_OR': odds_ci_lower,
        'CI_upper_OR': odds_ci_upper,
        'Significant (CI excludes 1)': significant
    })

    # Optional: round for nicer printing
    summary_table = summary_table.round(4)

    summary_table
    return (summary_table,)


@app.cell
def _(np, summary_table):
    # --- COPY MODEL SUMMARY TABLE ---
    df_imp = summary_table.copy()

    # --- Keep only significant predictors (CI excludes OR=1) ---
    df_imp = df_imp[df_imp["Significant (CI excludes 1)"]]

    # --- Remove intercept ---
    df_imp = df_imp[df_imp.index != "Intercept"]

    # --- Sort by effect size (largest |log(OR)| first) ---
    df_imp["Effect"] = np.abs(np.log(df_imp["Odds_Ratio"]))
    df_imp = df_imp.sort_values("Effect", ascending=False)

    # --- Split Feature and Value into columns ---
    feature_names = []
    value_names = []

    for name in df_imp.index:
        if "C(" in name:   
            # Example: C(season)[T.Winter] --> Feature="season", Value="Winter"
            feature = name.split("(")[1].split(")")[0]
            value = name.split("[T.")[1].replace("]", "")
        else:
            # Continuous predictors
            feature = name
            value = "Continuous"
    
        # Human-friendly names
        feature = (
            feature.replace("when_phase_of_flight", "Phase of Flight")
                   .replace("when_time_of_day", "Time of Day")
                   .replace("wildlife_animal_category", "Animal Category")
                   .replace("aircraft_type", "Aircraft Type")
                   .replace("season", "Season")
                   .replace("Log_Altitude", "Altitude")
                   .replace("aircraft_number_of_engines", "Number of Engines")
        )
    
        feature_names.append(feature)
        value_names.append(value)

    df_imp["Feature"] = feature_names
    df_imp["Value"] = value_names

    # --- Format p-values ---
    df_imp["p_value"] = df_imp["p_value"].apply(lambda p: "<0.001" if p < 0.001 else f"{p:.3f}")

    # --- Final clean table ---
    clean_table = df_imp[[
        "Feature", "Value", "Odds_Ratio", "CI_lower_OR", "CI_upper_OR", "p_value"
    ]].round(3)

    clean_table

    return


@app.cell
def _(np, pd, plt):
    # Build DataFrame
    df_forest = pd.DataFrame({
        "Factor": [
            'Terrestrial Mammals', 'Log(Altitude)', 'Takeoff Run', 'Climb', 'Descent',
            'Landing Roll', 'Winter', 'Spring', 'Summer', 'Number of Engines'
        ],
        "OR": np.array([6.55, 1.38, 2.78, 2.14, 2.02, 1.73, 1.49, 1.14, 0.69, 0.59]),
        "CI_L": np.array([5.20, 1.28, 2.35, 1.93, 1.77, 1.51, 1.30, 1.02, 0.62, 0.52]),
        "CI_U": np.array([8.10, 1.48, 3.29, 2.38, 2.30, 1.98, 1.72, 1.28, 0.77, 0.67])
    })

    # Compute effect size
    df_forest["Effect"] = np.abs(np.log(df_forest["OR"]))

    # Sort descending
    df_forest = df_forest.sort_values("Effect", ascending=False).reset_index(drop=True)

    # REVERSE ORDER for plotting (most important at top)
    factors = df_forest["Factor"][::-1]
    odds_ratios = df_forest["OR"][::-1]
    lower_ci = df_forest["CI_L"][::-1]
    upper_ci = df_forest["CI_U"][::-1]

    # Compute CI errors
    error_lower = odds_ratios - lower_ci
    error_upper = upper_ci - odds_ratios

    plt.figure(figsize=(10, 6))

    plt.errorbar(
        odds_ratios, factors,
        xerr=[error_lower, error_upper],
        fmt='o',
        color='black',
        markersize=7,
        ecolor='#d62728',
        capsize=4
    )

    plt.axvline(1, linestyle='--', color='gray', alpha=0.7)
    plt.xscale('log')

    plt.xlabel('Adjusted Odds Ratio (log scale)', fontsize=12)
    plt.title('Predictors of Physical Damage',
              fontsize=12, fontweight='normal')

    plt.grid(axis='x', linestyle=':', alpha=0.4)
    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(df_model2, glm_model):
    # Predictions & residuals
    df_model2["pred_prob"] = glm_model.predict(df_model2)
    df_model2["resid_deviance"] = glm_model.resid_deviance
    df_model2["resid_pearson"] = glm_model.resid_pearson
    df_model2["resid_working"] = glm_model.resid_working
    return


@app.cell
def _(df_model2):
    df_model2["pred_prob"].isna().sum()
    df_model2[df_model2["pred_prob"].isna()].head()
    return


@app.cell
def _(df_model2):
    df_roc = df_model2.dropna(subset=["pred_prob"])
    df_roc.shape
    return (df_roc,)


@app.cell
def _(df_roc, plt, roc_auc_score, roc_curve):
    fpr, tpr, _ = roc_curve(df_roc["damage_flag"], df_roc["pred_prob"])
    auc = roc_auc_score(df_roc["damage_flag"], df_roc["pred_prob"])

    plt.figure(figsize=(6,5))
    plt.plot(fpr, tpr, label=f"AUC = {auc:.3f}")
    plt.plot([0,1], [0,1], 'k--')
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve for GLM Model")
    plt.legend()
    plt.grid(True)
    plt.show()
    return


@app.cell
def _(df1, plt, sns):
    plt.figure(figsize=(7, 5)) 

    # Subsample to reduce overplotting
    sample_df = df1.sample(5000, random_state=42) if len(df1) > 5000 else df1

    sns.regplot(
        data=sample_df,
        x='feet_above_ground',
        y='damage_flag',
        logistic=True,
        scatter_kws={'alpha': 0.08, 's': 10, 'color': 'gray'},
        line_kws={'color': 'crimson', 'lw': 2.2}
    )

    plt.title('Risk Probability Curve', fontsize=13, fontweight='bold')
    plt.xlabel('Altitude (Feet Above Ground)', fontsize=11)
    plt.ylabel('Predicted Probability of Damage', fontsize=11)

    plt.xlim(0, 5000)

    # Tick label sizes
    plt.xticks(fontsize=9)
    plt.yticks(fontsize=9)

    plt.grid(alpha=0.25)
    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(df1, plt, sns):
    eng_rate = df1.groupby('aircraft_number_of_engines')['damage_flag'].mean().reset_index()

    plt.figure(figsize=(6,4))
    sns.barplot(data=eng_rate, x='aircraft_number_of_engines', y='damage_flag', color='steelblue')

    plt.xlabel('Number of Engines', fontsize=11)
    plt.ylabel('Damage Rate', fontsize=11)
    plt.title('Damage Rate by Number of Engines', fontsize=13)
    plt.ylim(0, eng_rate['damage_flag'].max() + 0.05)

    plt.grid(axis='y', alpha=0.25)
    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(df1, pd, plt):
    df1['Month'] = pd.to_datetime(df1['collision_date_and_time']).dt.month

    # Monthly Aggregation
    seasonal_data = df1.groupby('Month').agg(
        total_strikes=('Month', 'count'),
        damage_rate=('damage_flag', 'mean')
    ).reset_index()

    seasonal_data['damage_rate'] *= 100
    months = seasonal_data['Month']

    # Figure
    fig11, ax4 = plt.subplots(figsize=(10, 5))

    # Volume Bars (Soft Grey)
    ax4.bar(
        months,
        seasonal_data['total_strikes'],
       
        edgecolor='#9c9c9c', 
        linewidth=0.6,
        label='Total Strikes'
    )
    ax4.set_ylabel('Total Strikes', fontsize=11, color='#333333')
    ax4.set_xlabel('Month', fontsize=11)

    # Damage Rate Line (Clean Navy Blue)
    ax5 = ax4.twinx()
    ax5.plot(
        months,
        seasonal_data['damage_rate'],
        color='#1f4e79',   
        linewidth=2.3,
        marker='o',
        markersize=5,
        markerfacecolor='white',
        markeredgecolor='#1f4e79',
        label='Damage Rate (%)'
    )

    ax5.set_ylabel('Damage Rate (%)', fontsize=11, color='#1f4e79')
    ax5.tick_params(axis='y', labelcolor='#1f4e79')

    # Season Shading
    # Winter = Dec + Jan + Feb
    ax4.axvspan(11.5, 12.5, color='#d0e2f2', alpha=0.32)  # December
    ax4.axvspan(0.5,  2.5,  color='#d0e2f2', alpha=0.32)  # Jan–Feb

    # Spring = Mar–May
    ax4.axvspan(2.5, 5.5,  color='#ffe9c6', alpha=0.32)

    # Summer = Jun–Aug
    ax4.axvspan(5.5, 8.5,  color='#d4eed8', alpha=0.32)

    # Fall = Sep–Nov
    ax4.axvspan(8.5, 11.5, color='#f6dfcd', alpha=0.32)
    plt.title(
        'Seasonal Wildlife Strike Patterns: Strike Volume vs Damage Rate',
        fontsize=14,
        fontweight='normal',
        color='#333333'
    )

    plt.xticks(
        ticks=range(1, 13),
        labels=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
        fontsize=10
    )

    ax4.tick_params(axis='y', labelsize=10)
    ax5.tick_params(axis='y', labelsize=10)

    ax4.grid(axis='y', alpha=0.2)

    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(df, plt):
    # --- Order categories by strike frequency ---
    time_order2 = df["when_time_of_day"].dropna().value_counts().index

    # --- Create damage flag ---
    tmp7 = df.copy()
    tmp7["damage_flag"] = (tmp7["effect_indicated_damage"] == "Caused damage").astype(int)

    # --- Compute damage rate (%) ---
    damage_by_time2 = (
        tmp7.groupby("when_time_of_day")["damage_flag"]
           .mean()
           .loc[time_order2] * 100
    )

    strike_counts1 = df["when_time_of_day"].value_counts().loc[time_order2]

    # --- Dual-Axis Plot ---
    fig12, ax6 = plt.subplots(figsize=(8, 5))

    # Bars: Strike Frequency (Standard Blue)
    ax6.bar(
        time_order2,
        strike_counts1,
        edgecolor="#081f30",
        linewidth=0.5
    )
    ax6.set_ylabel("Strike Frequency", fontsize=10)
    ax6.set_xlabel("Time of Day", fontsize=10)

    # Line: Damage Rate (Darker Navy for contrast)
    ax7 = ax6.twinx()
    ax7.plot(
        time_order2,
        damage_by_time2.values,
        color="#2a5880", 
        linewidth=2.4,
        marker="o",
        markersize=6,
        markerfacecolor="white",
        markeredgecolor="#0b2c48"
    )
    ax7.set_ylabel("Damage Rate (%)", fontsize=10, color="#0b2c48")
    ax7.tick_params(axis="y", labelcolor="#0b2c48")
    # Formatting
    plt.title("Wildlife Strikes by Time of Day: Volume vs Damage Severity",
              fontsize=12, fontweight="normal", color="#333333")

    plt.xticks(rotation=25, fontsize=10)
    ax6.tick_params(axis="y", labelsize=10)
    ax7.tick_params(axis="y", labelsize=10)

    # Light grid on left axis
    ax6.grid(axis="y", alpha=0.20)

    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(df, plt):
    tmp8 = df.copy()
    tmp8["damage_flag"] = (tmp8["effect_indicated_damage"] == "Caused damage").astype(int)

    #  Order categories by strike frequency 
    cat_order2 = df["wildlife_animal_category"].value_counts().index

    # Compute damage rate (%) in same order
    cat_damage_rate2 = (
        tmp8.groupby("wildlife_animal_category")["damage_flag"]
           .mean()
           .reindex(cat_order2) * 100
    )

    strike_counts2 = df["wildlife_animal_category"].value_counts().reindex(cat_order2)

    # Dual-Axis Plot
    fig13, ax8 = plt.subplots(figsize=(8, 5))

    # Bars: Strike Frequency (Standard Blue)
    ax8.bar(
        cat_order2,
        strike_counts2,
        color="#1f77b4",
        edgecolor="#0f4a73",
        linewidth=0.5
    )
    ax8.set_ylabel("Strike Frequency", fontsize=10)
    ax8.set_xlabel("Animal Category", fontsize=10)

    # Line: Damage Rate
    ax9 = ax8.twinx()
    ax9.plot(
        cat_order2,
        cat_damage_rate2.values,
        color="#0b2c48",
        linewidth=2.4,
        marker="o",
        markersize=6,
        markerfacecolor="white",
        markeredgecolor="#0b2c48"
    )
    ax9.set_ylabel("Damage Rate (%)", fontsize=10, color="#0b2c48")
    ax9.tick_params(axis="y", labelcolor="#0b2c48")

    # Title
    plt.title(
        "Wildlife Strikes by Animal Category: Volume vs Damage Severity",
        fontsize=12,
        fontweight="normal",
        color="#333333"
    )

    # X-axis formatting
    plt.xticks(rotation=30, ha="right", fontsize=10)
    ax8.tick_params(axis="y", labelsize=10)
    ax9.tick_params(axis="y", labelsize=10)

    # Light grid
    ax8.grid(axis="y", alpha=0.2)

    plt.tight_layout()
    plt.show()
    return


if __name__ == "__main__":
    app.run()
