class TSPInstance:
    def __init__(self, name, dimension, edge_weight_type, edge_weight_format, node_coord_type, display_data_type, edge_weights, tour=None):
        self.name = name
        self.dimension = dimension
        self.edge_weight_type = edge_weight_type
        self.edge_weight_format = edge_weight_format
        self.node_coord_type = node_coord_type
        self.display_data_type = display_data_type
        self.edge_weights = edge_weights
        self.tour = tour

def read_tsp_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    dimension_line = next(line for line in lines if line.startswith("DIMENSION"))
    dimension = int(dimension_line.split(":")[1].strip())

    edge_weight_type_line = next(line for line in lines if line.startswith("EDGE_WEIGHT_TYPE"))
    edge_weight_type = edge_weight_type_line.split(":")[1].strip()

    edge_weight_format_line = next((line for line in lines if line.startswith("EDGE_WEIGHT_FORMAT")), None)
    edge_weight_format = edge_weight_format_line.split(":")[1].strip() if edge_weight_format_line else None

    node_coord_type_line = next((line for line in lines if line.startswith("NODE_COORD_TYPE")), None)
    node_coord_type = node_coord_type_line.split(":")[1].strip() if node_coord_type_line else None

    display_data_type_line = next((line for line in lines if line.startswith("DISPLAY_DATA_TYPE")), None)
    display_data_type = display_data_type_line.split(":")[1].strip() if display_data_type_line else None

    edge_weights = []

    if "EDGE_WEIGHT_SECTION" in lines:
        edge_weight_section_start = lines.index("EDGE_WEIGHT_SECTION\n") + 1
        edge_weight_section_end = None

        for i in range(edge_weight_section_start, len(lines)):
            if "EOF" in lines[i]:
                edge_weight_section_end = i
                break

        if edge_weight_section_end is None:
            edge_weight_section_end = len(lines)

        edge_weights = [list(map(int, line.split())) for line in lines[edge_weight_section_start:edge_weight_section_end] if line.strip()]

    elif edge_weight_format == "FULL_MATRIX":
        edge_weight_section_start = lines.index("EDGE_WEIGHT_SECTION\n") + 1

        # Encontrar o final da seção de pesos das arestas
        edge_weight_section_end = None
        for i in range(edge_weight_section_start, len(lines)):
            if "EOF" in lines[i]:
                edge_weight_section_end = i
                break

        if edge_weight_section_end is None:
            edge_weight_section_end = len(lines)

        # Extrair a parte inferior do triângulo da matriz
        edge_weights = []
        for i in range(edge_weight_section_start, edge_weight_section_end):
            row = list(map(int, lines[i].split()))
            edge_weights.extend(row)

    tsp_data = TSPInstance(
        name=lines[1].split(":")[1].strip(),
        dimension=dimension,
        edge_weight_type=edge_weight_type,
        edge_weight_format=edge_weight_format,
        node_coord_type=node_coord_type,
        display_data_type=display_data_type,
        edge_weights=edge_weights
    )

    if "TOUR_SECTION" in lines:
        tour_start_index = lines.index("TOUR_SECTION\n") + 1
        tour_end_index = lines.index("-1\n", tour_start_index) if "-1\n" in lines[tour_start_index:] else len(lines)
        tsp_data.tour = list(map(int, lines[tour_start_index:tour_end_index]))

    return tsp_data

# Exemplo de uso:
file_path = "p01.tsp.txt"
tsp_instance = read_tsp_file(file_path)

# Acessando os dados
print(f"Nome: {tsp_instance.name}")
print(f"Dimensão: {tsp_instance.dimension}")
print(f"Tipo de Peso das Arestas: {tsp_instance.edge_weight_type}")
print(f"Formato do Peso das Arestas: {tsp_instance.edge_weight_format}")
print(f"Tipo de Coordenadas dos Nós: {tsp_instance.node_coord_type}")
print(f"Tipo de Dados de Exibição: {tsp_instance.display_data_type}")
print(f"Pesos das Arestas: {tsp_instance.edge_weights}")
print(f"Tour: {tsp_instance.tour}")
