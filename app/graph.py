import base64
from io import BytesIO
import networkx as nx
import matplotlib.pyplot as plt


def build_graph(graph_data: dict) -> nx.Graph:
    graph = nx.Graph()
    graph.add_nodes_from(graph_data['nodes'])

    edge_tuples = []
    for edge in graph_data['edges']:
        edge_tuples.append(edge.values())
    graph.add_edges_from(edge_tuples)
    return graph


def get_graph_image(graph: nx.Graph) -> str:
    buf = BytesIO()
    plt.figure(figsize=(3, 3))
    pos = nx.spring_layout(graph, k=1, iterations=50)

    nx.draw_networkx_nodes(
        graph, pos, 
        node_size=800, 
        node_color='lightblue',
        edgecolors='black',
        linewidths=0.5
    )
    nx.draw_networkx_edges(
        graph, pos, 
        edge_color='black',
        width=0.5
    )
    nx.draw_networkx_labels(
        graph, pos, 
        font_size=10, 
    )
    
    plt.axis('off')
    plt.tight_layout()
    
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    plt.close()
    
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{image_base64}"