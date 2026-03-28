from mazegen.generator import NORTH, EAST, SOUTH, WEST

RESET = "\033[0m"
WALL_COLOR = "\033[37m"  # WHITE COLOR
PATH_COLOR = "\033[32m"  # GREEN COLOR
ENTRY_COLOR = "\033[34m"  # BLUE COLOR
EXIT_COLOR = "\033[31m"  # RED COLOR
PATTERN_COLOR = "\033[37m"  # DIM WHITE for 42 pattern
ENTRY_MARK = "E"
EXIT_MARK = "X"

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
        entry_mark: str = ENTRY_MARK,
        exit_mark: str = EXIT_MARK,
) -> None:
    """Display maze in terminal using box-drawing characters."""


    import os
    path_cells: list[tuple[int, int]] = []
    if path:
        x, y = entry
        path_cells.append((x, y))
        for ch in path:
            if ch == "N":
                y -= 1
            elif ch == "S":
                y += 1
            elif ch == "E":
                x += 1
            elif ch == "W":
                x -= 1
            path_cells.append((x, y))

    path_set = set(path_cells)

    # --- Terminal size check ---
    try:
        rows, cols = os.popen('stty size', 'r').read().split()
        rows, cols = int(rows), int(cols)
    except Exception:
        rows, cols = 24, 80  # fallback default

    # Each maze row prints 2 lines (sep+mid), each cell is 3 chars wide
    needed_rows = (height + 1) + height
    needed_cols = (width + 1) * 4  # approx, for walls and padding
    if needed_rows > rows or needed_cols > cols:
        print(f"\033[31m[!] Terminal too small for maze: needs {needed_cols}x{needed_rows}, you have {cols}x{rows}.\033[0m")
        print("Resize your terminal or use a smaller maze.")
        return

    def get_path_char(idx: int) -> str:
        if idx == 0 or idx == len(path_cells) - 1:
            return "●"  # Start/end marker
        x0, y0 = path_cells[idx - 1]
        x1, y1 = path_cells[idx]
        x2, y2 = path_cells[idx + 1]
        dx1, dy1 = x1 - x0, y1 - y0
        dx2, dy2 = x2 - x1, y2 - y1
        if (dx1, dy1) == (dx2, dy2):
            if dx1 == 0:
                return "┃"
            else:
                return "━"
        # Turn cases
        if (dx1, dy1) == (0, -1) and (dx2, dy2) == (1, 0):
            return "┏"
        if (dx1, dy1) == (1, 0) and (dx2, dy2) == (0, 1):
            return "┓"
        if (dx1, dy1) == (0, 1) and (dx2, dy2) == (-1, 0):
            return "┛"
        if (dx1, dy1) == (-1, 0) and (dx2, dy2) == (0, -1):
            return "┗"
        if (dx1, dy1) == (0, -1) and (dx2, dy2) == (-1, 0):
            return "┓"
        if (dx1, dy1) == (-1, 0) and (dx2, dy2) == (0, 1):
            return "┏"
        if (dx1, dy1) == (0, 1) and (dx2, dy2) == (1, 0):
            return "┗"
        if (dx1, dy1) == (1, 0) and (dx2, dy2) == (0, -1):
            return "┛"
        return "*"  # fallback

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
                    mid += ENTRY_COLOR + entry_mark + wall_color
                elif (x, hy) == exit_pos:
                    mid += EXIT_COLOR + exit_mark + wall_color
                elif (x, hy) in path_set:
                    idx = path_cells.index((x, hy))
                    # Support rainbow: path_color can be a list of colors
                    if isinstance(path_color, list):
                        color = path_color[idx % len(path_color)]
                    else:
                        color = path_color
                    mid += color + get_path_char(idx) * 3 + wall_color
                elif pattern_cells and (x, hy) in pattern_cells:
                    mid += pattern_color + "███" + wall_color
                else:
                    mid += "   "
            mid += V_WALL if v_wall(width, hy) else " "
            mid += RESET
            print(mid)