from collections import deque
import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    def __init__(self):
        pass
    
    def gen_DiGraph(self, rows, rows2):
        try:
            G = nx.DiGraph()
            nodes = set()

            for row in rows:
                node1 = (row[1])
                if node1 not in nodes:
                    nodes.add(node1)
                if not rows2:
                    node2 = (row[3])
                    if node2 not in nodes: 
                        nodes.add(node2)
            
            G.add_nodes_from(nodes)

            if rows2:
                for row in rows2:
                    node1 = (row[1])
                    node2 = (row[3])
                    if node1 in nodes and node2 in nodes:
                        G.add_edge(node1, node2)
            else:
                for row in rows:
                    node1 = (row[1])
                    node2 = (row[3])
                    G.add_edge(node1, node2)

            return G
        
        except Exception as e:
            print(f"Error g: {e}")
            return None

    def view_graph(self, G):
        nx.draw(G, with_labels=True, node_color='lightblue', font_weight='bold')
        plt.show()

    def bfs(self, G, start_node):
        visited = set()
        queue = deque([(start_node, 0)])
        max_level = 0
        
        while queue:
            node, level = queue.popleft()
            
            if node not in visited:
                visited.add(node)
                max_level = max(max_level, level)
                
                for neighbor in G.neighbors(node):
                    if neighbor not in visited:
                        queue.append((neighbor, level + 1))
        
        return max_level
    