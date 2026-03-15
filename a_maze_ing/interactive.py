"""Interactive console menu for A_Maze_ing.

Subject requirements:
  1. Re-generate a new maze and display it.
  2. Show/Hide a valid shortest path from entrance to exit.
  3. Change maze wall colours.
  4. Optional: set specific colours to display the "42" pattern.
"""

from a_maze_ing.visualizer import display_maze, PATTERN_COLOR
from a_maze_ing.visualizer import clear_screen
from mazegen.generator import MazeGenerator
from mazegen.patterns import inject_42_pattern
from mazegen.solver import solve_maze

# -- wall colour rotation -----------------------------------------------------
WALL_COLORS = [
    ("\033[37m", "White (default)"),
    ("\033[93m", "Yellow"),
    ("\033[92m", "Green"),
    ("\033[94m", "Blue"),
    ("\033[90m", "Dark"),
]

# -- 42 pattern colour options ------------------------------------------------
PATTERN_COLORS = [
    ("\033[37m", "White"),
    ("\033[93m", "Yellow"),
    ("\033[92m", "Green"),
    ("\033[96m", "Cyan"),
]

# -- path colour options ------------------------------------------------------
PATH_COLORS = [
    ("\033[32m", "Green (default)"),
    ("\033[96m", "Cyan"),
    ("\033[95m", "Magenta"),
    ("\033[93m", "Yellow"),
    ("\033[91m", "Red"),
]


def run_interactive(
    grid: list[list[int]],
    width: int,
    height: int,
    entry: tuple[int, int],
    exit_pos: tuple[int, int],
    perfect: bool = True,
    seed: int | None = None,
    pattern_enabled: bool = False,
    pattern_cells: set[tuple[int, int]] | None = None,
) -> tuple[list[list[int]], set[tuple[int, int]], str]:
    """Run the interactive menu.

    Returns (grid, pattern_cells, path) so __main__ can export.
    """
    if pattern_cells is None:
        pattern_cells = set()

    wall_idx = 0
    path_idx = 0
    pat_idx = 0
    show_path = False

    # Solve for initial maze
    path = solve_maze(grid, width, height, entry, exit_pos)

    while True:
        clear_screen()

        wall_color = WALL_COLORS[wall_idx][0]
        path_color = PATH_COLORS[path_idx][0]
        pat_color = (PATTERN_COLORS[pat_idx][0]
                     if pattern_cells else PATTERN_COLOR)

        display_maze(
            grid=grid,
            width=width,
            height=height,
            entry=entry,
            exit_pos=exit_pos,
            path=path if show_path else None,
            wall_color=wall_color,
            path_color=path_color,
            pattern_cells=pattern_cells,
            pattern_color=pat_color,
        )

        print()
        print("== A-Maze-ing ==")
        print("R. Re-generate a new maze")
        print("P. Show/Hide path from entry to exit")
        print("W. Rotate maze colors")
        print("J. Rotate path colors")
        if pattern_enabled:
            print("M. Rotate 42 pattern colors")
            print("Q. Quit")
            prompt = "Choice? (R-P-W-J-M-Q): "
        else:
            print("Q. Quit")
            prompt = "Choice? (R-P-W-J-Q): "
        print()

        try:
            choice = input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            break

        if choice == "R":
            gen = MazeGenerator(
                width=width, height=height, perfect=perfect, seed=None
            )

            if pattern_enabled:
                pattern_cells = inject_42_pattern(
                    gen.grid, width, height
                )
            else:
                pattern_cells = set()

            gen.generate(blocked=pattern_cells)
            grid = gen.get_grid()

            path = solve_maze(grid, width, height, entry, exit_pos)

        elif choice == "P":
            show_path = not show_path

        elif choice == "W":
            wall_idx = (wall_idx + 1) % len(WALL_COLORS)

        elif choice == "J":
            path_idx = (path_idx + 1) % len(PATH_COLORS)

        elif choice == "M" and pattern_enabled:
            pat_idx = (pat_idx + 1) % len(PATTERN_COLORS)

        elif ((choice == "Q" and pattern_enabled) or
                (choice == "M" and not pattern_enabled)):
            break

        else:
            continue

    return grid, pattern_cells, path or ""
