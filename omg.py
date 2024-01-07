class TSPInstance:
    def __init__(self):
        self.name = None
        self.comment = None
        self.type = None
        self.dimension = None
        self.edge_weight_type = None
        self.node_coordinates = {}  # Dicionário para armazenar as coordenadas dos nós
        self.tour_solution = []     # Lista para armazenar a solução do caixeiro viajante

    def read_instance_from_file(self, file_path):
        with open(file_path, 'r') as file:
            section = None
            for line in file:
                line = line.strip()
                if not line:
                    continue

                if line.startswith("NODE_COORD_SECTION"):
                    section = "NODE_COORD_SECTION"
                    continue
                elif line.startswith("TOUR_SECTION"):
                    section = "TOUR_SECTION"
                    continue
                elif line.startswith("EOF"):
                    break

                if section == "NODE_COORD_SECTION":
                    node_data = line.split()
                    node_num, x, y = map(int, node_data)
                    self.node_coordinates[node_num] = (x, y)
                elif section == "TOUR_SECTION":
                    if line == "-1":
                        break
                    node_num = int(line)
                    self.tour_solution.append(node_num)

    def __str__(self):
        return f"TSP Instance: {self.name}, Dimension: {self.dimension}, Edge Weight Type: {self.edge_weight_type}"


# Exemplo de uso:
file_path = "att48.tsp.txt"
tsp_instance = TSPInstance()
tsp_instance.read_instance_from_file(file_path)

print(tsp_instance)
print("Node Coordinates:", tsp_instance.node_coordinates)
print("Tour Solution:", tsp_instance.tour_solution)
