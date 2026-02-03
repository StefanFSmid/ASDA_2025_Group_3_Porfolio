import marimo

__generated_with = "0.19.7"
app = marimo.App(width="medium", auto_download=["html"])


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import altair as alt
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans
    from sklearn.decomposition import PCA
    from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
    from sklearn.metrics import silhouette_score, pairwise_distances

    # Disable Altair max rows warning for this dataset size
    alt.data_transformers.disable_max_rows()
    return (
        KMeans,
        PCA,
        StandardScaler,
        alt,
        dendrogram,
        fcluster,
        linkage,
        mo,
        np,
        pd,
        plt,
        silhouette_score,
    )


@app.cell
def _(pd):
    # Load Spotify dataset
    username = "datagus"
    repository = "ASDA2025"
    directory = "datasets/homework_week11/6.3.3_spotify_5000_songs.csv"
    github_url = f"https://raw.githubusercontent.com/{username}/{repository}/main/{directory}"
    df = pd.read_csv(github_url)

    # Clean column names
    df.columns = df.columns.str.strip()
    return (df,)


@app.cell
def _(mo):
    mo.md("""
    # 🎵 Spotify Song Analysis Dashboard

    **Contributors:** Stefan

    ### Project Objective
    This dashboard demonstrates how data-driven methods can support playlist curation. By grouping songs based on audio features (like **energy**, **valence**, and **danceability**) rather than genre, we can identify distinct musical moods automatically. While you can explore any number of clusters below, our analysis suggests that **k=4** provides the most distinct musical moods.

    **How to use:**
    1. Adjust **k** to change the number of clusters.
    2. Use the **filters** to find specific artists or songs.
    3. Explore the **Audio Profile Heatmap** to interpret what each cluster represents.
    4. Listen to the **Spotify Previews** to validate the grouping.
    """)
    return


@app.cell
def _(StandardScaler, df, pd):
    # Define clustering features
    audio_features = [
        "danceability", "energy", "loudness", "speechiness", "acousticness", 
        "instrumentalness", "liveness", "valence", "tempo", "duration_ms"
    ]

    # Create feature matrix (X)
    X = df[audio_features].copy()
    X = X.dropna(axis=0)

    # Scale the data (StandardScaler)
    scaler = StandardScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns, index=X.index)
    return X, X_scaled


@app.cell
def _(PCA, X_scaled, linkage, pd):
    # 1. Run PCA for Visualization (Map)
    pca = PCA(n_components=2, random_state=42)
    X_pca = pca.fit_transform(X_scaled)
    X_pca_df = pd.DataFrame(X_pca, columns=['PC1', 'PC2'], index=X_scaled.index)

    # 2. Run Hierarchical Linkage (Ward's Method)
    linkage_matrix = linkage(X_scaled, method="ward")
    max_dist = linkage_matrix[-1, 2]
    return X_pca_df, linkage_matrix, max_dist, pca


@app.cell
def _(X, df, mo):
    # Create interactive UI elements
    k_slider_final = mo.ui.slider(
        start=2, stop=10, value=4, step=1, label="Number of Clusters (k)"
    )

    # Artist Dropdown
    artists_list = ["All"] + sorted(df.loc[X.index, "artist"].unique().tolist())
    artist_filter_final = mo.ui.dropdown(
        options=artists_list, value="All", label="Filter by Artist"
    )

    # Song Search
    song_search_final = mo.ui.text(
        label="Search Song Title", placeholder="Type to filter..."
    )

    # Display Controls
    mo.callout(
        mo.vstack([
            mo.md("### 🎧 Spotify Cluster Dashboard"),
            mo.hstack([k_slider_final, artist_filter_final, song_search_final], gap=2)
        ]),
        kind="neutral"
    )
    return artist_filter_final, k_slider_final, song_search_final


@app.cell
def _(
    KMeans,
    X_pca_df,
    X_scaled,
    alt,
    artist_filter_final,
    df,
    k_slider_final,
    pca,
    pd,
    song_search_final,
):
    # 1. Get current k
    current_k = int(k_slider_final.value)

    # 2. Fit K-Means
    kmeans_interactive = KMeans(n_clusters=current_k, random_state=42, n_init=10)
    cluster_labels_interactive = kmeans_interactive.fit_predict(X_scaled)

    # 3. Prepare Plot Data
    plot_data = X_pca_df.copy()
    plot_data["cluster"] = cluster_labels_interactive.astype(str)
    plot_data["artist"] = df.loc[plot_data.index, "artist"]
    plot_data["name"] = df.loc[plot_data.index, "name"]

    # 4. Apply Filters
    mask = pd.Series(True, index=plot_data.index)
    if artist_filter_final.value != "All":
        mask &= (plot_data["artist"] == artist_filter_final.value)
    if song_search_final.value.strip():
        mask &= (plot_data["name"].str.contains(song_search_final.value, case=False))

    filtered_plot_data = plot_data[mask].copy()

    # 5. Calculate Visual Centroids
    current_centroids_pca = pca.transform(kmeans_interactive.cluster_centers_)
    centroids_viz_df = pd.DataFrame(current_centroids_pca, columns=["PC1", "PC2"])
    centroids_viz_df["cluster"] = centroids_viz_df.index.astype(str)

    # 6. Altair Chart
    base_chart = alt.Chart(filtered_plot_data).mark_circle(size=60, opacity=0.7).encode(
        x=alt.X('PC1:Q', title='PC1'),
        y=alt.Y('PC2:Q', title='PC2'),
        color=alt.Color('cluster:N', title='Cluster', scale=alt.Scale(scheme='category10')),
        tooltip=['name', 'artist', 'cluster']
    ).properties(
        title=f"Clusters (k={current_k}) - {len(filtered_plot_data)} songs visible",
        width=600, height=400
    )

    centroid_chart = alt.Chart(centroids_viz_df).mark_point(
        shape='cross', size=300, filled=True, strokeWidth=3, color='black'
    ).encode(x='PC1:Q', y='PC2:Q', tooltip=['cluster'])

    (base_chart + centroid_chart).interactive()
    return (
        cluster_labels_interactive,
        current_k,
        filtered_plot_data,
        kmeans_interactive,
    )


@app.cell
def _(
    X_scaled,
    cluster_labels_interactive,
    kmeans_interactive,
    mo,
    silhouette_score,
):
    # Metrics Calculation
    inertia = kmeans_interactive.inertia_
    sil_score = silhouette_score(X_scaled, cluster_labels_interactive)

    mo.hstack([
        mo.stat(label="Inertia (WCSS)", value=f"{inertia:,.0f}"),
        mo.stat(label="Silhouette Score", value=f"{sil_score:.3f}")
    ], gap=4)
    return


@app.cell
def _(X_scaled, alt, cluster_labels_interactive, current_k, mo):
    # Calculate cluster profiles
    profile_df = X_scaled.copy()
    profile_df["cluster"] = cluster_labels_interactive
    cluster_profiles = profile_df.groupby("cluster").mean().reset_index()
    cluster_profiles_long = cluster_profiles.melt(id_vars="cluster", var_name="feature", value_name="z_score")

    # Heatmap Visualization
    heatmap = alt.Chart(cluster_profiles_long).mark_rect().encode(
        x=alt.X('feature:N', axis=alt.Axis(labelAngle=-45)),
        y=alt.Y('cluster:N'),
        color=alt.Color('z_score:Q', scale=alt.Scale(scheme='redblue', domainMid=0)),
        tooltip=['cluster', 'feature', alt.Tooltip('z_score', format='.2f')]
    ).properties(width=600, height=150 + (current_k * 20))

    text = heatmap.mark_text(baseline='middle').encode(
        text=alt.Text('z_score:Q', format='.1f'), color=alt.value('black')
    )

    mo.vstack([
        mo.md("### 📊 Audio Feature Analysis (Red = High, Blue = Low)"),
        (heatmap + text)
    ])
    return


@app.cell
def _(pd):
    def get_spotify_iframe(track_id):
        if pd.isna(track_id):
            return "<div>No ID available</div>"

        # Convert to string just in case
        track_str = str(track_id).strip()

        # Logic to extract the ID if the input is a full URL
        # Example Input: https://open.spotify.com/track/6rqhFgbbKwnb9MLmUQDhG6
        if "track/" in track_str:
            # Split by 'track/' and take the last part, then remove any query params (?)
            clean_id = track_str.split("track/")[-1].split("?")[0]
        else:
            # Assume it's already just the ID
            clean_id = track_str

        # Spotify Embed URL structure
        embed_url = f"https://open.spotify.com/embed/track/{clean_id}?utm_source=generator"

        return f"""
        <iframe style="border-radius:12px" 
                src="{embed_url}" 
                width="100%" 
                height="152" 
                frameBorder="0" 
                allowfullscreen="" 
                allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" 
                loading="lazy">
        </iframe>
        """
    return (get_spotify_iframe,)


@app.cell
def _(
    X_scaled,
    df,
    filtered_plot_data,
    get_spotify_iframe,
    kmeans_interactive,
    mo,
    np,
):
    # Cell 9: Spotify Embeds (Updated with HTML styling)
    if len(filtered_plot_data) > 0:
        # 1. Get subset of data
        X_subset = X_scaled.loc[filtered_plot_data.index]

        # 2. Identify assigned clusters and centroids
        assigned_clusters = filtered_plot_data["cluster"].astype(int).values
        assigned_centroids = kmeans_interactive.cluster_centers_[assigned_clusters]

        # 3. Calculate distances
        dists = np.sqrt(np.sum((X_subset.values - assigned_centroids)**2, axis=1))

        # 4. Create ranking dataframe
        preview_df = df.loc[filtered_plot_data.index].copy()
        preview_df["cluster"] = assigned_clusters
        preview_df["dist_to_centroid"] = dists

        # 5. Get Top 3 per cluster
        top_picks = preview_df.sort_values("dist_to_centroid").groupby("cluster").head(3)

        cluster_sections = []

        # 6. Build UI
        for c in sorted(top_picks["cluster"].unique()):
            songs_in_cluster = top_picks[top_picks["cluster"] == c]

            # Header
            header = mo.md(f"### 🎵 Cluster {c} (Top Matches)")

            song_cards = []
            for _, row in songs_in_cluster.iterrows():
                # Use the 'html' column with our helper function
                iframe_code = get_spotify_iframe(row['html'])

                # Use mo.Html with explicit HTML tags for styling
                card = mo.vstack([
                    mo.Html(f"<b>{row['name']}</b>"),
                    mo.Html(f"<i>{row['artist']}</i>"),
                    mo.Html(iframe_code)
                ], align="center")

                song_cards.append(card)

            # Stack horizontal cards for this cluster
            cluster_sections.append(
                mo.vstack([
                    header, 
                    mo.hstack(song_cards, gap=2, wrap=True)
                ])
            )

        display_output = mo.vstack(cluster_sections, gap=2)
    else:
        display_output = mo.md("⚠️ No songs match your current filter.")

    display_output
    return


@app.cell
def _(mo):
    mo.md("""
    ### ✂️ Hierarchical Validation

    This section uses **Hierarchical Clustering (Ward's Method)**. Unlike K-Means, this builds a tree structure (dendrogram) of the data.

    *   **Adjust the Cut Height** to slice the tree at different levels.
    *   Cutting the tree at a height of **~72** typically yields the same 4 main clusters found in K-Means, validating the structure of the data.
    """)
    return


@app.cell
def _(max_dist, mo):
    cut_slider = mo.ui.slider(
        start=0, stop=float(max_dist), step=1.0, value=72.0, 
        label="Cut Height"
    )

    mo.callout(
        mo.vstack([
            mo.md("### ✂️ Hierarchical Clustering Control"),
            cut_slider
        ]), kind="neutral"
    )
    return (cut_slider,)


@app.cell
def _(X_pca_df, cut_slider, dendrogram, fcluster, linkage_matrix, np, plt):
    # 1. Get current cut height
    current_cut = cut_slider.value

    # 2. "Cut" the tree to get cluster labels
    # criterion="distance" splits the tree where the distance between merges is > current_cut
    h_labels = fcluster(linkage_matrix, t=current_cut, criterion="distance")
    n_clusters_h = len(np.unique(h_labels))

    # 3. Create the Dendrogram Plot (Matplotlib)
    # We use truncate_mode='lastp' to keep the visual clean and fast
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    dendrogram(
        linkage_matrix,
        truncate_mode='lastp',  # Show only the last p merged clusters
        p=30,                   # Show top 30 branches for clarity
        leaf_rotation=90.,
        leaf_font_size=10.,
        show_contracted=True,
        ax=ax1,
        color_threshold=current_cut # Colors branches below the cut differently
    )

    # Add the interactive cut line
    ax1.axhline(y=current_cut, c='red', lw=2, linestyle='--')
    ax1.set_title(f"Hierarchical Dendrogram (Cut Height={current_cut})")
    ax1.set_ylabel("Ward Distance")
    ax1.set_xlabel(f"Resulting Clusters: {n_clusters_h}")

    # 4. Create the PCA Scatter Plot (Matplotlib for easy side-by-side)
    # We color points by the new hierarchical labels
    scatter = ax2.scatter(
        X_pca_df["PC1"], 
        X_pca_df["PC2"], 
        c=h_labels, 
        cmap='tab10', 
        alpha=0.6, 
        s=15
    )
    ax2.set_title(f"PCA Projection ({n_clusters_h} clusters)")
    ax2.set_xlabel("PC1")
    ax2.set_ylabel("PC2")

    plt.tight_layout()
    plt.gca() # Display the plot
    return


if __name__ == "__main__":
    app.run()
