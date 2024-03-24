from math import radians, sin, cos, sqrt, atan2
import geopandas as gpd
import networkx as nx
import pickle
import matplotlib.pyplot as plt
import time


def visualize_path(gdf, path):
    fig, ax = plt.subplots(figsize=(10, 10))

    gdf.plot(ax=ax, color='blue', markersize=50)

    for i in range(len(path) - 1):
        source, target = path[i], path[i + 1]
        source_coords = (gdf[gdf['asciiname'] == source]['geometry'].y.values[0],
                         gdf[gdf['asciiname'] == source]['geometry'].x.values[0])
        target_coords = (gdf[gdf['asciiname'] == target]['geometry'].y.values[0],
                         gdf[gdf['asciiname'] == target]['geometry'].x.values[0])

        ax.plot([source_coords[1], target_coords[1]], [source_coords[0], target_coords[0]], color='red', linewidth=2)

    plt.title('Shortest Path between Cities')
    plt.savefig("path.png")
    plt.show()


def a_star_algorithm(graph, start, end):
    try:
        path = nx.astar_path(graph, start, end, heuristic=Distance)
        return path
    except nx.NetworkXNoPath:
        print(f"No path found between {start} and {end}.")
        return None


def create_graph_from_geojson(file_path):
    gdf = gpd.read_file(file_path)

    G = nx.Graph()

    for idx, row in gdf.iterrows():
        lon, lat = row['geometry'].x, row['geometry'].y
        G.add_node(row['asciiname'], pos=(lon, lat))

    graph_file = 'graph.pkl'
    try:
        with open(graph_file, 'rb') as f:
            G = pickle.load(f)
            print("Graph loaded")
    except FileNotFoundError:
        print("Graph file not found, creating a new graph")

        for idx, row in gdf.iterrows():
            print(idx)
            close_cities = find_cities_within_distance(gdf, row['asciiname'], 20.0, 10)

            for close_city in close_cities:
                distance = Distance(
                    (row['geometry'].y, row['geometry'].x),
                    (gdf[gdf['asciiname'] == close_city]['geometry'].y.values[0],
                     gdf[gdf['asciiname'] == close_city]['geometry'].x.values[0])
                )
                G.add_edge(row['asciiname'], close_city, weight=distance)

        with open(graph_file, 'wb') as f:
            pickle.dump(G, f)

    return G, gdf


def find_cities_within_distance(gdf, city, distance, num_closest):
    close_cities = []

    for idx, row in gdf.iterrows():
        if row['asciiname'] != city:
            distance_to_city = Distance(
                (gdf[gdf['asciiname'] == city]['geometry'].y.values[0],
                 gdf[gdf['asciiname'] == city]['geometry'].x.values[0]),
                (row['geometry'].y, row['geometry'].x)
            )
            if distance_to_city < distance:
                close_cities.append((row['asciiname'], distance_to_city))

    close_cities = sorted(close_cities, key=lambda x: x[1])[:num_closest]

    close_cities = [city[0] for city in close_cities]

    if not close_cities:
        nearest_neighbors = find_nearest_neighbors(gdf, city, num_closest)
        close_cities.extend(nearest_neighbors)

    return close_cities


def Distance(coord1, coord2):
    try:
        lat1, lon1 = radians(coord1[0]), radians(coord1[1])
        lat2, lon2 = radians(coord2[0]), radians(coord2[1])

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        radius = 6371.0

        distance = radius * c
        return distance
    except (ValueError, TypeError):
        return float('inf')


def find_nearest_neighbors(gdf, city, num_neighbors):
    neighbors = []

    for idx, row in gdf.iterrows():
        if row['asciiname'] != city:
            distance = Distance(
                (gdf[gdf['asciiname'] == city]['geometry'].y.values[0],
                 gdf[gdf['asciiname'] == city]['geometry'].x.values[0]),
                (row['geometry'].y, row['geometry'].x)
            )
            neighbors.append((row['asciiname'], distance))

    neighbors = sorted(neighbors, key=lambda x: x[1])[:num_neighbors]

    neighbors = [neighbor[0] for neighbor in neighbors]

    return neighbors


def find_nearest_neighbor(gdf, city):
    neighbors = find_nearest_neighbors(gdf, city, 1)
    return neighbors[0] if neighbors else None


file_path = 'map.geojson'
graph, gdf = create_graph_from_geojson(file_path)
start_city = 'Prague'
end_city = 'Kynsperk nad Ohri'

if graph:
    startCas = time.time()
    shortest_path = a_star_algorithm(graph, start_city, end_city)
    print("Cas hledani:", round((time.time()-startCas)*1000,2), "ms")
    if shortest_path:
        path_length = sum(graph.get_edge_data(shortest_path[i], shortest_path[i + 1])['weight'] for i in
                          range(len(shortest_path) - 1))

        print('Shortest Path:', shortest_path)
        print('Length of the Path:', round(path_length, 1), "km")
        visualize_path(gdf, shortest_path)
