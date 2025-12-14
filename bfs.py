"""
Breadth-First Search (BFS) implementation.

BFS is an uninformed search algorithm that explores the search space level by level.
It uses a FIFO queue and guarantees finding the shortest path.
"""

from collections import deque
import time
from node import Node
from search_algorithm import SearchAlgorithm


class BFS(SearchAlgorithm):
    """
    Breadth-First Search algorithm.
    
    Properties:
    - Complete: Yes (will find a solution if one exists)
    - Optimal: Yes (finds shortest path in unweighted graphs)
    - Time Complexity: O(b^d) where b=branching factor, d=depth
    - Space Complexity: O(b^d) (stores all nodes at current level)
    
    Uses FIFO queue for frontier management.
    """
    
    def __init__(self):
        """Initialize BFS algorithm."""
        super().__init__("Breadth-First Search (BFS)")
    
    def search(self, maze):
        """
        Execute BFS on the maze.
        
        Algorithm:
        1. Initialize queue with start node
        2. While queue is not empty:
           a. Dequeue front node
           b. If goal reached, reconstruct path
           c. Expand node by adding unvisited neighbors to queue
        
        Args:
            maze (Maze): The maze to solve
            
        Returns:
            bool: True if path found, False otherwise
        """
        self.reset()
        start_time = time.time()
        
        # Initialize start node
        start_node = Node(maze.start, parent=None, g=0, h=0)
        
        # FIFO queue for BFS
        frontier = deque([start_node])
        
        # Track visited positions to avoid cycles
        visited = set()
        visited.add(start_node.position)
        
        while frontier:
            # Dequeue front node (FIFO)
            current = frontier.popleft()
            self.explored.append(current.position)
            self.nodes_expanded += 1
            
            # Goal test
            if current.position == maze.goal:
                self.execution_time = time.time() - start_time
                self.reconstruct_path(current)
                return True
            
            # Expand node: add neighbors to frontier
            for neighbor_pos in maze.get_neighbors(current.position):
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
