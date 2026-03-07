from mazegen.generator import (
    NORTH, EAST, SOUTH, WEST,
    ALL_WALLS, OPPOSITE, DIRECTION
    )

PATTERN_42 = [
    "#...#..#####",
    "#...#..#...#",
    "#...#.....#.",
    "#####....#..",
    "....#...#...",
    "....#..#...#",
    "....#..#####",
]


def inject_42_pattern(
    grid: list[list[int]],
    width: int,
    height: int
) -> set[tuple[int, int]]:
    """Inject '42' pattern into the grid.

    Returns set of (x, y) cells that form the pattern.
    """
    pattern_h = len(PATTERN_42)
    pattern_w = max(len(row) for row in PATTERN_42)
    pattern_cells: set[tuple[int, int]] = set()

    if width < pattern_w + 2 or height < pattern_h + 2:
        return pattern_cells

    start_x = (width - pattern_w) // 2
    start_y = (height - pattern_h) // 2

    for py, row_str in enumerate(PATTERN_42):
        for px, char in enumerate(row_str):
            if char == '#':
                gx = start_x + px
                gy = start_y + py
                grid[gy][gx] = ALL_WALLS
                pattern_cells.add((gx, gy))

                for wall in (NORTH, EAST, SOUTH, WEST):
                    nx = gx + DIRECTION[wall][0]
                    ny = gy + DIRECTION[wall][1]
                    if 0 <= nx < width and 0 <= ny < height:
                        grid[ny][nx] |= OPPOSITE[wall]
    return pattern_cells
