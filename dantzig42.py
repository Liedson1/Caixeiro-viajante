import networkx as nx
import matplotlib.pyplot as plt

class TSPBase:
    def __init__(self):
        self.name = None
        self.comment = None
        self.type = None
        self.dimension = None
        self.edge_weight_type = None
        self.node_coordinates = {}
        self.graph = nx.Graph()

    def read_instance_from_file(self, file_path):
        raise NotImplementedError("Subclasses must implement this method.")

    def calculate_distance(self, coord1, coord2):
        return ((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2) ** 0.5

    def plot_graph(self):
        pos = nx.get_node_attributes(self.graph, 'pos')
        nx.draw(self.graph, pos, with_labels=True, font_weight='bold')
        labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels)
        plt.show()

    def find_tsp_path_length(self):
        # Encontrar o caminho mínimo usando o algoritmo TSP
        tsp_path = nx.approximation.traveling_salesman_problem(self.graph, weight='weight', cycle=True)
        tsp_length = sum(self.graph[i][j]['weight'] for i, j in zip(tsp_path, tsp_path[1:]))
        return tsp_length

class TSPInstance(TSPBase):
    def read_instance_from_file(self, file_path):
        with open(file_path, 'r') as file:
            section = None
            for line in file:
                line = line.strip()
                if not line:
                    continue

                if line.startswith("EDGE_WEIGHT_TYPE"):
                    self.edge_weight_type = line.split(":")[1].strip()
                elif line.startswith("NODE_COORD_SECTION"):
                    section = "NODE_COORD_SECTION"
                    continue
                elif line.startswith("DISPLAY_DATA_SECTION"):
                    section = "DISPLAY_DATA_SECTION"
                    continue
                elif line.startswith("EOF"):
                    break

                if section == "NODE_COORD_SECTION":
                    node_data = line.split()
                    if len(node_data) != 3:
                        continue  # Ignora linhas que não contêm coordenadas
                    node_num, x, y = map(int, node_data[0:3])
                    self.node_coordinates[node_num] = (x, y)
                    self.graph.add_node(node_num, pos=(x, y))
                elif section == "DISPLAY_DATA_SECTION":
                    node_data = line.split()
                    node_num, x, y = int(node_data[0]), float(node_data[1]), float(node_data[2])
                    if node_num not in self.node_coordinates:
                        self.node_coordinates[node_num] = (x, y)
                        self.graph.add_node(node_num, pos=(x, y))

            # Adiciona as arestas com base nas coordenadas dos nós
            for i in self.node_coordinates:
                for j in self.node_coordinates:
                    if i != j:
                        distance = self.calculate_distance(self.node_coordinates[i], self.node_coordinates[j])
                        self.graph.add_edge(i, j, weight=distance)

# Exemplo de uso:
file_path = "dantzig42.tsp.txt"
tsp_instance = TSPInstance()
tsp_instance.read_instance_from_file(file_path)

print(tsp_instance)
print("Node Coordinates:", tsp_instance.node_coordinates)

# Encontrar o comprimento do caminho mínimo
tsp_length = tsp_instance.find_tsp_path_length()
print("The minimal tour length:", tsp_length)

# Exibir o grafo (opcional)
tsp_instance.plot_graph()
