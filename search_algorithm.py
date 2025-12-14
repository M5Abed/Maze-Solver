"""
Abstract base class for search algorithms.

Provides common interface and utilities for all search algorithm implementations.
"""

from abc import ABC, abstractmethod
import time


class SearchAlgorithm(ABC):
    """
    Abstract base class for search algorithms.
    
    All search algorithms must implement the search() method.
    Provides common functionality for path reconstruction and metrics tracking.
    """
    
    def __init__(self, name):
        """
        Initialize the search algorithm.
        
        Args:
            name (str): Name of the algorithm
        """
        self.name = name
        self.nodes_expanded = 0
        self.path_length = 0
        self.execution_time = 0
        self.explored = []  # Track exploration order for visualization
        self.path = []  # Final path from start to goal
    
    @abstractmethod
    def search(self, maze):
        """
        Execute the search algorithm on the given maze.
        
        Must be implemented by subclasses.
        
        Args:
            maze (Maze): The maze to solve
            
        Returns:
            bool: True if path found, False otherwise
        """
        pass
    
    def reconstruct_path(self, current_node):
        """
        Reconstruct the path from start to goal using parent pointers.
        
        Args:
            current_node (Node): The goal node
            
        Returns:
            list: List of positions from start to goal
        """
        path = []
        node = current_node
        
        while node is not None:
            path.append(node.position)
            node = node.parent
        
        path.reverse()
        self.path = path
        self.path_length = len(path)
        return path
    
    def get_metrics(self):
        """
        Get performance metrics for the search.
        
        Returns:
            dict: Dictionary containing metrics
        """
        return {
            'algorithm': self.name,
            'nodes_expanded': self.nodes_expanded,
            'path_length': self.path_length,
            'execution_time': f"{self.execution_time:.4f}s",
            'path_found': len(self.path) > 0
        }
    
    def reset(self):
        """Reset metrics and tracking for a new search."""
        self.nodes_expanded = 0
        self.path_length = 0
        self.execution_time = 0
        self.explored = []
        self.path = []
