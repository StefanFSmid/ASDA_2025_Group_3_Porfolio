import marimo

__generated_with = "0.19.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    import scipy
    import plotly
    import plotly.express as px
    return mo, np, pd, px


@app.cell
def _(pd):
    url = 'https://docs.google.com/spreadsheets/d/1ecopK6oyyb4d_7-QLrCr8YlgFrCetHU7-VQfnYej7JY/export?format=xlsx'
    airbnb = pd.ExcelFile(url)

    airbnb.sheet_names
    return (airbnb,)


@app.cell
def _(airbnb, pd):
    airbnbdf= pd.read_excel(airbnb, sheet_name='amsterdam_weekdays')
    print(airbnbdf.head())
    print(airbnbdf.shape)
    return


@app.cell
def _(airbnb, pd):
    # Merge all sheets into one df
    merged_airbnbdf = pd.concat(
        [airbnb.parse(sheet).assign(sheet_name=sheet) for sheet in airbnb.sheet_names],
        ignore_index=True
    )

    merged_airbnbdf.reset_index(drop=True, inplace=True)

    merged_airbnbdf.head(), merged_airbnbdf.shape
    return (merged_airbnbdf,)


@app.cell
def _(merged_airbnbdf):
    # Split the sheet_name column into city name
    merged_airbnbdf['city'] = merged_airbnbdf['sheet_name'].str.split('_').str[0].str.capitalize()

    # Define a mapping of city to country
    city_to_country = {
        'Amsterdam': 'Netherlands',
        'Athens': 'Greece',
        'Berlin': 'Germany',
        'Barcelona': 'Spain',
        'Budapest': 'Hungary',
        'Lisbon': 'Portugal',
        'London': 'United Kingdom',
        'Paris': 'France',
        'Rome': 'Italy',
        'Vienna': 'Austria'
    }

    # Map city to country
    merged_airbnbdf['country'] = merged_airbnbdf['city'].map(city_to_country)

    # Extract day type from sheet_name
    merged_airbnbdf['day_type'] = merged_airbnbdf['sheet_name'].str.split('_').str[1].str.capitalize()


    # Print the updated DataFrame
    print(merged_airbnbdf.head())
    print(merged_airbnbdf.shape)


    return


@app.cell
def _(merged_airbnbdf):
    # Change column name 'realSum' to 'Price' and print columns
    merged_airbnbdf.rename(columns={'realSum': 'Price'}, inplace=True)
    print(merged_airbnbdf.columns)
    return


@app.cell
def _(merged_airbnbdf):
    # Drop the 'Unnamed: 0' column
    merged_airbnbdf.drop('Unnamed: 0', axis=1, inplace=True)
    print(merged_airbnbdf.columns)
    return


@app.cell
def _(merged_airbnbdf):
    # Create a NEW dataframe (do not modify merged_airbnbdf in-place)
    merged_airbnbdf2 = merged_airbnbdf.copy()

    # Initialize the new column
    merged_airbnbdf2["room_category"] = "Other"

    # Fill conditionally
    merged_airbnbdf2.loc[
        merged_airbnbdf2["room_private"] == True, "room_category"
    ] = "Private"

    merged_airbnbdf2.loc[
        merged_airbnbdf2["room_shared"] == True, "room_category"
    ] = "Shared"

    # Drop the 3rd and 4th columns (index 2 and 3)
    merged_airbnbdf2 = merged_airbnbdf2.drop(
        merged_airbnbdf2.columns[[2, 3]], axis=1
    )

    # Move 'room_category' to 3rd position
    cols = list(merged_airbnbdf2.columns)
    cols.insert(2, cols.pop(cols.index("room_category")))
    merged_airbnbdf2 = merged_airbnbdf2[cols]

    # Display results 
    merged_airbnbdf2.head(), merged_airbnbdf2.shape, merged_airbnbdf2.columns

    return (merged_airbnbdf2,)


@app.cell
def _(merged_airbnbdf2, np):
    merged_airbnbdf3 = merged_airbnbdf2.copy()

    # Create 'listings by host' based on 'multi' and 'biz'
    merged_airbnbdf3["listings by host"] = np.select(
        [
            (merged_airbnbdf3["multi"] == 0) & (merged_airbnbdf3["biz"] == 0),
            merged_airbnbdf3["multi"] == 1,
            merged_airbnbdf3["biz"] == 1,
        ],
        ["1", "2-4", "4+"],
        default="Unknown",
    )

    # Drop the 5th and 6th columns (index 5 and 6)
    merged_airbnbdf3 = merged_airbnbdf3.drop(
        merged_airbnbdf3.columns[[5, 6]], axis=1
    )

    # Move 'listings by host' to 5th position (use a NEW helper variable name)
    cols3 = list(merged_airbnbdf3.columns)
    cols3.insert(5, cols3.pop(cols3.index("listings by host")))
    merged_airbnbdf3 = merged_airbnbdf3[cols3]

    # Display results
    merged_airbnbdf3.head(), merged_airbnbdf3.shape, merged_airbnbdf3.columns
    return (merged_airbnbdf3,)


@app.cell
def _(merged_airbnbdf3):
    merged_airbnbdf4 = merged_airbnbdf3.copy()

    # Reorder key columns (use a NEW helper variable name)
    cols4 = list(merged_airbnbdf4.columns)

    cols4.insert(0, cols4.pop(cols4.index("sheet_name")))
    cols4.insert(1, cols4.pop(cols4.index("country")))
    cols4.insert(2, cols4.pop(cols4.index("city")))
    cols4.insert(3, cols4.pop(cols4.index("day_type")))

    merged_airbnbdf4 = merged_airbnbdf4[cols4]

    # Rename a single column (do NOT use inplace in marimo)
    merged_airbnbdf4 = merged_airbnbdf4.rename(
        columns={"dist": "citycenter_dist"}
    )

    # Standardize all column names
    merged_airbnbdf4.columns = (
        merged_airbnbdf4.columns
        .str.lower()
        .str.replace(" ", "_")
    )

    # Display results
    merged_airbnbdf4.head(), merged_airbnbdf4.shape, merged_airbnbdf4.columns
    return (merged_airbnbdf4,)


@app.cell
def _(merged_airbnbdf4):
    df=merged_airbnbdf4
    return (df,)


@app.cell
def _(df):
    df
    return


@app.cell
def _(df):
    #Q1. How many listings are in each city in total and also per type of day?
    #listing per city
    listing_per_city=df.groupby(['city']).size()
    listing_per_city.to_frame(name='Total listings per city')
    return


@app.cell
def _(df, mo):
    day = mo.ui.dropdown(
        options=["All"] + sorted(df["day_type"].dropna().unique().tolist()),
        value="All",
        label="Day type"
    )

    mo.hstack([day])

    return (day,)


@app.cell
def _(day, df, px):
    df_view = df if day.value == "All" else df[df["day_type"] == day.value]

    counts = (
        df_view.groupby("city")
        .size()
        .reset_index(name="listings")
        .sort_values("listings", ascending=False)
    )

    fig = px.bar(counts, x="city", y="listings", title="Listings per city")
    fig
    return


if __name__ == "__main__":
    app.run()
