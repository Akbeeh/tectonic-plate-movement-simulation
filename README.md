# Tectonic Plate Movement Simulation

This project focuses on the use of GeoJSON to do a simulation of tectonic plate movements.

Help from [GeoJSON docs](https://geojson.readthedocs.io/en/latest/) and [GeoPandas docs](https://geopandas.org/en/stable/docs.html).

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

Here, we create a `TectonicPlateSimulator` class with all the functions we need to simulate the tectonic plates movements.
For the movement of the tectonic plates, we use the `shapely` library, more precisely the `translate` function.

### 3. Write functions to visualize the simulation

To visualize the simulation, we simply use `matplotlib` and `geopandas` to plot the tectonic plates.

### Where I got a bit stuck / Interesting points

- http://geojson.xyz/ and http://geojson.io/ are great to visualize, create and download GeoJSON files.
- One of the main issues I had was to find a way to create polygons without having them touching each other at the beginning.
- One other was to dispatch the tectonic plates all over the world map.

### Extra: Setup of pre-commit

```bash
pip install pre-commit
```

Once the `.pre-commit-config.yaml` completed, we need to set up the git hooks scripts.

```bash
pre-commit install
```
