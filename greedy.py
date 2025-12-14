"""
Greedy Best-First Search implementation.

Greedy search is an informed search algorithm that uses only the heuristic
function h(n) to guide the search toward the goal. Fast but not optimal.
"""

import heapq
import time
from node import Node
from search_algorithm import SearchAlgorithm


class GreedyBestFirst(SearchAlgorithm):
    """
    Greedy Best-First Search algorithm.
    
    Properties:
    - Complete: No (can get stuck in dead ends)
    - Optimal: No (ignores path cost, only considers heuristic)
    - Time Complexity: O(b^m) in worst case
    - Space Complexity: O(b^m)
    
    Uses priority queue ordered by h(n) only.
    Heuristic: Manhattan distance to goal.
    """
    
    def __init__(self):
        """Initialize Greedy Best-First Search algorithm."""
        super().__init__("Greedy Best-First Search")
    
    @staticmethod
    def manhattan_distance(pos1, pos2):
        """
        Calculate Manhattan distance heuristic.
        
        h(n) = |x_current - x_goal| + |y_current - y_goal|
        
        This heuristic is admissible for grid-based movement
        (never overestimates the actual cost).
        
        Args:
            pos1 (tuple): Current position (x, y)
            pos2 (tuple): Goal position (x, y)
            
        Returns:
            float: Manhattan distance
        """
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def search(self, maze):
        """
        Execute Greedy Best-First Search on the maze.
        
        Algorithm:
        1. Initialize priority queue with start node
        2. While queue is not empty:
           a. Pop node with lowest h(n)
           b. If goal reached, reconstruct path
           c. Expand node by adding unvisited neighbors
        
        Args:
            maze (Maze): The maze to solve
            
        Returns:
            bool: True if path found, False otherwise
        """
        self.reset()
        start_time = time.time()
        
        # Calculate heuristic for start node
        h_start = self.manhattan_distance(maze.start, maze.goal)
        start_node = Node(maze.start, parent=None, g=0, h=h_start)
        
        # Priority queue ordered by h(n) only
        # Format: (h_value, counter, node) - counter for tie-breaking
        counter = 0
        frontier = [(start_node.h, counter, start_node)]
        heapq.heapify(frontier)
        
        # Track visited positions
        visited = set()
        visited.add(start_node.position)
        
        while frontier:
            # Pop node with lowest h(n)
            _, _, current = heapq.heappop(frontier)
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
                    
                    # Calculate heuristic for neighbor
                    h = self.manhattan_distance(neighbor_pos, maze.goal)
                    
                    neighbor_node = Node(
                        neighbor_pos,
                        parent=current,
                        g=current.g + 1,  # Track g for path reconstruction
                        h=h
                    )
                    
                    counter += 1
                    heapq.heappush(frontier, (neighbor_node.h, counter, neighbor_node))
        
        # No path found
        self.execution_time = time.time() - start_time
        return False
