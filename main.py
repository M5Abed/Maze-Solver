"""
AI Maze Solver - Main Application

Interactive maze solver demonstrating classical AI search algorithms:
- Breadth-First Search (BFS)
- Depth-First Search (DFS)
- Greedy Best-First Search
- A* Search

Author: AI Course Project
"""

import pygame
from maze import Maze
from bfs import BFS
from dfs import DFS
from greedy import GreedyBestFirst
from astar import AStar
from visualizer import Visualizer


def main():
    """Main application entry point."""
    
    print("=" * 60)
    print("AI Maze Solver - Search Algorithms Visualization")
    print("=" * 60)
    print("\nDemonstrating classical AI search algorithms:")
    print("  • Breadth-First Search (BFS) - Optimal, uninformed")
    print("  • Depth-First Search (DFS) - Deep exploration")
    print("  • Greedy Best-First - Heuristic-driven, fast")
    print("  • A* Search - Optimal, heuristic-guided")
    print("\nClick an algorithm button to see it solve the maze!")
    print("Click 'Generate Random Maze' to create a new maze.")
    print("=" * 60)
    
    # Initialize algorithms
    algorithms = {
        "Breadth-First Search (BFS)": BFS(),
        "Depth-First Search (DFS)": DFS(),
        "Greedy Best-First Search": GreedyBestFirst(),
        "A* Search": AStar()
    }
    
    # Generate initial random maze (larger and harder)
    maze = Maze.generate_random(width=41, height=41)
    
    # Create visualizer with larger cells
    visualizer = Visualizer(maze, cell_size=25)
    
    # Define button positions for side panel (vertical layout)
    # Panel will be on the right side in fullscreen
    display_info = pygame.display.Info()
    panel_x = display_info.current_w - 400
    button_width = 340
    button_height = 50
    button_spacing = 10
    start_y = 150
    
    buttons = {}
    for i, name in enumerate(algorithms.keys()):
        buttons[name] = pygame.Rect(
            panel_x + 30,
            start_y + i * (button_height + button_spacing),
            button_width,
            button_height
        )
    
    # Generate maze button (below algorithm buttons)
    generate_button = pygame.Rect(
        panel_x + 30,
        start_y + len(algorithms) * (button_height + button_spacing) + 20,
        button_width,
        button_height
    )
    
    # Main loop
    running = True
    current_algorithm = None
    
    while running:
        # Draw initial state or wait for user input
        visualizer.screen.fill(visualizer.COLOR_BG)
        visualizer.draw_maze()
        visualizer.draw_special_cells()
        visualizer.draw_side_panel(buttons, generate_button)
        
        pygame.display.flip()
        
        # Wait for user to select algorithm or generate maze
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting = False
                    break
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Check generate button
                    if generate_button.collidepoint(event.pos):
                        print("\n🔄 Generating new random maze...")
                        maze = Maze.generate_random(width=41, height=41)
                        visualizer = Visualizer(maze, cell_size=25)
                        
                        # Update button positions for new visualizer
                        panel_x = display_info.current_w - 400
                        for i, name in enumerate(algorithms.keys()):
                            buttons[name] = pygame.Rect(
                                panel_x + 30,
                                start_y + i * (button_height + button_spacing),
                                button_width,
                                button_height
                            )
                        generate_button = pygame.Rect(
                            panel_x + 30,
                            start_y + len(algorithms) * (button_height + button_spacing) + 20,
                            button_width,
                            button_height
                        )
                        
                        waiting = False
                        break
                    
                    # Check algorithm buttons
                    for name, rect in buttons.items():
                        if rect.collidepoint(event.pos):
                            current_algorithm = algorithms[name]
                            print(f"\n🔍 Running {name}...")
                            
                            # Execute search
                            success = current_algorithm.search(maze)
                            
                            # Print results
                            metrics = current_algorithm.get_metrics()
                            print(f"   ✓ Path found: {success}")
                            print(f"   • Nodes expanded: {metrics['nodes_expanded']}")
                            print(f"   • Path length: {metrics['path_length']}")
                            print(f"   • Execution time: {metrics['execution_time']}")
                            
                            # Visualize
                            result = visualizer.visualize(current_algorithm, buttons, generate_button)
                            
                            if result == "GENERATE":
                                print("\n🔄 Generating new random maze...")
                                maze = Maze.generate_random(width=41, height=41)
                                visualizer = Visualizer(maze, cell_size=25)
                                
                                # Update button positions
                                panel_x = display_info.current_w - 400
                                for i, name in enumerate(algorithms.keys()):
                                    buttons[name] = pygame.Rect(
                                        panel_x + 30,
                                        start_y + i * (button_height + button_spacing),
                                        button_width,
                                        button_height
                                    )
                                generate_button = pygame.Rect(
                                    panel_x + 30,
                                    start_y + len(algorithms) * (button_height + button_spacing) + 20,
                                    button_width,
                                    button_height
                                )
                            elif result in algorithms:
                                current_algorithm = algorithms[result]
                                print(f"\n🔍 Running {result}...")
                                
                                success = current_algorithm.search(maze)
                                metrics = current_algorithm.get_metrics()
                                print(f"   ✓ Path found: {success}")
                                print(f"   • Nodes expanded: {metrics['nodes_expanded']}")
                                print(f"   • Path length: {metrics['path_length']}")
                                print(f"   • Execution time: {metrics['execution_time']}")
                                
                                result = visualizer.visualize(current_algorithm, buttons, generate_button)
                            elif result == False:
                                running = False
                            
                            waiting = False
                            break
            
            visualizer.clock.tick(60)
    
    visualizer.close()
    print("\n👋 Thank you for using AI Maze Solver!")


if __name__ == "__main__":
    main()
