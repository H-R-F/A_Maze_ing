from typing import Optional
from mazegen.generator import NORTH, EAST, SOUTH, WEST, DIRECTION

DIRECTION_LETTER = {
    NORTH: "N",
    EAST: "E",
    SOUTH: "S",
    WEST: "W",
}


def solve_maze(
    grid: list[list[int]],
    width: int,
    height: int,
    entry: tuple[int, int],
    exit_pos: tuple[int, int],
) -> Optional[str]:
    """Find shortest path from entry to exit using BFS.
    Returns:
        String of directions like "EESSNW...", or None if no path.
    """
    todo: list[tuple[tuple[int, int], str]] = [(entry, "")]
    visited: set[tuple[int, int]] = {entry}

    while todo:
        (x, y), path = todo.pop(0)

        if (x, y) == exit_pos:
            return path

        for wall in (NORTH, EAST, SOUTH, WEST):
            if not (grid[y][x] & wall):
                nx = x + DIRECTION[wall][0]
                ny = y + DIRECTION[wall][1]
                if nx >= 0 and nx < width and ny >= 0 and ny < height:
                    if (nx, ny) not in visited:
                        visited.add((nx, ny))
                        todo.append(((nx, ny), path + DIRECTION_LETTER[wall]))
    return None
