from dataclasses import dataclass
from typing import cast

MANDATORY_KEYS = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"}


@dataclass(frozen=True)
class Config:
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None = None


def load_lines(filepath: str) -> list[str]:
    """Load all lines from a config file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.readlines()


def parse_line(line: str, lineno: int) -> tuple[str, str] | None:
    """Parse a KEY=VALUE line. Returns None for empty lines or comments."""
    s = line.strip()

    if not s:
        return None

    if s.startswith("#"):
        return None

    key, sep, value = s.partition("=")
    if sep == "":
        raise ValueError(
            f"Line {lineno}: invalid format (expected KEY=VALUE): {s!r}")

    key = key.strip()
    value = value.strip()

    if not key:
        raise ValueError(f"Line {lineno}: empty key")
    if value == "":
        raise ValueError(f"Line {lineno}: empty value for key {key!r}")

    return key, value


def parse_int(value: str, key: str, lineno: int) -> int:
    """Parse value as integer."""
    try:
        return int(value)
    except ValueError as e:
        raise ValueError(
            f"Line {lineno}: {key} must be an integer, got {value!r}") from e


def parse_bool(value: str, lineno: int) -> bool:
    """Parse value as boolean ('true' or 'false')."""
    v = value.strip().lower()
    if v == "true":
        return True
    if v == "false":
        return False
    raise ValueError(
        f"Line {lineno}: PERFECT must be True/False, got {value!r}")


def parse_coord(value: str, key: str, lineno: int) -> tuple[int, int]:
    """Parse value as coordinate tuple (x,y)."""
    parts = [p.strip() for p in value.split(",")]
    if len(parts) != 2:
        raise ValueError(f"Line {lineno}: {key} must be 'x,y', got {value!r}")
    try:
        x = int(parts[0])
        y = int(parts[1])
    except ValueError as e:
        raise ValueError(
            f"Line {lineno}: {key} coord must be ints, got {value!r}") from e
    return (x, y)


def cast_by_key(key: str, value: str,
                lineno: int) -> int | tuple[int, int] | str | bool:
    """Cast value to appropriate type based on key."""
    k = key.upper()

    if k in ("WIDTH", "HEIGHT"):
        return parse_int(value, k, lineno)

    if k in ("ENTRY", "EXIT"):
        return parse_coord(value, k, lineno)

    if k == "OUTPUT_FILE":
        return value.strip()

    if k == "PERFECT":
        return parse_bool(value, lineno)

    if k == "SEED":
        return parse_int(value, k, lineno)

    raise ValueError(f"Line {lineno}: unknown key {key!r}")


def build_config(lines: list[str]) -> dict[str, object]:
    """Parse lines and build config dictionary."""
    cfg: dict[str, object] = {}

    for lineno, line in enumerate(lines, start=1):
        parsed = parse_line(line, lineno)
        if parsed is None:
            continue

        key, value = parsed
        key_up = key.upper()

        if key_up in cfg:
            raise ValueError(f"Line {lineno}: duplicate key {key_up}")

        cfg[key_up] = cast_by_key(key_up, value, lineno)

    return cfg


def validate_config(cfg: dict[str, object]) -> None:
    """Validate config values (bounds, types, requirements)."""
    missing = [k for k in MANDATORY_KEYS if k not in cfg]
    if missing:
        raise ValueError(
            f"Missing mandatory keys: {', '.join(sorted(missing))}")

    width = cfg["WIDTH"]
    height = cfg["HEIGHT"]

    if not isinstance(width, int) or not isinstance(height, int):
        raise ValueError("WIDTH and HEIGHT must be integers")

    if width <= 0 or height <= 0:
        raise ValueError("WIDTH and HEIGHT must be > 0")

    entry = cfg["ENTRY"]
    exit_ = cfg["EXIT"]

    if entry == exit_:
        raise ValueError(f"ENTRY and EXIT must be different: {entry}")

    for name, pos in (("ENTRY", entry), ("EXIT", exit_)):
        if not (isinstance(pos, tuple)
                and len(pos) == 2 and all(isinstance(n, int) for n in pos)):
            raise ValueError(f"{name} must be a tuple of 2 ints")

        x, y = pos
        if not (0 <= x < width and 0 <= y < height):
            raise ValueError(
                f"{name} out of bounds: "
                f"{pos} for WIDTH={width}, HEIGHT={height}")

    out = cfg["OUTPUT_FILE"]
    if not isinstance(out, str) or not out.strip():
        raise ValueError("OUTPUT_FILE must be a non-empty string")


def get_config(filepath: str) -> Config:
    """Load, parse, and validate config file. Returns Config object."""
    lines = load_lines(filepath)
    cfg_dict = build_config(lines)
    validate_config(cfg_dict)

    return Config(
        width=cast(int, cfg_dict["WIDTH"]),
        height=cast(int, cfg_dict["HEIGHT"]),
        entry=cast(tuple[int, int], cfg_dict["ENTRY"]),
        exit=cast(tuple[int, int], cfg_dict["EXIT"]),
        output_file=cast(str, cfg_dict["OUTPUT_FILE"]),
        perfect=cast(bool, cfg_dict["PERFECT"]),
        seed=cast(int | None, cfg_dict.get("SEED")),
    )
