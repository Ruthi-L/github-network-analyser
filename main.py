from graph_engine import GitHubNetworkGraph

def run_analysis():
    print("--- GitHub Social Network Analyzer ---")
    user_to_analyze = input("Enter a GitHub username to map: ")
    
    # Initialize the engine
    # Note: For research, a Personal Access Token is recommended to avoid rate limits
    engine = GitHubNetworkGraph()
    
    print(f"Building graph for {user_to_analyze}...")
    engine.build_adjacency_map(user_to_analyze, depth_limit=15)
    
    # Generate the output
    engine.generate_visualization("github_social_graph.html")
    print("Process complete.")

if __name__ == "__main__":
    run_analysis()
