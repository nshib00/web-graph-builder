import base64
from io import BytesIO
import networkx as nx
import matplotlib

matplotlib.use('Agg')  # бэкенд matplotlib без GUI, используется для ускорения отрисовки

import matplotlib.pyplot as plt


def build_graph(graph_data: dict) -> nx.Graph:
    graph = nx.Graph()
    graph.add_nodes_from(graph_data['nodes'])
    edges = (tuple(edge.values()) for edge in graph_data['edges'])
    graph.add_edges_from(edges)
    return graph


def write_graph_in_bytes(graph: nx.Graph, longest_path: list[int]) -> BytesIO:
    buffer = BytesIO()
    plt.figure(figsize=(5, 3), dpi=60)
    pos = nx.spring_layout(graph, k=1, iterations=50)

    nx.draw_networkx_nodes(
        graph, pos, 
        node_size=800, 
        node_color='lightblue',
        edgecolors='black',
        linewidths=0.3
    )
    nx.draw_networkx_edges(
        graph, pos, 
        edge_color='black',
        width=0.3
    )
    nx.draw_networkx_labels(
        graph, pos, 
        font_size=12, 
    )

    if longest_path:
        nx.draw_networkx_nodes(
            graph, pos,
            nodelist=longest_path,
            node_size=800,
            node_color='orange',
            edgecolors='darkorange',
            linewidths=1
        )
    path_edges = []
    for i in range(len(longest_path) - 1):
        path_edges.append((longest_path[i], longest_path[i + 1]))
    nx.draw_networkx_edges(
        graph, pos,
        edgelist=path_edges, 
        edge_color='darkorange',
        width=1
    )  

    plt.axis('off')
    plt.tight_layout(pad=0.1) 
    plt.margins(0.1)
    plt.savefig(buffer, format='png', dpi=150)
    plt.close()

    buffer.seek(0)
    return buffer


def get_graph_image(graph: nx.Graph) -> str:
    buffer = write_graph_in_bytes(
        graph=graph,
        longest_path=find_longest_path(graph)
    )
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{image_base64}"


def find_longest_path(graph: nx.Graph):
    if not graph.nodes:
        return []
    
    longest_path = []
    
    for start_node in graph.nodes:
        visited = set()
        current_path = []
        
        def dfs(node):
            nonlocal current_path, longest_path
            visited.add(node)
            current_path.append(node)
            
            if len(current_path) > len(longest_path):
                longest_path = current_path.copy()
            
            for neighbor in graph.neighbors(node):
                if neighbor not in visited:
                    dfs(neighbor)
            
            visited.remove(node)
            current_path.pop()
        
        dfs(start_node)
    
    return longest_path
