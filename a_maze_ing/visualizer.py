from mazegen.generator import NORTH, EAST, SOUTH, WEST

RESET = "\033[0m"
WALL_COLOR = "\033[37m"  # WHITE COLOR
PATH_COLOR = "\033[32m"  # GREEN COLOR
ENTRY_COLOR = "\033[34m"  # BLUE COLOR
EXIT_COLOR = "\033[31m"  # RED COLOR
PATTERN_COLOR = "\033[37;2m"  # DIM WHITE for 42 pattern

CROSS = {
    (0, 0, 0, 0): " ",
    (0, 0, 0, 1): "╸",
    (0, 0, 1, 0): "╻",
    (0, 0, 1, 1): "┓",
    (0, 1, 0, 0): "╺",
    (0, 1, 0, 1): "━",
    (0, 1, 1, 0): "┏",
    (0, 1, 1, 1): "┳",
    (1, 0, 0, 0): "╹",
    (1, 0, 0, 1): "┛",
    (1, 0, 1, 0): "┃",
    (1, 0, 1, 1): "┫",
    (1, 1, 0, 0): "┗",
    (1, 1, 0, 1): "┻",
    (1, 1, 1, 0): "┣",
    (1, 1, 1, 1): "╋",
}
H_WALL = "━━━"
V_WALL = "┃"


def clear_screen() -> None:
    """Clear terminal screen."""
    print("\033[2J\033[H", end="")


def display_maze(
        grid: list[list[int]],
        width: int,
        height: int,
        entry: tuple[int, int],
        exit_pos: tuple[int, int],
        path: str | None = None,
        wall_color: str = WALL_COLOR,
        path_color: str = PATH_COLOR,
        pattern_cells: set[tuple[int, int]] | None = None,
        pattern_color: str = PATTERN_COLOR,
) -> None:
    """Display maze in terminal using box-drawing characters."""

    path_cells: set[tuple[int, int]] = set()
    if path:
        x, y = entry
        path_cells.add((x, y))
        for ch in path:
            if ch == "N":
                y -= 1
            elif ch == "S":
                y += 1
            elif ch == "E":
                x += 1
            elif ch == "W":
                x -= 1
            path_cells.add((x, y))

    def h_wall(hx: int, hy: int) -> bool:
        """Check horizontal wall at column hx, separator row hy."""
        if hx < 0 or hx >= width:
            return False
        if hy == 0:
            return bool(grid[0][hx] & NORTH)
        if hy >= height:
            return bool(grid[height - 1][hx] & SOUTH)
        return bool(grid[hy][hx] & NORTH)

    def v_wall(vx: int, vy: int) -> bool:
        """Check vertical wall at column vx, cell row vy."""
        if vy < 0 or vy >= height:
            return False
        if vx == 0:
            return bool(grid[vy][0] & WEST)
        if vx >= width:
            return bool(grid[vy][width - 1] & EAST)
        return bool(grid[vy][vx] & WEST)

    for hy in range(height + 1):
        sep = wall_color
        for ix in range(width + 1):
            up = 1 if v_wall(ix, hy - 1) else 0
            right = 1 if h_wall(ix, hy) else 0
            down = 1 if v_wall(ix, hy) else 0
            left = 1 if h_wall(ix - 1, hy) else 0
            sep += CROSS[(up, right, down, left)]
            if ix < width:
                sep += H_WALL if h_wall(ix, hy) else "   "
        sep += RESET
        print(sep)

        if hy < height:
            mid = wall_color
            for x in range(width):
                mid += V_WALL if v_wall(x, hy) else " "
                if (x, hy) == entry:
                    mid += ENTRY_COLOR + "███" + wall_color
                elif (x, hy) == exit_pos:
                    mid += EXIT_COLOR + "███" + wall_color
                elif pattern_cells and (x, hy) in pattern_cells:
                    mid += pattern_color + "███" + wall_color
                elif (x, hy) in path_cells:
                    mid += path_color + "███" + wall_color
                else:
                    mid += "   "
            mid += V_WALL if v_wall(width, hy) else " "
            mid += RESET
            print(mid)
