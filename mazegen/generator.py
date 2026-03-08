import random
from typing import Optional

NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8

ALL_WALLS = NORTH + EAST + SOUTH + WEST

OPPOSITE = {
    NORTH: SOUTH, 
    SOUTH: NORTH,
    EAST: WEST,
    WEST: EAST,
    }

DIRECTION = {
    NORTH: (0, -1),
    SOUTH: (0, 1),
    EAST: (1 , 0),
    WEST: (-1, 0)
}


class MazeGenerator:
    """Generate a random maze using Recursive Backtracker"""

    def __init__(
        self,
        width: int,
        height: int,
        perfect: bool = True,
        seed: Optional[int] = None,
    )-> None:

        """Initialize the maze generator

        Args:
            width: Number of cells horizontally
            height: Number of cells vertically
            perfect: If True, exactly one path between any two cells
            seed: Random seed for reproducibility
        """
        self.width = width
        self.height = height
        self.perfect = perfect
        if seed is not None:
            random.seed(seed)
        self.grid: list[list[int]] = [
            [ALL_WALLS for _ in range(width)]
            for _ in range(height)
        ]

    def _is_valid(self, x: int, y: int) -> bool:
        """Check if (x, y) is inside the grid"""
        if x >= 0 and x < self.width and y >= 0 and y < self.height:
            return True
        else:
            return False

    def _has_wall(self, x: int, y: int, wall: int) -> bool:
        """Check if cell (x, y) has the given wall"""
        return bool(self.grid[y][x] & wall)

    def _remove_wall(self, x: int, y: int, wall: int) -> None:
        """Remove wall from cell (x, y) and the opposite wall from neighbor"""
        self.grid[y][x] &= ~wall
        nx = x + DIRECTION[wall][0]
        ny = y + DIRECTION[wall][1]
        self.grid[ny][nx] &= ~OPPOSITE[wall]
    
    def generate(
        self,
        blocked: set[tuple[int, int]] | None = None,
    ) -> None:
        """Generate the maze using Recursive Backtracker (DFS).

        Args:
            blocked: cells to skip (e.g. 42 pattern cells).
        """
        if blocked is None:
            blocked = set()

        self.grid = [
            [ALL_WALLS for _ in range(self.width)]
            for _ in range(self.height)
        ]

        visited: set[tuple[int, int]] = set()
        visited.update(blocked)
        start = (0, 0)
        visited.add(start)
        stack: list[tuple[int, int]] = [start]

        while stack:
            cx, cy = stack[len(stack) - 1]
            neighbors = []
            for wall in (NORTH, EAST, SOUTH, WEST):
                nx = cx + DIRECTION[wall][0]
                ny = cy + DIRECTION[wall][1]
                if self._is_valid(nx, ny) and (nx, ny) not in visited:
                    neighbors.append((wall, nx, ny))
            
            if neighbors:
                wall, nx, ny = random.choice(neighbors)
                self._remove_wall(cx, cy, wall)
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                stack.pop()

        if not self.perfect:
            extra = (self.width * self.height) // 10
            for _ in range(extra):
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                if (x, y) in blocked:
                    continue
                wall = random.choice([NORTH, EAST, SOUTH, WEST])
                nx = x + DIRECTION[wall][0]
                ny = y + DIRECTION[wall][1]
                if self._is_valid(nx, ny) and (nx, ny) not in blocked:
                    if self._has_wall(x, y, wall):
                        self._remove_wall(x, y, wall)
    
    def get_grid(self) -> list[list[int]]:
        """Return a copy of the maze grid"""
        rows: list[list[int]] = []
        for row in self.grid:
            rows.append(row[:]) #![:] is mean slice ----([start:stop]----[start:] ---- [:stop] ----- [:])
        return rows
