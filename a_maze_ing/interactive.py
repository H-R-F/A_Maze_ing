"""Interactive console menu for A_Maze_ing.

Subject requirements:
  1. Re-generate a new maze and display it.
  2. Show/Hide a valid shortest path from entrance to exit.
  3. Change maze wall colours.
  4. Optional: set specific colours to display the "42" pattern.
"""

from a_maze_ing.visualizer import display_maze, clear_screen, WALL_COLOR, PATTERN_COLOR
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
    ("\033[37;2m", "Dim white"),
    ("\033[93;2m", "Dim yellow"),
    ("\033[92;2m", "Dim green"),
    ("\033[96;2m", "Dim cyan"),
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
    pat_idx = 0
    show_path = False

    # Solve for initial maze
    path = solve_maze(grid, width, height, entry, exit_pos)

    while True:
        clear_screen()

        wall_color = WALL_COLORS[wall_idx][0]
        pat_color = PATTERN_COLORS[pat_idx][0] if pattern_cells else PATTERN_COLOR

        display_maze(
            grid=grid,
            width=width,
            height=height,
            entry=entry,
            exit_pos=exit_pos,
            path=path if show_path else None,
            wall_color=wall_color,
            pattern_cells=pattern_cells,
            pattern_color=pat_color,
        )

        print()
        print("== A-Maze-ing ==")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        if pattern_enabled:
            print("4. Rotate 42 pattern colors")
        print("5. Quit")
        print()

        try:
            choice = input("Choice? (1-5): ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if choice == "1":
            gen = MazeGenerator(
                width=width, height=height, perfect=perfect, seed=None
            )
            gen.generate()
            grid = gen.get_grid()

            if pattern_enabled:
                result = inject_42_pattern(grid, width, height)
                pattern_cells = result if isinstance(result, set) else set()
            else:
                pattern_cells = set()

            path = solve_maze(grid, width, height, entry, exit_pos)
            show_path = False

        elif choice == "2":
            show_path = not show_path

        elif choice == "3":
            wall_idx = (wall_idx + 1) % len(WALL_COLORS)

        elif choice == "4" and pattern_enabled:
            pat_idx = (pat_idx + 1) % len(PATTERN_COLORS)

        elif choice == "5":
            break

    return grid, pattern_cells, path or ""
