*This project has been created as part of the 42 curriculum by aben-sab, moezzoub.*

# A_Maze_ing

## Description

`A_Maze_ing` is a Python project that generates, displays, and exports mazes.
The goal is to build a playable maze application and a reusable maze generation
module named `mazegen`.

The project reads a configuration file, creates a maze, injects a `42` pattern
inside the grid, opens an interactive console mode, and exports the final maze
to a text file.

## Features

- Maze generation with a reusable `mazegen` package
- Config file parsing and validation
- Interactive console display
- Maze solving support
- Export to `maze.txt`
- Optional non-perfect maze generation
- Reproducible generation with an optional seed

## Instructions

### Installation

```zsh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

### Run the project

```zsh
python3 a_maze_ing.py config.txt
```

Or with `make`:

```zsh
make install
make run
```

### Build the reusable package

```zsh
python3 -m build
```

This creates:

- `dist/mazegen-1.0.0.tar.gz`
- `dist/mazegen-1.0.0-py3-none-any.whl`


## Config File Structure

The configuration file uses a simple `KEY=VALUE` format.

Example from `config.txt`:

```txt
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
```

Supported keys:

- `WIDTH`: maze width
- `HEIGHT`: maze height
- `ENTRY`: start cell as `x,y`
- `EXIT`: exit cell as `x,y`
- `OUTPUT_FILE`: output file path
- `PERFECT`: `True` or `False`
- `SEED`: optional integer for reproducible randomness

Rules:

- `WIDTH` and `HEIGHT` must be positive integers
- `ENTRY` and `EXIT` must be inside the maze
- `ENTRY` and `EXIT` must be different
- `OUTPUT_FILE` must not be empty

## Maze Generation Algorithm

The project uses the **Recursive Backtracker** algorithm, implemented as an
iterative depth-first search with a stack in `mazegen/generator.py`.

How it works:

1. Start from one cell
2. Randomly choose an unvisited neighbor
3. Remove the wall between the two cells
4. Continue until there are no unvisited neighbors
5. Backtrack using the stack

When `PERFECT=True`, the maze has exactly one path between any two cells.
When `PERFECT=False`, extra walls may be removed to create additional paths.

## Why This Algorithm

This algorithm was chosen because it is:

- Simple to understand and implement
- Fast enough for this project
- Good for generating clean, solvable mazes
- Easy to adapt with custom blocked cells like the `42` pattern
- Well suited for a reusable module

### Usage Example

Here is a basic example of how to use the `MazeGenerator` in your own project:

```python
from mazegen.generator import MazeGenerator

# 1. Instantiate the generator
gen = MazeGenerator(width=21, height=11, perfect=True, seed=42)

# 2. Generate the maze
gen.generate()

# 3. Access the grid (2D list of integers)
grid = gen.get_grid()

# 4. Use the solver to find a path
from mazegen.solver import solve_maze
path = solve_maze(grid, 21, 11, (0, 0), (20, 10))
print(f"Path: {path}")
```

This entire reusable module (code and documentation) is available in a single
`.whl` or `.tar.gz` file suitable for installation via `pip`.

## Team and Project Management

### Team Roles

This project was developed by:

- `aben-sab`: project design, implementation, and documentation
- `moezzoub`: testing, packaging, and project support

### Planning and Evolution

The project started with the core maze generator and configuration parser.
Then interactive features, export support, packaging, and tests were added.
The packaging setup evolved later to ensure that only `mazegen` is included in
the built distribution.

### What Worked Well

- Clear separation between app code and reusable package code
- Simple config format
- Tests for core modules
- Packaging of `mazegen` as a standalone distribution

### What Could Be Improved

- Add more tests for the interactive part
- Improve the README usage examples
- Expand advanced generation/display options
- Add stricter automation in the `Makefile`

### Tools Used

- Python 3
- `pytest`
- `flake8`
- `mypy`
- `setuptools`
- `build`
- `make`

## Resources

- Python documentation: https://docs.python.org/3/
- `setuptools` documentation: https://setuptools.pypa.io/
- Packaging guide: https://packaging.python.org/
- `pytest` documentation: https://docs.pytest.org/
- Depth-first search overview: https://en.wikipedia.org/wiki/Depth-first_search
- Maze generation overview: https://en.wikipedia.org/wiki/Maze_generation_algorithm

### AI Usage

AI was used as a support tool for:

- Explaining packaging errors
- Improving `pyproject.toml`
- Drafting and structuring documentation
- Reviewing project organization and required README sections

AI was not used as a substitute for project logic validation; the code structure,
packaging decisions, and final verification were still checked inside the project.

## Notes

Advanced behavior currently included in the project:

- Perfect and non-perfect maze generation
- Interactive display/export flow
- Embedded `42` pattern inside the maze when dimensions allow it
