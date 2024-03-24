# Geographical Pathfinding Application

This Python application uses the A* algorithm to find the shortest path between cities. It leverages geographic data in GeoJSON format to construct a graph, with cities as nodes and distances as weighted edges.

## Features

- Load city data from a GeoJSON file.
- Utilize A* pathfinding algorithm to calculate the shortest path.
- Visualize the shortest path on a map with matplotlib.

## Installation

Ensure that you have the following Python libraries installed:

- `geopandas`: For handling GeoJSON files and geospatial data.
- `networkx`: For creating and manipulating the graph structure.
- `matplotlib`: For plotting and visualizing data.
- `pickle`: For saving and loading the graph structure.

## Usage

Run `V1.py` to start the application. The script performs the following steps:

1. It loads geographic data from the provided `map.geojson` file and constructs a graph.
2. It uses the A* algorithm to find the shortest path between two hardcoded cities (which can be changed in the script).
3. It visualizes this path on a map, saving the plot as `path.png`.

To visualize a path between different cities, modify the `start_city` and `end_city` variables in the script.

## Visualizing the Path

The path visualization is handled by the `visualize_path` function, which creates a map plot showing the cities as blue points and the shortest path as red lines between them.

## Acknowledgements

This project is made possible thanks to the open-source community and the various libraries used.

