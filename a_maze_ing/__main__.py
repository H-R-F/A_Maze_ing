import argparse
import sys

from a_maze_ing.config_parser import get_config
from a_maze_ing.interactive import run_interactive
from a_maze_ing.visualizer import display_maze, clear_screen
from mazegen.formatter import export_maze
from mazegen.generator import MazeGenerator
from mazegen.patterns import inject_42_pattern
from mazegen.solver import solve_maze


def build_parser() -> argparse.ArgumentParser:
    """Build CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="a_maze_ing",
        description="Generate, display, and play a maze in the console.",
    )
    parser.add_argument("config", help="Path to config file")
    parser.add_argument(
        "-p", "--inject-42",
        action="store_true",
        help="Inject the 42 pattern into the generated maze",
    )
    return parser


def main() -> None:
    """Main entry point – always opens the interactive menu."""
    parser = build_parser()
    args = parser.parse_args()

    # ── load config ──────────────────────────────────────────────────────
    try:
        cfg = get_config(args.config)
    except FileNotFoundError:
        print(f"Error: config file not found: {args.config}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Config error: {e}", file=sys.stderr)
        sys.exit(1)

    width = cfg.width
    height = cfg.height
    entry = cfg.entry
    exit_pos = cfg.exit
    output_file = cfg.output_file
    perfect = cfg.perfect
    seed = getattr(cfg, "seed", None)

    # ── generate maze ────────────────────────────────────────────────────
    generator = MazeGenerator(
        width=width, height=height, perfect=perfect, seed=seed
    )
    generator.generate()
    grid = generator.get_grid()

    # ── inject 42 pattern (optional) ─────────────────────────────────────
    pattern_cells: set[tuple[int, int]] = set()
    if args.inject_42:
        result = inject_42_pattern(grid, width, height)
        pattern_cells = result if isinstance(result, set) else set()

    # ── run interactive menu ─────────────────────────────────────────────
    grid, pattern_cells, path = run_interactive(
        grid=grid,
        width=width,
        height=height,
        entry=entry,
        exit_pos=exit_pos,
        perfect=perfect,
        seed=seed,
        pattern_enabled=args.inject_42,
        pattern_cells=pattern_cells,
    )

    # ── export on exit ───────────────────────────────────────────────────
    export_maze(
        grid=grid,
        entry=entry,
        exit_pos=exit_pos,
        path=path,
        output_file=output_file,
    )
    print(f"\n✓ Maze exported to: {output_file}")


if __name__ == "__main__":
    main()