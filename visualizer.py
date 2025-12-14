"""
Pygame-based visualization for maze solving algorithms.

Provides real-time animation of search exploration and final path display.
"""

import pygame
import sys


class Visualizer:
    """
    Visualizes maze solving with pygame.
    
    Features:
    - Grid rendering with color-coded cells
    - Animated exploration process
    - Final path highlighting
    - Real-time metrics display
    """
    
    # Modern color palette
    COLOR_WALL = (30, 30, 40)           # Dark walls
    COLOR_FREE = (250, 250, 252)        # Light free cells
    COLOR_START = (16, 185, 129)        # Modern green - start
    COLOR_GOAL = (239, 68, 68)          # Modern red - goal
    COLOR_EXPLORED = (147, 197, 253)    # Sky blue - explored
    COLOR_PATH = (59, 130, 246)         # Bright blue - path
    COLOR_BG = (17, 24, 39)             # Dark background
    COLOR_PANEL = (31, 41, 55)          # Panel background
    COLOR_CARD = (55, 65, 81)           # Card background
    COLOR_TEXT = (243, 244, 246)        # Light text
    COLOR_TEXT_MUTED = (156, 163, 175)  # Muted text
    COLOR_BUTTON = (59, 130, 246)       # Primary button
    COLOR_BUTTON_HOVER = (37, 99, 235)  # Button hover
    COLOR_BUTTON_ACTIVE = (29, 78, 216) # Active button
    COLOR_ACCENT = (168, 85, 247)       # Purple accent
    
    def __init__(self, maze, cell_size=25):
        """
        Initialize the visualizer with modern UI.
        
        Args:
            maze (Maze): The maze to visualize
            cell_size (int): Size of each cell in pixels
        """
        self.maze = maze
        self.cell_size = cell_size
        
        # Calculate window dimensions with side panel layout
        self.maze_width = maze.width * cell_size
        self.maze_height = maze.height * cell_size
        self.side_panel_width = 400  # Side panel for controls and metrics
        self.window_width = self.maze_width + self.side_panel_width
        self.window_height = max(self.maze_height, 800)
        
        # Initialize pygame
        pygame.init()
        
        # Get display info for fullscreen
        display_info = pygame.display.Info()
        screen_width = display_info.current_w
        screen_height = display_info.current_h
        
        # Calculate optimal cell size to fit screen
        available_width = screen_width - self.side_panel_width
        available_height = screen_height
        
        max_cell_from_width = available_width // maze.width
        max_cell_from_height = available_height // maze.height
        
        # Use the smaller to ensure everything fits
        self.cell_size = min(cell_size, max_cell_from_width, max_cell_from_height)
        
        # Recalculate dimensions with optimized cell size
        self.maze_width = maze.width * self.cell_size
        self.maze_height = maze.height * self.cell_size
        self.window_width = self.maze_width + self.side_panel_width
        self.window_height = max(self.maze_height, screen_height)
        
        # Create fullscreen window
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("AI Maze Solver - Search Algorithms Visualization")
        self.clock = pygame.time.Clock()
        self.font_title = pygame.font.Font(None, 36)
        self.font = pygame.font.Font(None, 26)
        self.font_small = pygame.font.Font(None, 22)
        self.font_tiny = pygame.font.Font(None, 18)
        
        # Get actual screen dimensions
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        
        # Center maze on screen
        self.maze_offset_x = (self.screen_width - self.side_panel_width - self.maze_width) // 2
        self.maze_offset_y = (self.screen_height - self.maze_height) // 2
        
        # Animation state
        self.explored_index = 0
        self.animation_speed = 5  # Steps per frame (lower = slower, clearer)
        self.min_speed = 1
        self.max_speed = 50
        self.is_animating = False
        self.show_path = False
        
        # Current algorithm and results
        self.current_algorithm = None
        self.metrics = None
    
    def draw_maze(self):
        """Draw the maze grid."""
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                rect = pygame.Rect(
                    self.maze_offset_x + x * self.cell_size,
                    self.maze_offset_y + y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                
                # Determine cell color
                if self.maze.grid[y][x] == 1:
                    color = self.COLOR_WALL
                else:
                    color = self.COLOR_FREE
                
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)  # Grid lines
    
    def draw_special_cells(self):
        """Draw start and goal cells."""
        # Start cell
        start_rect = pygame.Rect(
            self.maze_offset_x + self.maze.start[0] * self.cell_size,
            self.maze_offset_y + self.maze.start[1] * self.cell_size,
            self.cell_size,
            self.cell_size
        )
        pygame.draw.rect(self.screen, self.COLOR_START, start_rect)
        pygame.draw.rect(self.screen, (200, 200, 200), start_rect, 1)
        
        # Goal cell
        goal_rect = pygame.Rect(
            self.maze_offset_x + self.maze.goal[0] * self.cell_size,
            self.maze_offset_y + self.maze.goal[1] * self.cell_size,
            self.cell_size,
            self.cell_size
        )
        pygame.draw.rect(self.screen, self.COLOR_GOAL, goal_rect)
        pygame.draw.rect(self.screen, (200, 200, 200), goal_rect, 1)
    
    def draw_explored(self, explored_list, up_to_index):
        """Draw explored cells up to a certain index."""
        for i in range(min(up_to_index, len(explored_list))):
            pos = explored_list[i]
            # Don't overwrite start and goal
            if pos != self.maze.start and pos != self.maze.goal:
                rect = pygame.Rect(
                    self.maze_offset_x + pos[0] * self.cell_size,
                    self.maze_offset_y + pos[1] * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                pygame.draw.rect(self.screen, self.COLOR_EXPLORED, rect)
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)
    
    def draw_path(self, path):
        """Draw the final path."""
        for pos in path:
            # Don't overwrite start and goal
            if pos != self.maze.start and pos != self.maze.goal:
                rect = pygame.Rect(
                    self.maze_offset_x + pos[0] * self.cell_size,
                    self.maze_offset_y + pos[1] * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                pygame.draw.rect(self.screen, self.COLOR_PATH, rect)
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)
    
    def draw_button(self, text, rect, is_active=False, is_hover=False):
        """Draw a button."""
        if is_active:
            color = self.COLOR_BUTTON_ACTIVE
        elif is_hover:
            color = self.COLOR_BUTTON_HOVER
        else:
            color = self.COLOR_BUTTON
        
        pygame.draw.rect(self.screen, color, rect, border_radius=5)
        pygame.draw.rect(self.screen, self.COLOR_TEXT, rect, 2, border_radius=5)
        
        text_surface = self.font_small.render(text, True, self.COLOR_TEXT)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)
    
    def draw_side_panel(self, buttons, generate_button):
        """Draw the modern side panel with controls and metrics."""
        panel_x = self.screen_width - self.side_panel_width
        
        # Panel background
        pygame.draw.rect(self.screen, self.COLOR_PANEL, 
                        (panel_x, 0, self.side_panel_width, self.screen_height))
        
        y_offset = 30
        
        # Title
        title = self.font_title.render("AI Maze Solver", True, self.COLOR_TEXT)
        self.screen.blit(title, (panel_x + 30, y_offset))
        y_offset += 50
        
        # Subtitle
        subtitle = self.font_small.render("Search Algorithms", True, self.COLOR_TEXT_MUTED)
        self.screen.blit(subtitle, (panel_x + 30, y_offset))
        y_offset += 50
        
        # Algorithm selection section
        section_title = self.font.render("Select Algorithm", True, self.COLOR_TEXT)
        self.screen.blit(section_title, (panel_x + 30, y_offset))
        y_offset += 40
        
        # Draw algorithm buttons (vertical stack)
        mouse_pos = pygame.mouse.get_pos()
        button_names = ["Breadth-First Search (BFS)", "Depth-First Search (DFS)", 
                       "Greedy Best-First Search", "A* Search"]
        
        for i, name in enumerate(button_names):
            rect = buttons[name]
            is_active = self.current_algorithm and self.current_algorithm.name == name
            is_hover = rect.collidepoint(mouse_pos)
            self.draw_modern_button(name, rect, is_active, is_hover)
        
        y_offset += len(button_names) * 60 + 20
        
        # Generate maze button
        is_hover = generate_button.collidepoint(mouse_pos)
        self.draw_modern_button("Generate Random Maze", generate_button, False, is_hover, accent=True)
        y_offset += 80
        
        # Speed controls section
        pygame.draw.rect(self.screen, self.COLOR_CARD, 
                        (panel_x + 20, y_offset, self.side_panel_width - 40, 80), border_radius=10)
        
        speed_title = self.font_small.render("Animation Speed", True, self.COLOR_TEXT)
        self.screen.blit(speed_title, (panel_x + 35, y_offset + 15))
        
        speed_value = self.font.render(f"{self.animation_speed}", True, self.COLOR_ACCENT)
        self.screen.blit(speed_value, (panel_x + 35, y_offset + 40))
        
        controls = self.font_tiny.render("UP/DOWN Adjust  SPACE Pause", True, self.COLOR_TEXT_MUTED)
        self.screen.blit(controls, (panel_x + 100, y_offset + 48))
        y_offset += 100
        
        # Metrics section
        if self.metrics:
            pygame.draw.rect(self.screen, self.COLOR_CARD, 
                            (panel_x + 20, y_offset, self.side_panel_width - 40, 200), border_radius=10)
            
            metrics_title = self.font.render("Results", True, self.COLOR_TEXT)
            self.screen.blit(metrics_title, (panel_x + 35, y_offset + 15))
            
            metrics_data = [
                ("Algorithm", self.metrics['algorithm'].split('(')[0].strip()),
                ("Nodes Expanded", str(self.metrics['nodes_expanded'])),
                ("Path Length", str(self.metrics['path_length'])),
                ("Time", self.metrics['execution_time']),
                ("Status", "Found" if self.metrics['path_found'] else "Not Found")
            ]
            
            for i, (label, value) in enumerate(metrics_data):
                label_surface = self.font_small.render(label, True, self.COLOR_TEXT_MUTED)
                self.screen.blit(label_surface, (panel_x + 35, y_offset + 50 + i * 28))
                
                value_surface = self.font_small.render(value, True, self.COLOR_TEXT)
                self.screen.blit(value_surface, (panel_x + 200, y_offset + 50 + i * 28))
    
    def draw_modern_button(self, text, rect, is_active=False, is_hover=False, accent=False):
        """Draw a modern button with rounded corners and shadows."""
        if is_active:
            color = self.COLOR_BUTTON_ACTIVE
        elif accent:
            color = self.COLOR_ACCENT if not is_hover else (147, 51, 234)
        elif is_hover:
            color = self.COLOR_BUTTON_HOVER
        else:
            color = self.COLOR_BUTTON
        
        # Draw button with rounded corners
        pygame.draw.rect(self.screen, color, rect, border_radius=8)
        
        # Draw text
        text_surface = self.font_small.render(text, True, self.COLOR_TEXT)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)
    
    def visualize(self, algorithm, buttons, generate_button):
        """
        Main visualization loop.
        
        Args:
            algorithm (SearchAlgorithm): The algorithm that was executed
            buttons (dict): Dictionary of button names to rects
            generate_button (pygame.Rect): Generate maze button rect
        """
        self.current_algorithm = algorithm
        self.metrics = algorithm.get_metrics()
        self.explored_index = 0
        self.is_animating = True
        self.show_path = False
        
        running = True
        paused = False
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return False
                
                if event.type == pygame.KEYDOWN:
                    # Speed controls
                    if event.key == pygame.K_UP:
                        self.animation_speed = min(self.max_speed, self.animation_speed + 1)
                        print(f"Speed increased to {self.animation_speed} steps/frame")
                    elif event.key == pygame.K_DOWN:
                        self.animation_speed = max(self.min_speed, self.animation_speed - 1)
                        print(f"Speed decreased to {self.animation_speed} steps/frame")
                    elif event.key == pygame.K_SPACE:
                        paused = not paused
                        print(f"Animation {'paused' if paused else 'resumed'}")
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if generate button clicked
                    if generate_button.collidepoint(event.pos):
                        return "GENERATE"
                    
                    # Check if algorithm button clicked
                    for name, rect in buttons.items():
                        if rect.collidepoint(event.pos):
                            return name
            
            # Clear screen
            self.screen.fill(self.COLOR_BG)
            
            # Draw maze
            self.draw_maze()
            
            # Draw exploration animation
            if self.is_animating:
                self.draw_explored(algorithm.explored, self.explored_index)
                
                # Increment animation (only if not paused)
                if not paused and self.explored_index < len(algorithm.explored):
                    self.explored_index += self.animation_speed
                elif self.explored_index >= len(algorithm.explored):
                    self.is_animating = False
                    self.show_path = True
            else:
                # Show all explored cells
                self.draw_explored(algorithm.explored, len(algorithm.explored))
            
            # Draw path if animation complete
            if self.show_path and algorithm.path:
                self.draw_path(algorithm.path)
            
            # Draw start and goal on top
            self.draw_special_cells()
            
            # Draw side panel
            self.draw_side_panel(buttons, generate_button)
            
            pygame.display.flip()
            self.clock.tick(60)  # 60 FPS
        
        return False
    
    def close(self):
        """Close the visualizer."""
        pygame.quit()
