import marimo

__generated_with = "0.19.6"
app = marimo.App(width="medium")


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
        pairwise_distances,
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
    return X, X_scaled, audio_features


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
def _(X_scaled, df, filtered_plot_data, kmeans_interactive, mo, np):
    # Show top 3 songs per cluster based on distance to centroid
    if len(filtered_plot_data) > 0:
        X_subset = X_scaled.loc[filtered_plot_data.index]
        assigned_clusters = filtered_plot_data["cluster"].astype(int).values
        assigned_centroids = kmeans_interactive.cluster_centers_[assigned_clusters]
        dists = np.sqrt(np.sum((X_subset.values - assigned_centroids)**2, axis=1))
    
        preview_df = df.loc[filtered_plot_data.index].copy()
        preview_df["cluster"] = assigned_clusters
        preview_df["dist_to_centroid"] = dists
    
        top_picks = preview_df.sort_values("dist_to_centroid").groupby("cluster").head(3)
    
        cluster_sections = []
        for c in sorted(top_picks["cluster"].unique()):
            songs_in_cluster = top_picks[top_picks["cluster"] == c]
            header = mo.md(f"### 🎵 Cluster {c}")
            song_cards = []
            for _, row in songs_in_cluster.iterrows():
                card = mo.vstack([
                    mo.md(f"**{row['name']}**\n_{row['artist']}_"),
                    mo.Html(row.get("html", ""))
                ], align="center")
                song_cards.append(card)
            cluster_sections.append(mo.vstack([header, mo.hstack(song_cards, gap=1, wrap=True)]))
        display_output = mo.vstack(cluster_sections, gap=2)
    else:
        display_output = mo.md("⚠️ No songs match your current filter.")

    display_output
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


app._unparsable_cell(
    r"""
    current_cut = cut_slider.value
    h_labels = fcluster(linkage_matrix, t=current_cut, criterion="distance")
    n_clusters_h = len(np.unique(h_labels))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Plot Dendrogram
    dendrogram(
        linkage_matrix, truncate_mode='lastp', p=30, leaf_rotation=90.,
        show_contracted=True, ax=ax1, color_threshold=current_cut
    )
    ax1.axhline(y=current_cut, c='red', lw=2, linestyle='--')
    ax1.set_title(f"Dendrogram (Cut Height={current_cut})")

    # Plot Scatter
    ax2.scatter(X_pca_df["PC1"], X_pca_df["PC2
    """,
    name="_"
)


@app.cell
def _(X, df, mo):
    # Create interactive UI elements
    k_slider_final = mo.ui.slider(
        start=2, 
        stop=10, 
        value=4, 
        step=1, 
        label="Number of Clusters (k)"
    )

    # Get list of artists for the dropdown
    artists_list = ["All"] + sorted(df.loc[X.index, "artist"].unique().tolist())
    artist_filter_final = mo.ui.dropdown(
        options=artists_list,
        value="All",
        label="Filter by Artist"
    )

    # Use a text input for song search (better for large lists)
    song_search_final = mo.ui.text(
        label="Search Song Title",
        placeholder="Type to filter..."
    )

    # Display controls
    mo.callout(
        mo.vstack([
            mo.md("### 🎧 Dashboard Controls"),
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
    # Re-run K-Means and build the interactive plot
    # 1. Get current k from slider
    current_k = int(k_slider_final.value)

    # 2. Fit K-Means on the scaled data (re-run logic)
    kmeans_interactive = KMeans(n_clusters=current_k, random_state=42, n_init=10)
    cluster_labels_interactive = kmeans_interactive.fit_predict(X_scaled)

    # 3. Prepare data for plotting
    # We reuse the PCA coordinates calculated earlier to keep the "map" consistent
    plot_data = X_pca_df.copy()
    plot_data["cluster"] = cluster_labels_interactive.astype(str)
    # Add metadata from original dataframe (aligned by index)
    plot_data["artist"] = df.loc[plot_data.index, "artist"]
    plot_data["name"] = df.loc[plot_data.index, "name"]

    # 4. Apply Filters (Artist & Song)
    mask = pd.Series(True, index=plot_data.index)

    if artist_filter_final.value != "All":
        mask &= (plot_data["artist"] == artist_filter_final.value)

    if song_search_final.value.strip():
        # Case-insensitive string search
        mask &= (plot_data["name"].str.contains(song_search_final.value, case=False))

    filtered_plot_data = plot_data[mask].copy()

    # 5. Calculate Centroids for the plot
    # We project the new K-Means centroids into the existing PCA space
    current_centroids_pca = pca.transform(kmeans_interactive.cluster_centers_)
    centroids_viz_df = pd.DataFrame(current_centroids_pca, columns=["PC1", "PC2"])
    centroids_viz_df["cluster"] = centroids_viz_df.index.astype(str)

    # 6. Create Altair Chart
    base_chart = alt.Chart(filtered_plot_data).mark_circle(size=60, opacity=0.7).encode(
        x=alt.X('PC1:Q', title='PC1'),
        y=alt.Y('PC2:Q', title='PC2'),
        color=alt.Color('cluster:N', title='Cluster', scale=alt.Scale(scheme='category10')),
        tooltip=['name', 'artist', 'cluster']
    ).properties(
        title=f"Clusters (k={current_k}) - {len(filtered_plot_data)} songs visible",
        width=600,
        height=400
    )

    # Overlay centroids (always visible to show structure)
    centroid_chart = alt.Chart(centroids_viz_df).mark_point(
        shape='cross', size=300, filled=True, strokeWidth=3, color='black'
    ).encode(
        x='PC1:Q',
        y='PC2:Q',
        tooltip=['cluster']
    )

    combined_chart = (base_chart + centroid_chart).interactive()
    combined_chart
    return (
        cluster_labels_interactive,
        current_k,
        filtered_plot_data,
        kmeans_interactive,
    )


@app.cell
def _(X_scaled, df, filtered_plot_data, kmeans_interactive, mo, np):
    # Display Spotify Embeds for the top songs in the filtered view
    if len(filtered_plot_data) > 0:
        # 1. Get the feature vectors for the currently filtered selection
        X_subset = X_scaled.loc[filtered_plot_data.index]
    
        # 2. Get the assigned centroids for these specific points
        # filtered_plot_data["cluster"] comes from the dynamic K-Means in Cell 2
        assigned_clusters = filtered_plot_data["cluster"].astype(int).values
        assigned_centroids = kmeans_interactive.cluster_centers_[assigned_clusters]
    
        # 3. Calculate Euclidean distance to the assigned centroid
        # (Lower distance = more representative of that cluster)
        dists = np.sqrt(np.sum((X_subset.values - assigned_centroids)**2, axis=1))
    
        # 4. Create a temporary dataframe for ranking
        preview_df = df.loc[filtered_plot_data.index].copy()
        preview_df["cluster"] = assigned_clusters
        preview_df["dist_to_centroid"] = dists
    
        # 5. Pick the top 3 closest songs per cluster
        top_picks = preview_df.sort_values("dist_to_centroid").groupby("cluster").head(3)
    
        # 6. Build the Visual Layout
        cluster_sections = []
    
        # Iterate through clusters present in the data
        for c in sorted(top_picks["cluster"].unique()):
            songs_in_cluster = top_picks[top_picks["cluster"] == c]
        
            # Create a header for the cluster
            header = mo.md(f"### 🎵 Cluster {c} (Top Matches)")
        
            # Create song cards
            song_cards = []
            for _, row in songs_in_cluster.iterrows():
                # The dataset has an 'html' column with the Spotify iframe
                iframe_code = row.get("html", "No Preview Available")
            
                card = mo.vstack([
                    mo.md(f"**{row['name']}**"),
                    mo.md(f"_{row['artist']}_"),
                    mo.Html(iframe_code)
                ], align="center")
            
                song_cards.append(card)
        
            # Add this cluster's section to the list
            cluster_sections.append(
                mo.vstack([
                    header, 
                    mo.hstack(song_cards, gap=1, wrap=True)
                ])
            )
        
        # Combine all sections
        display_output = mo.vstack(cluster_sections, gap=2)
    else:
        display_output = mo.md("⚠️ No songs match your current filter criteria.")

    display_output
    return


@app.cell
def _(X_scaled, alt, cluster_labels_interactive, current_k, mo):
    # Calculate cluster profiles (mean of scaled features) based on current interactive labels
    # 1. Create a temporary dataframe with scaled features and current cluster labels
    profile_df = X_scaled.copy()
    profile_df["cluster"] = cluster_labels_interactive

    # 2. Calculate the mean of each feature for each cluster
    # Since X_scaled is already standardized, a value of 0 means "average", 
    # +1 means "high" (1 std dev above mean), -1 means "low".
    cluster_profiles = profile_df.groupby("cluster").mean().reset_index()

    # 3. Melt for Altair (convert to long format)
    cluster_profiles_long = cluster_profiles.melt(
        id_vars="cluster", 
        var_name="feature", 
        value_name="z_score"
    )

    # 4. Create the Heatmap
    heatmap = alt.Chart(cluster_profiles_long).mark_rect().encode(
        x=alt.X('feature:N', title=None, axis=alt.Axis(labelAngle=-45)),
        y=alt.Y('cluster:N', title='Cluster'),
        color=alt.Color(
            'z_score:Q', 
            title='Deviation from Mean',
            scale=alt.Scale(scheme='redblue', domainMid=0)
        ),
        tooltip=['cluster', 'feature', alt.Tooltip('z_score', format='.2f')]
    ).properties(
        title=f"Cluster Audio Profiles (k={current_k})",
        width=600,
        height=150 + (current_k * 20)  # Dynamic height based on number of clusters
    )

    # Text overlay to show values on the heatmap
    text = heatmap.mark_text(baseline='middle').encode(
        text=alt.Text('z_score:Q', format='.1f'),
        color=alt.value('black')  # readable on most diverging colors
    )

    # Combine and display
    mo.vstack([
        mo.md("### 📊 Audio Feature Analysis"),
        mo.md("*Values show how many standard deviations the cluster average is from the global average. Blue = Low, Red = High.*"),
        (heatmap + text)
    ])
    return


@app.cell
def _(X_scaled, linkage):
    # Calculate linkage matrix (heavy computation, run once)
    # Using Ward's method as in your original analysis
    linkage_matrix = linkage(X_scaled, method="ward")

    # Determine the maximum height of the tree to set slider limits
    max_dist = linkage_matrix[-1, 2]
    return linkage_matrix, max_dist


@app.cell
def _(max_dist, mo):
    # Create a slider for the dendrogram cut height
    cut_slider = mo.ui.slider(
        start=0,
        stop=float(max_dist),
        step=1.0,
        value=72.0,  # Your original static value
        label="Dendrogram Cut Height (Distance)"
    )

    mo.callout(
        mo.vstack([
            mo.md("### ✂️ Hierarchical Clustering Control"),
            mo.md("Adjust the slider to 'cut' the tree at different heights. Lower height = more clusters."),
            cut_slider
        ]),
        kind="neutral"
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


@app.cell
def _():
    import pandas as pd
    import altair as alt
    import numpy as np
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans
    from sklearn.decomposition import PCA
    from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
    from sklearn.metrics import silhouette_score
    import matplotlib.pyplot as plt
    from sklearn.metrics import pairwise_distances
    return (
        KMeans,
        PCA,
        StandardScaler,
        alt,
        dendrogram,
        fcluster,
        linkage,
        np,
        pairwise_distances,
        pd,
        plt,
        silhouette_score,
    )


@app.cell
def _(pd):
    # spotify dataset from GitHub
    username = "datagus"
    repository = "ASDA2025"
    directory = "datasets/homework_week11/6.3.3_spotify_5000_songs.csv"
    github_url = f"https://raw.githubusercontent.com/{username}/{repository}/main/{directory}"
    df = pd.read_csv(github_url)
    df.info()
    return (df,)


@app.cell
def _(df):
    df.head()
    return


@app.cell
def _(df):
    # clustering features
    audio_features = [
        "danceability","energy","loudness","speechiness","acousticness",
        "instrumentalness","liveness","valence","tempo","duration_ms"
    ]
    df.columns = df.columns.str.strip()

    # Create a dataframe with only these features
    X = df[audio_features].copy()
    X = X.dropna(axis=0)
    return X, audio_features


@app.cell
def _(StandardScaler, X, pd):
    # Scale the data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_scaled = pd.DataFrame(X_scaled, columns=X.columns)
    X_scaled.describe()
    return (X_scaled,)


@app.cell
def _(KMeans, X_scaled, plt, silhouette_score):
    # Determine optimal K using Elbow Method and Silhouette Score
    inertias = []
    K_range = range(1, 11)

    for k_i_1 in K_range:
        kmeans_1 = KMeans(n_clusters=k_i_1, random_state=42, n_init=10)
        kmeans_1.fit(X_scaled)
        inertias.append(kmeans_1.inertia_)


    silhouette_scores = []

    for k_i_2 in range(2, 11):  # silhouette requires k ≥ 2
        kmeans_2 = KMeans(n_clusters=k_i_2, random_state=42, n_init=10)
        labels_1 = kmeans_2.fit_predict(X_scaled)
        score = silhouette_score(X_scaled, labels_1)
        silhouette_scores.append(score)


    fig, axes = plt.subplots(1, 2, figsize=(14, 5), constrained_layout=True)

    # Elbow plot 
    axes[0].plot(K_range, inertias, marker='o')
    axes[0].set_xlabel('Number of clusters (K)')
    axes[0].set_ylabel('Inertia (WCSS)')
    axes[0].set_title('Elbow Method for Optimal K')

    # Silhouette plot
    axes[1].plot(range(2, 11), silhouette_scores, marker='o')
    axes[1].set_xlabel('Number of clusters (K)')
    axes[1].set_ylabel('Silhouette Score')
    axes[1].set_title('Silhouette Score vs K')

    plt.show()
    return


@app.cell
def _(KMeans, X_scaled, df):
    # Fit KMeans with chosen K
    kmeans = KMeans(
        n_clusters=4,
        init="k-means++", 
        n_init=10,
        random_state=42
    )

    labels_2 = kmeans.fit_predict(X_scaled)
    centroids = kmeans.cluster_centers_
    df["cluster"] = labels_2
    return centroids, kmeans


@app.cell
def _(X_scaled, centroids, np, pd):
    # Calculate distances to centroids
    k = centroids.shape[0]
    distances = pd.DataFrame(index=X_scaled.index)

    for i in range(k):
        diff = X_scaled.values - centroids[i]
        dist = np.sqrt(np.sum(diff**2, axis=1))
        distances[f"centroid_{i}"] = dist

    distances.head()
    return


@app.cell
def _(PCA, X_scaled, df, pd):
    # Apply PCA to reduce to 2 dimensions
    pca = PCA(n_components=2, random_state=42)
    X_pca = pca.fit_transform(X_scaled)

    # Create a DataFrame with PCA results
    X_pca_df = pd.DataFrame(
        X_pca,
        columns=['PC1', 'PC2'],
        index=X_scaled.index
    )
    # Attach cluster labels
    X_pca_df["cluster"] = df["cluster"]

    # Display variance explained
    variance_explained = pca.explained_variance_ratio_
    print(f"""
    **PCA Results:**
    - PC1 explains {variance_explained[0]:.2%} of variance
    - PC2 explains {variance_explained[1]:.2%} of variance
    - Total variance explained: {variance_explained.sum():.2%}
    """)
    return X_pca_df, pca, variance_explained


@app.cell
def _(centroids, pca, pd):
    # Transform centroids to PCA space
    centroids_pca = pca.transform(centroids) 

    centroids_df = pd.DataFrame(centroids_pca, columns=["PC1", "PC2"])
    centroids_df["cluster"] = centroids_df.index.astype(str)
    return (centroids_df,)


@app.cell
def _(X_pca_df, alt, centroids_df, df, variance_explained):
    # Create Altair plot
    alt.data_transformers.disable_max_rows()
    plot_df_1 = X_pca_df.copy()
    plot_df_1["cluster"] = df["cluster"].astype(str)

    # trimming extreme PCA outliers for visualization only
    lower_q_1 = X_pca_df["PC1"].quantile(0.01)
    upper_q_1 = X_pca_df["PC1"].quantile(0.99)

    plot_df_1 = X_pca_df[
        (X_pca_df["PC1"] >= lower_q_1) &
        (X_pca_df["PC1"] <= upper_q_1)
    ].copy()


    points = alt.Chart(plot_df_1).mark_circle(size=30, opacity=0.6).encode(
        x=alt.X('PC1:Q', title=f'PC1 ({variance_explained[0]:.1%} variance)'),
        y=alt.Y('PC2:Q', title=f'PC2 ({variance_explained[1]:.1%} variance)'),
        color=alt.Color('cluster:N', title='Cluster', scale=alt.Scale(scheme='category10')),
        tooltip=['PC1:Q', 'PC2:Q', 'cluster:N']
    )

    centroids_plot = alt.Chart(centroids_df).mark_point(
        shape='cross',
        size=300,
        filled=True,
        strokeWidth=3
    ).encode(
        x='PC1:Q',
        y='PC2:Q',
        color=alt.Color('cluster:N', scale=alt.Scale(scheme='category10')),
        tooltip=['PC1:Q', 'PC2:Q', 'cluster:N']
    )

    chart = (points + centroids_plot).properties(
        title='K-Means Clusters',
        width=600,
        height=500
    )
    chart
    return


@app.cell
def _(audio_features, df):
    # check mean for each cluster rounded to 2
    df.groupby("cluster")[audio_features].mean().round(2)
    return


@app.cell
def _(df):
    # check number of samples in each cluster
    df["cluster"].value_counts()
    return


@app.cell
def _(X_pca_df, X_scaled, alt, np, pca, pd, variance_explained):
    # Get PCA loadings (how original features contribute to PCs)
    loadings = pca.components_.T * np.sqrt(pca.explained_variance_)

    # Create DataFrame with loadings
    loadings_df = pd.DataFrame(
        loadings,
        columns=['PC1', 'PC2'],
        index=X_scaled.columns
    )

    # Scale loadings for visualization
    scale_factor = 3
    loadings_df_scaled = loadings_df * scale_factor

    # Add feature names
    loadings_df_scaled['feature'] = loadings_df_scaled.index

    # trimming extreme PCA outliers for visualization only
    lower_q_2 = X_pca_df["PC1"].quantile(0.01)
    upper_q_2 = X_pca_df["PC1"].quantile(0.99)

    plot_df_2 = X_pca_df[
        (X_pca_df["PC1"] >= lower_q_2) &
        (X_pca_df["PC1"] <= upper_q_2)
    ].copy()

    # Create arrows for loadings
    loadings_chart_data = []
    for feature in loadings_df_scaled.index:
        loadings_chart_data.append({
            'feature': feature,
            'x': 0,
            'y': 0,
            'x2': loadings_df_scaled.loc[feature, 'PC1'],
            'y2': loadings_df_scaled.loc[feature, 'PC2']
        })

    loadings_chart_df = pd.DataFrame(loadings_chart_data)

    # Create the biplot with current iteration clusters
    base_points = alt.Chart(plot_df_2).mark_circle(size=20, opacity=0.3).encode(
        x=alt.X('PC1:Q', title=f'PC1 ({variance_explained[0]:.1%} variance)'),
        y=alt.Y('PC2:Q', title=f'PC2 ({variance_explained[1]:.1%} variance)'),
        color=alt.Color('cluster:N', title='Cluster', scale=alt.Scale(scheme='category10'))
    )

    # Create arrows for loadings
    arrows = alt.Chart(loadings_chart_df).mark_rule(strokeWidth=2, color='red').encode(
        x='x:Q',
        y='y:Q',
        x2='x2:Q',
        y2='y2:Q'
    )

    # Create text labels for loadings
    labels_3 = alt.Chart(loadings_chart_df).mark_text(
        align='center',
        baseline='middle',
        dx=0,
        dy=-10,
        fontSize=11,
        fontWeight='bold'
    ).encode(
        x='x2:Q',
        y='y2:Q',
        text='feature:N'
    )

    # Combine all layers
    biplot = (base_points + arrows + labels_3).properties(
        title=f'Biplot - K-Means',
        width=700,
        height=600
    )

    biplot
    return


@app.cell
def _(X_scaled, linkage, pd):
    # Hierarchical Clustering using Ward's method
    linkage_matrix = linkage(
        X_scaled,
        method="ward"
    )

    linkage_matrix_df = pd.DataFrame(
        linkage_matrix,
        columns=["cluster_1", "cluster_2", "distance", "n_observations"]
    )

    linkage_matrix_df.head(10)
    return (linkage_matrix,)


@app.cell
def _(dendrogram, linkage_matrix, plt):
    # Create the dendrogram
    plt.figure(figsize=(12, 6))
    dendrogram(
        linkage_matrix,
        show_contracted=True,
        no_labels=True
    )


    plt.title('Hierarchical Clustering Dendrogram', fontsize=14)
    plt.xlabel('Cluster Index or (Sample Count)', fontsize=12)
    plt.ylabel('Distance (Ward)', fontsize=12)
    plt.grid(True, alpha=0.3)

    plt.gca();
    return


@app.cell
def _(fcluster, linkage_matrix, np):
    # Cut the dendrogram at height = 72 to form flat clusters
    cut_height = 72
    clusters_at_72 = fcluster(linkage_matrix, t=cut_height, criterion="distance")
    print("Number of clusters at cut=72:", len(np.unique(clusters_at_72)))
    return (clusters_at_72,)


@app.cell
def _(dendrogram, linkage_matrix, plt):
    # Visualize dendrogram with cut line at 72
    plt.figure(figsize=(12, 6))
    dendrogram(linkage_matrix, show_contracted=True, no_labels=True)
    plt.axhline(y=72, color="purple", linestyle="--", linewidth=2)
    plt.title("Dendrogram (Ward) with cut at 72")
    plt.ylabel("Distance (Ward)")
    plt.grid(True, alpha=0.3)
    plt.show()
    return


@app.cell
def _(X_scaled, clusters_at_72):
    # Create a DataFrame to hold cluster assignments at height 72
    X_clusters_height_72 = X_scaled.copy()  
    X_clusters_height_72["h_cluster"] = clusters_at_72

    X_clusters_height_72.head(10)
    return


@app.cell
def _(X_pca_df, alt, clusters_at_72, pd, variance_explained):
    # trimming extreme PCA outliers for visualization only
    lower_q_3 = X_pca_df["PC1"].quantile(0.01)
    upper_q_3 = X_pca_df["PC1"].quantile(0.99)

    # Create Altair plot for hierarchical clusters at height 72
    plot_df_height_72 = X_pca_df.copy()
    plot_df_height_72["h_cluster"] = pd.Series(
        clusters_at_72, index=X_pca_df.index
    ).astype(str)

    plot_df_height_72_trim = plot_df_height_72[
        (plot_df_height_72["PC1"] >= lower_q_3) &
        (plot_df_height_72["PC1"] <= upper_q_3)
    ].copy()

    chart_height_72 = alt.Chart(plot_df_height_72_trim).mark_circle(size=30, opacity=0.6).encode(
        x=alt.X("PC1:Q", title=f"PC1 ({variance_explained[0]:.1%} variance)"),
        y=alt.Y("PC2:Q", title=f"PC2 ({variance_explained[1]:.1%} variance)"),
        color=alt.Color("h_cluster:N", title="Hierarchical Cluster", scale=alt.Scale(scheme="category10")),
        tooltip=["PC1:Q", "PC2:Q", "h_cluster:N"]
    ).properties(
        title="Hierarchical Clustering – Cut at Height 72",
        width=650,
        height=520
    )

    chart_height_72
    return


@app.cell
def _(X, X_scaled, df, kmeans):
    # Assign KMeans labels to the original dataframe
    labels_km = kmeans.fit_predict(X_scaled)
    df1 = df.drop(columns=["cluster"], errors="ignore")
    df1.loc[X.index, "cluster"] = labels_km
    return (df1,)


@app.cell
def _(X, df1):
    # Check dtype
    print(df1.loc[X.index, "cluster"].dtype)

    # Check unique values
    print(df1.loc[X.index, "cluster"].unique())

    # Check for NaNs
    print(df1.loc[X.index, "cluster"].isna().sum())

    # Check types (should all be int)
    print(df1.loc[X.index, "cluster"].map(type).value_counts())
    return


@app.cell
def _(audio_features, df1):
    # Check audio feature dtypes
    df1[audio_features].dtypes
    return


@app.cell
def _(audio_features, df1, pd):
    # Convert audio features to numeric, coercing errors to NaN
    df1[audio_features] = df1[audio_features].apply(
        pd.to_numeric, errors="coerce"
    )
    return


@app.cell
def _(audio_features, df1):
    # Check for NaNs in audio features
    df1[audio_features].isna().sum()
    return


@app.cell
def _(X, audio_features, df1):
    # Create cleaned dataframe with audio features and cluster labels
    df_clean = df1.loc[X.index, audio_features + ["cluster"]]
    return (df_clean,)


@app.cell
def _(audio_features, df_clean):
    # Cluster means
    cluster_means = (
        df_clean
        .groupby("cluster")[audio_features]
        .mean()
    )

    cluster_means.round(2)
    return (cluster_means,)


@app.cell
def _(cluster_means):
    # Convert to z-scores across clusters (easier to see what is high/low per cluster)
    cluster_z = (cluster_means - cluster_means.mean()) / cluster_means.std()
    #cluster_z.round(2)

    print(cluster_z.round(2).to_markdown())
    return


@app.cell
def _(X, df1, valid_idx):
    # Assign playlist names and image prompts based on cluster labels
    df1.loc[valid_idx, "cluster"] = df1.loc[valid_idx, "cluster"].astype(int)

    playlist_names = {
        0: "Quiet Hours",
        1: "Feel-Good Grooves",
        2: "Urban Pulse",
        3: "Heavy After Hours"
    }

    playlist_images = {
        0: "Minimal desk, soft morning light, neutral tones, calm mood",
        1: "Warm sunset golden hour, bright colors, friends smiling",
        2: "City street at night, bold graffiti, energetic crowd, movement",
        3: "Dark concert stage, heavy metal band performing, distorted guitars, smoke, red and black lighting"
    }

    df1.loc[X.index, "playlist_name"] = df1.loc[X.index, "cluster"].map(playlist_names)
    df1.loc[X.index, "image_prompt"] = df1.loc[X.index, "cluster"].map(playlist_images)
    return


@app.cell
def _(X, X_scaled, centroids, df1, np, pairwise_distances, pd):
    # Ensure cluster exists for exactly X.index rows and is numeric
    df1.loc[X.index, "cluster"] = pd.to_numeric(df1.loc[X.index, "cluster"], errors="coerce")

    # Drop any rows that still have missing clusters 
    valid_idx = df1.loc[X.index, "cluster"].dropna().index

    # Recompute D only for valid rows
    D = pairwise_distances(X_scaled.loc[valid_idx].values, centroids)

    assigned = df1.loc[valid_idx, "cluster"].astype(int).to_numpy()

    dist_to_own = D[np.arange(D.shape[0]), assigned]

    df1.loc[valid_idx, "dist_to_centroid"] = dist_to_own
    return (valid_idx,)


@app.cell
def _(df1, pd, valid_idx):
    # For each playlist, get top 5 unique artists closest to centroid
    ranked = (
        df1.loc[valid_idx]
          .sort_values("dist_to_centroid")
    )
    ranked_unique_artists = (
        ranked
          .groupby(["playlist_name", "artist"], as_index=False)
          .head(1)
    )
    samples_unique = (
        ranked_unique_artists
          .groupby(["cluster", "playlist_name"], as_index=False)
          .head(5)
          [["cluster", "playlist_name", "name", "artist", "html"]]
          .sort_values(["cluster"])
    )
    pd.set_option("display.max_colwidth", None)

    samples_unique
    return


@app.cell
def _(df, mo, pd):
    # Interactive controls: number of clusters, artist and song filters
    k_slider = mo.ui.slider(
        start=2,
        stop=10,
        value=4,
        step=1,
        label="Number of clusters (k)",
    )

    artist_options = ["All"] + sorted(pd.Series(df["artist"]).dropna().unique().tolist())
    artist_dropdown = mo.ui.dropdown(
        options=artist_options,
        value="All",
        label="Artist",
    )

    song_options = ["All"] + sorted(pd.Series(df["name"]).dropna().unique().tolist())
    song_dropdown = mo.ui.dropdown(
        options=song_options,
        value="All",
        label="Song",
    )
    return artist_dropdown, k_slider, song_dropdown


@app.cell
def _(
    KMeans,
    PCA,
    X_scaled,
    alt,
    artist_dropdown,
    df,
    k_slider,
    np,
    pairwise_distances,
    pd,
    song_dropdown,
):
    # Recompute k-means with selected k and build PCA scatterplot for filtered selection
    k_1 = int(k_slider.value)

    # Fit KMeans on the scaled features (full dataset) for the requested k
    kmeans_3 = KMeans(n_clusters=k_1, random_state=42, n_init=10)
    labels_k1 = kmeans_3.fit_predict(X_scaled)

    df_local_1 = df.copy()
    df_local_1.loc[X_scaled.index, "cluster"] = labels_k1

    # PCA transform for visualization
    pca_1 = PCA(n_components=2, random_state=42)
    X_pca_1 = pca_1.fit_transform(X_scaled)
    X_pca_df_int = pd.DataFrame(X_pca_1, columns=["PC1", "PC2"], index=X_scaled.index)
    X_pca_df_int["cluster"] = df_local_1.loc[X_pca_df_int.index, "cluster"].astype(str)

    # Apply filters for display
    mask_int = pd.Series(True, index=X_pca_df_int.index)
    if artist_dropdown.value != "All":
        mask_int &= df_local_1.loc[X_pca_df_int.index, "artist"] == artist_dropdown.value
    if song_dropdown.value != "All":
        mask_int &= df_local_1.loc[X_pca_df_int.index, "name"] == song_dropdown.value

    plot_df_int = X_pca_df_int[mask_int].copy()

    variance_explained_1 = pca_1.explained_variance_ratio_

    alt.data_transformers.disable_max_rows()

    points_int = alt.Chart(plot_df_int).mark_circle(size=60, opacity=0.7).encode(
        x=alt.X('PC1:Q', title=f'PC1 ({variance_explained_1[0]:.1%} variance)'),
        y=alt.Y('PC2:Q', title=f'PC2 ({variance_explained_1[1]:.1%} variance)'),
        color=alt.Color('cluster:N', title='Cluster', scale=alt.Scale(scheme='category10')),
        tooltip=['PC1:Q', 'PC2:Q', 'cluster:N']
    )

    centroids_1 = kmeans_3.cluster_centers_
    centroids_pca_1 = pca_1.transform(centroids_1)
    centroids_df_int = pd.DataFrame(centroids_pca_1, columns=["PC1", "PC2"]) 
    centroids_df_int["cluster"] = centroids_df_int.index.astype(str)

    centroids_plot_int = alt.Chart(centroids_df_int).mark_point(
        shape='cross',
        size=300,
        filled=True,
        strokeWidth=3
    ).encode(
        x='PC1:Q',
        y='PC2:Q',
        color=alt.Color('cluster:N', scale=alt.Scale(scheme='category10')),
        tooltip=['PC1:Q', 'PC2:Q', 'cluster:N']
    )

    chart_int = (points_int + centroids_plot_int).properties(
        title='K-Means Clusters (interactive)',
        width=700,
        height=520
    )

    # For the (filtered) subset, compute distance to centroids and pick top examples per cluster
    if plot_df_int.shape[0] > 0:
        idx_int = plot_df_int.index
        D_int = pairwise_distances(X_scaled.loc[idx_int].values, centroids_1)
        assigned_int = df_local_1.loc[idx_int, "cluster"].astype(int).to_numpy()
        dist_to_own_int = D_int[np.arange(D_int.shape[0]), assigned_int]
        df_examples_int = df_local_1.loc[idx_int].copy()
        df_examples_int["dist_to_centroid"] = dist_to_own_int

        top_examples_int = (
            df_examples_int.sort_values("dist_to_centroid").groupby("cluster").head(5)[
                ["cluster", "name", "artist", "html"]
            ]
        )
    else:
        top_examples_int = pd.DataFrame(columns=["cluster", "name", "artist", "html"])
    return chart_int, top_examples_int


@app.cell
def _():
    return


@app.cell
def _(
    artist_dropdown,
    chart_int,
    k_slider,
    mo,
    song_dropdown,
    top_examples_int,
):
    mo.vstack([
        mo.md("### 🎵 Interactive Cluster Dashboard"),
        mo.callout(
            mo.vstack([
                mo.md("**Filter Controls**"),
                mo.hstack([k_slider, artist_dropdown, song_dropdown], gap=2)
            ]),
            kind="neutral"
        ),
        chart_int,
        mo.md("#### Top Representative Songs per Cluster"),
        top_examples_int
    ])
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
