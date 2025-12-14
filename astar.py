"""
A* Search implementation.

A* is an informed search algorithm that combines actual cost g(n) and
heuristic estimate h(n) to find the optimal path efficiently.
"""

import heapq
import time
from node import Node
from search_algorithm import SearchAlgorithm


class AStar(SearchAlgorithm):
    """
    A* Search algorithm.
    
    Properties:
    - Complete: Yes (will find a solution if one exists)
    - Optimal: Yes (with admissible heuristic)
    - Time Complexity: O(b^d) but often much better with good heuristic
    - Space Complexity: O(b^d)
    
    Uses priority queue ordered by f(n) = g(n) + h(n).
    - g(n): actual cost from start to current node
    - h(n): heuristic estimate from current node to goal (Manhattan distance)
    - f(n): total estimated cost of path through current node
    
    The Manhattan distance heuristic is admissible (never overestimates)
    and consistent, guaranteeing optimal solution.
    """
    
    def __init__(self):
        """Initialize A* Search algorithm."""
        super().__init__("A* Search")
    
    @staticmethod
    def manhattan_distance(pos1, pos2):
        """
        Calculate Manhattan distance heuristic.
        
        h(n) = |x_current - x_goal| + |y_current - y_goal|
        
        This heuristic is:
        - Admissible: never overestimates actual cost
        - Consistent: h(n) <= cost(n, n') + h(n') for any successor n'
        
        Args:
            pos1 (tuple): Current position (x, y)
            pos2 (tuple): Goal position (x, y)
            
        Returns:
            float: Manhattan distance
        """
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def search(self, maze):
        """
        Execute A* Search on the maze.
        
        Algorithm:
        1. Initialize priority queue with start node
        2. While queue is not empty:
           a. Pop node with lowest f(n) = g(n) + h(n)
           b. If goal reached, reconstruct path
           c. Expand node by adding neighbors with updated costs
        
        Note: We track visited nodes but also check for better paths
        (though with consistent heuristic, first visit is always best).
        
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
        
        # Priority queue ordered by f(n) = g(n) + h(n)
        # Format: (f_value, counter, node) - counter for tie-breaking
        counter = 0
        frontier = [(start_node.f, counter, start_node)]
        heapq.heapify(frontier)
        
        # Track visited positions
        visited = set()
        
        while frontier:
            # Pop node with lowest f(n)
            _, _, current = heapq.heappop(frontier)
            
            # Skip if already visited (with consistent heuristic, first is best)
            if current.position in visited:
                continue
            
            visited.add(current.position)
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
                    # Calculate costs for neighbor
                    g = current.g + 1  # Cost from start (each step costs 1)
                    h = self.manhattan_distance(neighbor_pos, maze.goal)
                    
                    neighbor_node = Node(
                        neighbor_pos,
                        parent=current,
                        g=g,
                        h=h
                    )
                    # f(n) is automatically calculated in Node.__init__
                    
                    counter += 1
                    heapq.heappush(frontier, (neighbor_node.f, counter, neighbor_node))
        
        # No path found
        self.execution_time = time.time() - start_time
        return False
