import networkx as nx
from pyvis.network import Network
import requests
import time

class GitHubNetworkGraph:
    """
    A class to model and visualize GitHub social connectivity 
    using Graph Theory principles.
    """
    def __init__(self, api_token=None):
        self.G = nx.Graph()  # Initializing an Undirected Graph
        self.headers = {'Authorization': f'token {api_token}'} if api_token else {}
        self.api_base = "https://api.github.com/users/"

    def fetch_followers(self, username):
        """Retrieves follower data via GitHub API."""
        url = f"{self.api_base}{username}/followers"
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return [user['login'] for user in response.json()]
            return []
        except Exception as e:
            print(f"Error fetching data: {e}")
            return []

    def build_adjacency_map(self, root_user, depth_limit=10):
        """
        Implements Adjacency-based mapping to build the network.
        Nodes: User Accounts | Edges: Follower Relationships
        """
        # Add the central node (Root)
        self.G.add_node(root_user, label=root_user, title="Primary Node", color='#ff4d4d')
        
        followers = self.fetch_followers(root_user)[:depth_limit]

        for follower in followers:
            # Add secondary nodes and create edges (Connectivity)
            self.G.add_node(follower, label=follower, title="Follower")
            self.G.add_edge(root_user, follower)
            
            # Artificial delay to respect API rate limits
            time.sleep(0.1)

    def generate_visualization(self, output_file="network_map.html"):
        """Converts the NetworkX graph into an interactive Pyvis HTML map."""
        net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")
        net.from_nx(self.G)
        
        # Configure physics for better graph distribution
        net.toggle_physics(True)
        net.save_graph(output_file)
        print(f"Graph successfully rendered to {output_file}")
