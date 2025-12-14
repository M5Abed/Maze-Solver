"""
Maze class for representing and generating mazes.

Supports:
- 2D grid representation (0=free, 1=wall)
- Random maze generation using recursive backtracking
- Neighbor generation (successor function)
- Validation
"""

import random
import json


class Maze:
    """
    Represents a maze as a 2D grid.
    
    Attributes:
        grid (list): 2D list where 0=free cell, 1=wall
        width (int): Width of the maze
        height (int): Height of the maze
        start (tuple): Starting position (x, y)
        goal (tuple): Goal position (x, y)
    """
    
    def __init__(self, grid=None, start=None, goal=None):
        """
        Initialize a Maze.
        
        Args:
            grid (list, optional): 2D grid representation
            start (tuple, optional): Start position (x, y)
            goal (tuple, optional): Goal position (x, y)
        """
        if grid is not None:
            self.grid = grid
            self.height = len(grid)
            self.width = len(grid[0]) if self.height > 0 else 0
            self.start = start
            self.goal = goal
        else:
            self.grid = []
            self.width = 0
            self.height = 0
            self.start = None
            self.goal = None
    
    @staticmethod
    def generate_random(width=25, height=25):
        """
        Generate a random maze using recursive backtracking algorithm.
        
        This creates a perfect maze (no loops, single path between any two points).
        
        Args:
            width (int): Width of the maze (must be odd)
            height (int): Height of the maze (must be odd)
            
        Returns:
            Maze: A randomly generated maze
        """
        # Ensure dimensions are odd for proper maze generation
        if width % 2 == 0:
            width += 1
        if height % 2 == 0:
            height += 1
        
        # Initialize grid filled with walls
        grid = [[1 for _ in range(width)] for _ in range(height)]
        
        # Recursive backtracking maze generation
        def carve_passages(x, y):
            """Carve passages starting from (x, y)."""
            grid[y][x] = 0  # Mark current cell as free
            
            # Define directions: right, down, left, up
            directions = [(2, 0), (0, 2), (-2, 0), (0, -2)]
            random.shuffle(directions)
            
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                
                # Check if the new position is valid and unvisited
                if 0 <= nx < width and 0 <= ny < height and grid[ny][nx] == 1:
                    # Carve the wall between current and next cell
                    grid[y + dy // 2][x + dx // 2] = 0
                    carve_passages(nx, ny)
        
        # Start carving from (1, 1)
        carve_passages(1, 1)
        
        # Set start at top-left free area
        start = (1, 1)
        
        # Set goal at bottom-right free area
        goal = (width - 2, height - 2)
        
        # Ensure start and goal are free
        grid[start[1]][start[0]] = 0
        grid[goal[1]][goal[0]] = 0
        
        return Maze(grid, start, goal)
    
    @staticmethod
    def load_from_file(filename):
        """
        Load a maze from a JSON file.
        
        Expected format:
        {
            "grid": [[0, 1, 0, ...], ...],
            "start": [x, y],
            "goal": [x, y]
        }
        
        Args:
            filename (str): Path to the JSON file
            
        Returns:
            Maze: Loaded maze
        """
        with open(filename, 'r') as f:
            data = json.load(f)
        
        grid = data['grid']
        start = tuple(data['start'])
        goal = tuple(data['goal'])
        
        return Maze(grid, start, goal)
    
    def save_to_file(self, filename):
        """
        Save the maze to a JSON file.
        
        Args:
            filename (str): Path to save the file
        """
        data = {
            'grid': self.grid,
            'start': list(self.start),
            'goal': list(self.goal)
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def is_valid_position(self, x, y):
        """
        Check if a position is valid (within bounds and not a wall).
        
        Args:
            x (int): X coordinate
            y (int): Y coordinate
            
        Returns:
            bool: True if position is valid and free
        """
        return (0 <= x < self.width and 
                0 <= y < self.height and 
                self.grid[y][x] == 0)
    
    def get_neighbors(self, position):
        """
        Get valid neighboring positions (successor function).
        
        Returns neighbors in 4 directions: right, down, left, up.
        
        Args:
            position (tuple): Current position (x, y)
            
        Returns:
            list: List of valid neighbor positions
        """
        x, y = position
        neighbors = []
        
        # Four directions: right, down, left, up
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if self.is_valid_position(nx, ny):
                neighbors.append((nx, ny))
        
        return neighbors
    
    def __repr__(self):
        """String representation for debugging."""
        return f"Maze({self.width}x{self.height}, start={self.start}, goal={self.goal})"
