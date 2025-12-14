# AI Maze Solver

An interactive visualization of classical AI search algorithms solving mazes. Built for university AI course to demonstrate state-space search, graph traversal, and heuristic-based search.

## 🎯 Features

- **Four Search Algorithms**:
  - **Breadth-First Search (BFS)**: Uninformed, optimal, level-by-level exploration
  - **Depth-First Search (DFS)**: Uninformed, deep exploration, may find suboptimal paths
  - **Greedy Best-First Search**: Informed, heuristic-driven, fast but not optimal
  - **A\* Search**: Informed, optimal, combines actual cost and heuristic

- **Interactive Visualization**:
  - Real-time animation of search exploration
  - Color-coded cells (walls, free, start, goal, explored, path)
  - Final path highlighting
  - Performance metrics display

- **Random Maze Generation**:
  - Click button to generate new random mazes
  - Uses recursive backtracking algorithm
  - Creates perfect mazes (single path between any two points)

## 🚀 Installation

1. **Install Python** (3.7 or higher)

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## 🎮 Usage

Run the application:
```bash
python main.py
```

**Controls**:
- Click an algorithm button to see it solve the maze
- Click "Generate Random Maze" to create a new maze
- **↑ (Up Arrow)**: Increase animation speed
- **↓ (Down Arrow)**: Decrease animation speed (slower = clearer)
- **SPACE**: Pause/Resume animation
- Watch the animated exploration process
- View metrics (nodes expanded, path length, execution time)

## 📊 Algorithm Comparison

| Algorithm | Complete | Optimal | Time Complexity | Space Complexity |
|-----------|----------|---------|-----------------|------------------|
| BFS | ✅ Yes | ✅ Yes | O(b^d) | O(b^d) |
| DFS | ❌ No | ❌ No | O(b^m) | O(bm) |
| Greedy | ❌ No | ❌ No | O(b^m) | O(b^m) |
| A\* | ✅ Yes | ✅ Yes | O(b^d) | O(b^d) |

*b = branching factor, d = depth of solution, m = maximum depth*

## 🧠 Academic Context

### State Representation
Each state is a position (x, y) in the maze grid.

### Successor Function
Returns valid neighboring cells (up, down, left, right) that are not walls.

### Cost Function
- **g(n)**: Actual cost from start to node n (number of steps)
- **h(n)**: Heuristic estimate from node n to goal (Manhattan distance)
- **f(n)**: Total estimated cost = g(n) + h(n) (used in A\*)

### Heuristic (Manhattan Distance)
```
h(n) = |x_current - x_goal| + |y_current - y_goal|
```

**Properties**:
- **Admissible**: Never overestimates actual cost
- **Consistent**: h(n) ≤ cost(n, n') + h(n') for any successor n'

These properties guarantee A\* finds the optimal solution.

## 📁 Project Structure

```
ai_maze_solver/
├── main.py              # Main application entry point
├── maze.py              # Maze representation and generation
├── node.py              # Node class for search states
├── search_algorithm.py  # Abstract base class for algorithms
├── bfs.py               # Breadth-First Search
├── dfs.py               # Depth-First Search
├── greedy.py            # Greedy Best-First Search
├── astar.py             # A* Search
├── visualizer.py        # Pygame visualization
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## 🎨 Color Coding

- **Black**: Walls
- **White**: Free cells
- **Green**: Start position
- **Red**: Goal position
- **Light Blue**: Explored nodes
- **Dark Blue**: Final path

## 🔬 Observations

When running different algorithms on the same maze, you'll notice:

- **BFS**: Expands uniformly in all directions, like a wave. Always finds shortest path.
- **DFS**: Explores deep into corridors before backtracking. Path may be longer.
- **Greedy**: Rushes toward the goal using heuristic. Fast but may miss shorter paths.
- **A\***: Balanced exploration, guided by both actual cost and heuristic. Optimal and efficient.

## 📝 License

Educational project for AI course. Free to use and modify.

## 👨‍💻 Author

Created for Artificial Intelligence university course.
