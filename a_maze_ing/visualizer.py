from mazegen.generator import NORTH, EAST, SOUTH, WEST

RESET = "\033[0m"
WALL_COLOR = "\033[37m"  #  WHITE COLOR
PATH_COLOR = "\033[32m"  #* GREEN COLOR
ENTRY_COLOR = "\033[34m" #? BLUE COLOR
EXIT_COLOR = "\033[31m"  #! RED COLOR

def display_maze(
        grid: list[list[int]],
        width: int,
        height: int,
        entry: tuple[int, int],
        exit_pos: tuple[int, int],
        path: str | None = None,
        wall_color: str = WALL_COLOR
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
    
    #border:
    top = wall_color
    for x in range(width):
        if grid[0][x] & NORTH:
            top += "┌───"
        else:
            top += "┌   "
    top += "┐" + RESET
    print(top)

    for y in range(height):
        mid = wall_color
        for x in range(width):
            if grid[y][x] & WEST:
                mid += "|"
            else:
                mid += " "
            
            if (x, y) == entry:
                mid += ENTRY_COLOR + " S " + wall_color
            elif (x, y) == exit_pos:
                mid += EXIT_COLOR + " E " + wall_color
            elif (x, y) in path_cells:
                mid += PATH_COLOR + " . " + wall_color
            else:
                mid += "   "

        if grid[y][width - 1] & EAST:
            mid += "|"
        else:
            mid += " "
        mid += RESET
        print(mid)    
        if y <  height - 1:
            bot = wall_color
            for x in range(width):
                if grid[y][x] & SOUTH:
                    bot += "├───"
                else:
                    bot += "├   "
            bot += "┤" + RESET
            print(bot)
    
    bot = wall_color
    for x in range(width):
        if grid[height - 1][x] & SOUTH:
            bot += "└───"
        else:
            bot += "└   "
    bot += "┘" + RESET
    print(bot)
            

