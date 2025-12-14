"""
Node class for representing states in the search space.

This class encapsulates a position in the maze along with search-related
metadata such as parent pointers and cost values.
"""

class Node:
    """
    Represents a state in the search space.
    
    Attributes:
        position (tuple): (x, y) coordinates in the maze grid
        parent (Node): Parent node in the search tree (for path reconstruction)
        g (float): Cost from start node to this node (actual cost)
        h (float): Heuristic estimate from this node to goal (Manhattan distance)
        f (float): Total estimated cost f(n) = g(n) + h(n) (used in A*)
    """
    
    def __init__(self, position, parent=None, g=0, h=0):
        """
        Initialize a Node.
        
        Args:
            position (tuple): (x, y) coordinates
            parent (Node, optional): Parent node for path reconstruction
            g (float, optional): Cost from start. Defaults to 0.
            h (float, optional): Heuristic estimate. Defaults to 0.
        """
        self.position = position
        self.parent = parent
        self.g = g
        self.h = h
        self.f = g + h
    
    def __eq__(self, other):
        """Check equality based on position."""
        if not isinstance(other, Node):
            return False
        return self.position == other.position
    
    def __lt__(self, other):
        """
        Less-than comparison for priority queue ordering.
        Compares based on f value (for A*).
        """
        return self.f < other.f
    
    def __hash__(self):
        """Hash based on position for use in sets/dicts."""
        return hash(self.position)
    
    def __repr__(self):
        """String representation for debugging."""
        return f"Node(pos={self.position}, g={self.g}, h={self.h}, f={self.f})"
