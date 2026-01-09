## Global Happiness Ordination: Principal Component Analysis

| Name      | Contribution                         |
|:----------|:-------------------------------------|
|Assad      | Analysis & Report |
|Stefan     | Analysis                |
|Zeyad     | Analysis with 3 clusters as a comparison     |
|Shiva      |
|Sumeet     |                |

---

## Executive Summary

This report analyzes how data-driven methods can support the editorial process of playlist creation. Using Spotify audio features such as energy, valence, and danceability, songs were grouped based on their sonic characteristics rather than traditional genre labels.

K-means clustering identified four distinct musical moods, which were explored and validated using PCA visualizations and hierarchical clustering dendrograms. These clusters were curated into four playlists: **Quiet Hours**, **Feel-Good Grooves**, **Urban Pulse**, and **Heavy After Hours**. Tracks were selected based on how well they represented each cluster, with basic editorial choices such as artist diversity applied.

---

## Dataset Overview

| **Item**                | **Description**                                                                    |
|-------------------------|------------------------------------------------------------------------------------|
| **Dataset Name**        | Spotify 5000 songs                                                           |
| **Number of Rows**      | 5,235                                                                                |
| **Number of Columns**   | 17                                                                                  |
| **File Format**         | `.csv`                                                                             |
| **Source (Name)**       | Github                                                                             |
| **Source Link**         | https://github.com/datagus/ASDA2025/blob/main/datasets/homework_week11/6.3.3_spotify_5000_songs.csv   |
| **Date Accessed**       | 08 Jan 2026                                                                   |


## K Means Clustering



### 1. Feature Selection & Scaling

| Audio Feature | Description |
|--------------|------------|
| Danceability | How suitable a track is for dancing, based on rhythm and tempo |
| Energy | Perceived intensity and activity of a track |
| Loudness | Overall loudness of a track in decibels (dB) |
| Speechiness | Presence of spoken words (higher values indicate rap or talk-heavy tracks) |
| Acousticness | Likelihood that a track is acoustic |
| Instrumentalness | Likelihood that a track contains no vocals |
| Liveness | Presence of a live audience or performance |
| Valence | Musical positivity (higher values sound happier) |
| Tempo | Speed of the track measured in beats per minute (BPM) |
| Duration (ms) | Length of the track in milliseconds |

### 2. Determining number of clusters


![11.DeterminingK.png](../additional_material/figures/11.DeterminingK.png)



### 3. Visualization through PCA and Dendrograms 


![11.BiplotKmeans.png](../additional_material/figures/11.BiplotKmeans.png)

![11.Dendrogram.png](../additional_material/figures/11.Dendrogram.png)

![11.HierarchicalClustering.png](../additional_material/figures/11.HierarchicalClustering.png)






## Results

|   cluster | danceability | energy | loudness | speechiness | acousticness | instrumentalness | liveness | valence | tempo |   duration_ms |
|----------:|---------------:|---------:|-----------:|--------------:|---------------:|-------------------:|-----------:|----------:|--------:|--------------:|
|         0 |        -0.69 |  -1.44 |    -1.49 |       -0.71 |         1.46 |             0.97 |    -1.32 |   -0.91 | -1.49 |        1.38 |
|         1 |         0.76 |   0.2  |     0.48 |       -0.6  |        -0.25 |            -0.83 |    -0.22 |    0.94 |  0.33 |       -0.82 |
|         2 |         0.95 |   0.37 |     0.62 |        1.45 |        -0.4  |            -0.89 |     0.83 |    0.79 |  0.66 |       -0.65 |
|         3 |        -1.02 |   0.87 |     0.39 |       -0.15 |        -0.81 |             0.75 |     0.71 |   -0.81 |  0.5  |        0.08 |



### Quiet Hours


<p align="left">
  <img src="../additional_material/figures/Playlist1.png" width="320">
</p>


**Playlist Description**: *Soft instrumentals and acoustic sounds for slowing down and clearing your head. Ideal for quiet mornings, focused work, or moments when you just want some calm in the background.*<br>
**Playlist Link**: [Listen to Quiet Hours on Spotify!](https://open.spotify.com/playlist/46Ql2b9cTdGhhHbzPyGPjN?si=JzH7fujNS5q4_pzwDDgSPg) <br>
**Sample Songs & Artists**:

| Song                          | Artist          |
|:------------------------------|:----------------|
| Before You Go - Piano Version | Flying Fingers  |
| Saku                          | Susumu Yokota   |
| The Unforgettable             | Dirk Maassen    |
| Violão Vadio                  | Raphael Rabello |
| Young And Foolish             | Bill Evans      |


### Feel-Good Grooves


<p align="left">
  <img src="../additional_material/figures/Playlist2.png" width="320">
</p>


**Playlist Description**: *Easygoing, upbeat tracks that lift your mood without trying too hard. Press play when you want something light, positive, and effortlessly feel-good.*<br>
**Playlist Link**: [Listen to Feel-Good Grooves on Spotify!](https://open.spotify.com/playlist/1FMIxKi50vaIdjXXpCJu5p?si=57RF7OAES3-wyFZ0yEAOIw)<br>
**Sample Songs & Artists**:

| Song                                      | Artist               |
|:------------------------------------------|:---------------------|
| Guerrera                                  | DELLAFUENTE          |
| I Got You Babe                            | Sonny & Cher         |
| I Guess That's Why They Call It The Blues | Elton John           |
| Lass mich nie mehr los - Studio Version   | Sportfreunde Stiller |
| Waiting For Love                          | Avicii               |

### Urban Pulse

<p align="left">
  <img src="../additional_material/figures/Playlist3.png" width="320">
</p>

**Playlist Description**: *Rhythmic, voice-driven tracks with a strong sense of movement and flow. A soundtrack for city nights, long walks, or whenever you want a bit of urban energy.*<br>
**Playlist Link**: [Listen to Urban Pulse on Spotify!](https://open.spotify.com/playlist/37DZ1WoxhFklk6A4KQmpbA?si=3dkB5VibRoWbC6fjCduupg)<br>
**Sample Songs & Artists**:

|Song                    | Artist       |
|:-----------------------|:-------------|
| Bring Em Out - Amended | T.I.         |
| Der Himmel soll warten | Sido         |
| Freak                  | R3HAB        |
| Gravel Pit             | Wu-Tang Clan |
| We Fly High            | Jim Jones    |

### Heavy After Hours


<p align="left">
  <img src="../additional_material/figures/Playlist4.png" width="320">
</p>

**Playlist Description**: *Dark, loud, and intense tracks made for late nights and turned-up volumes. Perfect when you want something heavy, raw, and unapologetic.*<br>
**Playlist Link**: [Listen to Heavy After Hours on Spotify!](https://open.spotify.com/playlist/04QIYwQGxI3pIbIHyVUofg?si=eorewadPRgySlCmpHYzlcQ)<br>
**Sample Songs & Artists**:

| Song                   | Artist      |
|:------------------------|:------------|
| Forsaken                | Entombed    |
| Frozen Soul             | Asphyx      |
| Ridden with Disease     | Autopsy     |
| The Secrecies of Horror | Pestilence  |
| Without Sin             | Morta Skuld |

## AI Disclaimer
- Use of Visual Studio / PyCharm with Github copilot (inline code suggestions) 
- AI was used to compile playlist images
 