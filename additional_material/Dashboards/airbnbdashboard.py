import marimo

__generated_with = "0.19.5"
app = marimo.App(width="medium", auto_download=["html"])


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

    #airbnb.sheet_names
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

    #merged_airbnbdf.head(), merged_airbnbdf.shape
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
    #merged_airbnbdf2.head(), merged_airbnbdf2.shape, merged_airbnbdf2.columns
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
    #merged_airbnbdf3.head(), merged_airbnbdf3.shape, merged_airbnbdf3.columns
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
    #merged_airbnbdf4.head(), merged_airbnbdf4.shape, merged_airbnbdf4.columns
    return (merged_airbnbdf4,)


@app.cell
def _(merged_airbnbdf4):
    df=merged_airbnbdf4
    return (df,)


@app.cell
def _():
    #df
    return


@app.cell
def _(df):
    #Q1. How many listings are in each city in total and also per type of day?
    #listing per city
    listing_per_city=df.groupby(['city']).size()
    #listing_per_city.to_frame(name='Total listings per city')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **AirBnb Dashboard**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Listings per city by day type**
    """)
    return


@app.cell
def _(df, mo):
    day = mo.ui.dropdown(
        options=["All"] + sorted(df["day_type"].dropna().unique()),
        value="All",
        label="Day type",
    )

    day
    return (day,)


@app.cell
def _(day, df):
    df_view = df if day.value == "All" else df[df["day_type"] == day.value]

    counts = (
        df_view
        .groupby("city")
        .size()
        .reset_index(name="listings")
        .sort_values("listings", ascending=False)
    )
    return counts, df_view


@app.cell
def _(counts, day, px):
    px.bar(
        counts,
        x="city",
        y="listings",
        title=f"Listings per city ({day.value})",
        text="listings"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Superhost % by city**
    """)
    return


@app.cell
def _(df):
    superhost_city = (
        df.groupby("city")
        .agg(
            total_listings=("city", "size"),
            superhosts=("host_is_superhost", "sum"),
        )
        .assign(superhost_share=lambda t: t["superhosts"] / t["total_listings"])
        .sort_values("superhost_share", ascending=False)
        .reset_index()
    )
    return (superhost_city,)


@app.cell
def _(df, mo):
    city_sh = mo.ui.dropdown(
        options=sorted(df["city"].dropna().unique().tolist()),
        value=sorted(df["city"].dropna().unique().tolist())[0],
        label="Select city"
    )

    city_sh
    return (city_sh,)


@app.cell
def _(city_sh, df, mo):
    city_df = df[df["city"] == city_sh.value]

    total_listings_city = len(city_df)
    superhosts_city = int(city_df["host_is_superhost"].sum())
    share_city = (superhosts_city / total_listings_city) if total_listings_city else 0.0

    mo.hstack([
        mo.stat(value=city_sh.value, label="City"),
        mo.stat(value=superhosts_city, label="Superhost listings"),
        mo.stat(value=total_listings_city, label="Total listings"),
        mo.stat(value=f"{share_city:.1%}", label="Superhost proportion"),
    ])
    return


@app.cell
def _(px, superhost_city):
    fig = px.bar(
        superhost_city,
        x="city",
        y="superhost_share",
        title="Superhost proportion by city",
        hover_data=["superhosts", "total_listings"],
        text=superhost_city["superhost_share"].mul(100).round(1).astype(str) + "%",
    )

    fig.update_yaxes(tickformat=".0%")
    fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Listings per city by number of bedrooms**
    """)
    return


@app.cell
def _(df, mo):
    max_bed = int(df["bedrooms"].max())

    min_bedrooms = mo.ui.slider(
        start=0,
        stop=max_bed,
        step=1,
        value=4,
        label="Minimum bedrooms (>=)"
    )

    min_bedrooms
    return (min_bedrooms,)


@app.cell
def _(df, min_bedrooms):
    df_bed = df[df["bedrooms"] >= min_bedrooms.value]

    city_counts = (
        df_bed.groupby("city")
        .size()
        .reset_index(name="listings")
        .sort_values("listings", ascending=False)
    )
    return (city_counts,)


@app.cell
def _(city_counts, min_bedrooms, px):
    px.bar(
        city_counts,
        x="city",
        y="listings",
        title=f"Listings per city with bedrooms ≥ {min_bedrooms.value}",
        text="listings",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Listings by Room Type**
    """)
    return


@app.cell
def _(df, mo):
    room_ui = mo.ui.dropdown(
        options=sorted(df["room_type"].unique().tolist()),
        value="Entire home/apt",
        label="Room type"
    )

    topn_ui = mo.ui.slider(
        start=3,
        stop=len(df["city"].unique()),
        step=1,
        value=10,
        label="Top N cities"
    )

    mo.hstack([room_ui, topn_ui])
    return room_ui, topn_ui


@app.cell
def _(df, mo, room_ui):
    room_df = df[df["room_type"] == room_ui.value]

    city_counts2 = (
        room_df.groupby("city")
        .size()
        .reset_index(name="listings")
        .sort_values("listings", ascending=False)
    )

    top_city = city_counts2.iloc[0]["city"]
    top_count = int(city_counts2.iloc[0]["listings"])

    mo.hstack([
        mo.stat(value=room_ui.value, label="Room type"),
        mo.stat(value=top_city, label="Top city"),
        mo.stat(value=top_count, label="Listings"),
    ])
    return


@app.cell
def _(city_counts, px, room_ui, topn_ui):
    plot_df = city_counts.head(topn_ui.value)

    px.bar(
        plot_df,
        x="city",
        y="listings",
        title=f"Top {topn_ui.value} cities by {room_ui.value} listings",
        text="listings",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Visualizing Ratings**
    """)
    return


@app.cell
def _(df, mo):
    rating_ui = mo.ui.dropdown(
        options=[
            "guest_satisfaction_overall",
            "cleanliness_rating",
        ],
        value="guest_satisfaction_overall",
        label="Rating metric"
    )

    city_ui_r = mo.ui.dropdown(
        options=["All"] + sorted(df["city"].dropna().unique().tolist()),
        value="All",
        label="City"
    )

    bins_ui = mo.ui.slider(
        start=10,
        stop=60,
        step=5,
        value=30,
        label="Histogram bins"
    )

    mo.hstack([rating_ui, city_ui_r, bins_ui])
    return bins_ui, city_ui_r, rating_ui


@app.cell
def _(col, df_view, mo):
    series = df_view[col].dropna()

    mo.hstack([
        mo.stat(value=f"{series.mean():.2f}", label="Mean"),
        mo.stat(value=f"{series.std():.2f}", label="Std dev"),
        mo.stat(value=f"{series.quantile(0.25):.2f}", label="25th percentile"),
        mo.stat(value=f"{series.quantile(0.75):.2f}", label="75th percentile"),
    ])
    return


@app.cell
def _(bins_ui, city_ui_r, df, mo, px, rating_ui):
    df_view2 = df if city_ui_r.value == "All" else df[df["city"] == city_ui_r.value]
    col = rating_ui.value

    fig_hist = px.histogram(
        df_view2,
        x=col,
        nbins=bins_ui.value,
        title=f"Distribution: {col}",
    )

    fig_hist.update_layout(
        title={
            "text": "Distribution: guest_satisfaction_overall",
            "x": 0.5,
            "xanchor": "center"
        }
    )

    fig_box = px.box(
        df_view2,
        y=col,
        title="Variation (box plot)",
        points="outliers",
    )

    fig_box.update_layout(
        title={
            "text": "Variation (box plot)",
            "x": 0.5,
            "xanchor": "center"
        }
    )


    mo.hstack(
        [
            mo.vstack([fig_hist]),
            mo.vstack([fig_box]),
        ],
        justify="space-between"
    )
    return (col,)


@app.cell
def _(mo):
    clean_min = mo.ui.slider(
        start=1, stop=10, step=1, value=7,
        label="Minimum cleanliness rating (1–10)"
    )

    guest_min = mo.ui.slider(
        start=0, stop=100, step=1, value=90,
        label="Minimum guest satisfaction (0–100)"
    )

    mode = mo.ui.radio(
        options=["Counts", "Percent"],
        value="Counts",
        label="Display mode"
    )

    mo.hstack([clean_min, guest_min, mode])
    return clean_min, guest_min, mode


@app.cell
def _(clean_min, df, guest_min, mode, pd):
    # Apply slider filters
    passed = df[
        (df["cleanliness_rating"] >= clean_min.value) &
        (df["guest_satisfaction_overall"] >= guest_min.value)
    ]

    # Total listings per city
    total_city = df.groupby("city").size().rename("Total")

    # Listings passing filters per city
    pass_city = passed.groupby("city").size().rename("Passing")

    # Combine
    out = (
        pd.concat([total_city, pass_city], axis=1)
        .fillna(0)
        .reset_index()
    )

    out["Total"] = out["Total"].astype(int)
    out["Passing"] = out["Passing"].astype(int)

    # Choose metric
    if mode.value == "Counts":
        out["Value"] = out["Passing"]
        y_label = "Number of listings"
    else:
        out["Value"] = (out["Passing"] / out["Total"]) * 100
        y_label = "% of city listings"
    return out, y_label


@app.cell
def _(clean_min, guest_min, mo, out, px, y_label):
    plot_df5 = out.sort_values("Value", ascending=False)

    fig5 = px.bar(
        plot_df5,
        x="city",
        y="Value",
        title=(
            f"Listings by city "
            f"(cleanliness ≥ {clean_min.value}, "
            f"guest satisfaction ≥ {guest_min.value})"
        ),
        hover_data=["Passing", "Total"],
        labels={"city": "City", "Value": y_label},
    )

    fig5.update_layout(title={"x": 0.5, "xanchor": "center"})
    fig5.update_xaxes(tickangle=45)

    mo.ui.plotly(fig5)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Person Capacity across listings**
    """)
    return


@app.cell
def _(df, mo):
    city = mo.ui.dropdown(
        options=["All"] + sorted(df["city"].unique().tolist()),
        value="All",
        label="City"
    )

    cap_max = mo.ui.slider(
        start=int(df["person_capacity"].min()),
        stop=int(df["person_capacity"].max()),
        step=1,
        value=min(10, int(df["person_capacity"].max())),
        label="Show capacities up to"
    )

    mo.hstack([city, cap_max])
    return cap_max, city


@app.cell
def _(cap_max, city, df, mo, px):
    df2 = df if city.value == "All" else df[df["city"] == city.value]
    df2 = df2[df2["person_capacity"] <= cap_max.value]

    counts6 = (
        df2.groupby("person_capacity")
        .size()
        .reset_index(name="Listings")
        .sort_values("person_capacity")
    )

    fig6 = px.bar(
        counts6,
        x="person_capacity",
        y="Listings",
        labels={"person_capacity": "Person capacity", "Listings": "Number of listings"},
    )

    fig6.update_layout(
        title=dict(
            text=f"Person capacity distribution ({city.value})",
            x=0.5, xanchor="center"
        )
    )

    mo.ui.plotly(fig6)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Visualizing Price Trends**
    """)
    return


@app.cell
def _(df, mo):
    city_ui = mo.ui.dropdown(
        options=["All"] + sorted(df["city"].dropna().unique().tolist()),
        value="All",
        label="City",
    )

    day_ui = mo.ui.dropdown(
        options=["All"] + sorted(df["day_type"].dropna().unique().tolist()),
        value="All",
        label="Day type",
    )

    dist_ui = mo.ui.range_slider(
        start=float(df["citycenter_dist"].min()),
        stop=float(df["citycenter_dist"].max()),
        value=(
            float(df["citycenter_dist"].quantile(0.05)),
            float(df["citycenter_dist"].quantile(0.95)),
        ),
        step=0.1,
        label="City center distance (km)",
    )

    mo.hstack([city_ui, day_ui, dist_ui])
    return city_ui, day_ui, dist_ui


@app.cell
def _(city_ui, day_ui, df, dist_ui):
    df_f = df.copy()

    if city_ui.value != "All":
        df_f = df_f[df_f["city"] == city_ui.value]

    if day_ui.value != "All":
        df_f = df_f[df_f["day_type"] == day_ui.value]

    dmin, dmax = dist_ui.value
    df_f = df_f[(df_f["citycenter_dist"] >= dmin) & (df_f["citycenter_dist"] <= dmax)]
    return (df_f,)


@app.cell
def _(df_f, mo):
    prices = df_f["price"].dropna()

    stat = getattr(mo, "stat", None) or mo.ui.stat

    if prices.empty:
        cards = mo.md("### No listings match these filters.")
    else:
        median_price = max(0.0, float(prices.median()))
        q25 = max(0.0, float(prices.quantile(0.25)))
        q75 = max(0.0, float(prices.quantile(0.75)))
        q90 = max(0.0, float(prices.quantile(0.90)))

        cards = mo.hstack([
            stat(value=len(prices), label="Listings"),
            stat(value=f"€{median_price:.0f}", label="Median price"),
            stat(value=f"€{q25:.0f} – €{q75:.0f}", label="Typical range"),
            stat(value=f"€{q90:.0f}", label="Premium price (90th)"),
        ])

    cards
    return


@app.cell
def _(df_f, px):

    room_counts = (
        df_f.groupby("room_type")
        .size()
        .reset_index(name="listings")
        .sort_values("listings", ascending=False)
    )

    fig7 = px.bar(
        room_counts,
        x="room_type",
        y="listings",
        title="Listings per room type (filtered)",
        text="listings",
    )
    fig7.update_layout(title_x=0.5)
    fig7
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Visualizing Geographically**
    """)
    return


@app.cell
def _(mo):
    zoom_ui = mo.ui.slider(
        start=3,
        stop=10,
        step=1,
        value=3,
        label="Map zoom"
    )

    zoom_ui
    return (zoom_ui,)


@app.cell
def _(df, px, zoom_ui):
    # Aggregate at city level (clean & fast)
    map_df = (
        df.groupby(["city", "country"])
        .agg(
            listings=("city", "size"),
            lat=("lat", "mean"),
            lon=("lng", "mean"),
            median_price=("price", "median"),
        )
        .reset_index()
    )

    # Europe center (approximate, works well visually)
    EUROPE_CENTER = {"lat": 45.0, "lon": 18.0}

    fig10 = px.scatter_mapbox(
        map_df,
        lat="lat",
        lon="lon",
        size="listings",
        color="median_price",
        hover_name="city",
        hover_data={
            "country": True,
            "listings": True,
            "median_price": ":.0f",
            "lat": False,
            "lon": False,
        },
        size_max=45,
        zoom=zoom_ui.value,
        center=EUROPE_CENTER,
        title="Airbnb listings across European cities<br><sup>Size = number of listings · Color = median price</sup>",
    )

    fig10.update_layout(
        mapbox_style="open-street-map",
        margin=dict(l=0, r=0, t=70, b=0),
        title_x=0.5,
    )

    fig10
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
