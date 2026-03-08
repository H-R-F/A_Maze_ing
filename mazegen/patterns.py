from mazegen.generator import ALL_WALLS

PATTERN_42 = [
    "#...###",
    "#.....#",
    "###.###",
    "..#.#..",
    "..#.###",
]


def inject_42_pattern(
    grid: list[list[int]],
    width: int,
    height: int,
) -> set[tuple[int, int]]:
    """Inject '42' pattern into the grid. Return set of pattern cells."""
    pattern_h = len(PATTERN_42)
    pattern_w = max(len(row) for row in PATTERN_42)

    if width < pattern_w + 2 or height < pattern_h + 2:
        return set()

    start_x = (width - pattern_w) // 2
    start_y = (height - pattern_h) // 2

    blocked: set[tuple[int, int]] = set()

    for py, row_str in enumerate(PATTERN_42):
        for px, char in enumerate(row_str):
            if char == '#':
                gx = start_x + px
                gy = start_y + py
                grid[gy][gx] = ALL_WALLS
                blocked.add((gx, gy))

    return blocked
