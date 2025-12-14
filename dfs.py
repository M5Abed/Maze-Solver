"""
Depth-First Search (DFS) implementation.

DFS is an uninformed search algorithm that explores as deep as possible
before backtracking. Uses a LIFO stack and may find suboptimal paths.
"""

import time
from node import Node
from search_algorithm import SearchAlgorithm


class DFS(SearchAlgorithm):
    """
    Depth-First Search algorithm.
    
    Properties:
    - Complete: No (can get stuck in infinite loops without cycle detection)
    - Optimal: No (may find longer paths)
    - Time Complexity: O(b^m) where b=branching factor, m=maximum depth
    - Space Complexity: O(bm) (only stores path and siblings)
    
    Uses LIFO stack for frontier management.
    """
    
    def __init__(self):
        """Initialize DFS algorithm."""
        super().__init__("Depth-First Search (DFS)")
    
    def search(self, maze):
        """
        Execute DFS on the maze.
        
        Algorithm:
        1. Initialize stack with start node
        2. While stack is not empty:
           a. Pop top node
           b. If goal reached, reconstruct path
           c. Expand node by adding unvisited neighbors to stack
        
        Args:
            maze (Maze): The maze to solve
            
        Returns:
            bool: True if path found, False otherwise
        """
        self.reset()
        start_time = time.time()
        
        # Initialize start node
        start_node = Node(maze.start, parent=None, g=0, h=0)
        
        # LIFO stack for DFS (using list)
        frontier = [start_node]
        
        # Track visited positions to avoid cycles
        visited = set()
        visited.add(start_node.position)
        
        while frontier:
            # Pop top node (LIFO)
            current = frontier.pop()
            self.explored.append(current.position)
            self.nodes_expanded += 1
            
            # Goal test
            if current.position == maze.goal:
                self.execution_time = time.time() - start_time
                self.reconstruct_path(current)
                return True
            
            # Expand node: add neighbors to frontier
            # Note: We reverse to maintain consistent exploration order
            neighbors = maze.get_neighbors(current.position)
            for neighbor_pos in reversed(neighbors):
                if neighbor_pos not in visited:
                    visited.add(neighbor_pos)
                    # Cost increases by 1 for each step
                    neighbor_node = Node(
                        neighbor_pos,
                        parent=current,
                        g=current.g + 1,
                        h=0
                    )
                    frontier.append(neighbor_node)
        
        # No path found
        self.execution_time = time.time() - start_time
        return False
