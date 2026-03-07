def export_maze(
    grid: list[list[int]],
    entry: tuple[int, int],
    exit_pos: tuple[int, int],
    path: str,
    output_file: str,
) -> None:
    """Write maze to file in hex format.

    Args:
        grid: 2D list of wall values (0-15).
        entry: (x, y) of maze entry.
        exit_pos: (x, y) of maze exit.
        path: Solution string like "EESSNW".
        output_file: Path to output file.
    """

    with open(output_file, "w") as f:
        for row in grid:
            line = ""
            for cell in row:
                line += format(cell, "X")
            f.write(line + "\n")
        
        f.write("\n")
        f.write(f"{entry[0]},{entry[1]}\n")
        f.write(f"{exit_pos[0]},{exit_pos[1]}\n")
        f.write(f"{path}\n")
