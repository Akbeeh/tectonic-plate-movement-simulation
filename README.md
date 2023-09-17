# Tectonic Plate Movement Simulation

This project focuses on the use of GeoJSON to do a simulation of tectonic plate movements.

Help from:

- [GeoJSON docs](https://geojson.readthedocs.io/en/latest/)
- [GeoPandas docs](https://geopandas.org/en/stable/docs.html)
- [Shapely docs](https://shapely.readthedocs.io/en/latest/manual.html)
- [Matplotlib docs](https://matplotlib.org/stable/contents.html)

## Overview

This project dives into the creation of a simulation of tectonic plate movements within a 2D world map. We'll use GeoJSON to represent the tectonic plates and simulate their movements. When two tectonic plates collide, they will move in opposite directions.

## Steps followed

### 0. Installation & Setup

```bash
# Install required librairies
pip install geojson geopandas
```

### 1. Initialize the World Map

Here, we initiate with `TectonicPlateGenerator` class with all the functions we need to create the tectonic plates.
In the end, we have two files: `geojson_map.py` and `world_map.geojson`.

### 2. Create Python file to perform movement simulation

Here, we create a `TectonicPlateSimulator` class with all the functions we need to simulate the tectonic plates movements, contained in the `geopandas_map.py` file.

For the movement of the tectonic plates, we use the `shapely` library, more precisely the `translate` function.

### 3. Determine the interactions between the tectonic plates (collisions) and the boundaries of the world map

To check if there is a collision between two tectonic plates, we use the `intersects` function from `shapely`.

### 4. Write functions to visualize the simulation

To visualize the simulation, we simply use `matplotlib` and `geopandas` to plot the tectonic plates.

### Where I got a bit stuck / Interesting points

- http://geojson.xyz/ and http://geojson.io/ are great to visualize, create and download GeoJSON files.
- One of the main issues I had was to find a way to create polygons without having them touching each other at the beginning.
- One other was to dispatch the tectonic plates all over the world map.
- **[QUESTION]** - When updating the data (i.e. the tectonic plate positions), the _figsize_ of the plot changes. I don't know why and I couldn't find a way to fix it, even by setting the _figsize_ in the `plt.figure()` function.

### Extra: Setup of pre-commit

```bash
pip install pre-commit
```

Once the `.pre-commit-config.yaml` completed, we need to set up the git hooks scripts.

```bash
pre-commit install
```
