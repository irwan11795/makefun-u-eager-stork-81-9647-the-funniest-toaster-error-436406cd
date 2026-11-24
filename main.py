"""The Funniest Toaster Error Message — make.fun entry.

Writes the single-line entry to entry.txt.
Standard library only, deterministic, no network.
"""

import os
import sys
import tempfile

ENTRY = "ERROR E04: Heating element has unionized. Breakfast is postponed until further notice."


def validate(entry=ENTRY):
    """Gate: entry must be 1-120 UTF-8 chars, one line, no trailing newline."""
    if not entry or not entry.strip():
        raise ValueError("entry must not be empty or whitespace-only")
    if "\n" in entry or "\r" in entry:
        raise ValueError("entry must be a single line")
    if entry.endswith("\n"):
        raise ValueError("entry must not end with a trailing newline")
    if len(entry) > 120:
        raise ValueError("entry exceeds 120 characters: %d" % len(entry))
    return entry


def resolve_output_dir():
    """Fallback chain: MAKEFUN_OUTPUT_DIR -> /output -> repo output/ -> tmp.

    Each candidate is probed with a real write to confirm it is writable.
    """
    candidates = []
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        candidates.append(env_dir)
    candidates.append("/output")
    candidates.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output"))
    candidates.append(tempfile.gettempdir())

    for candidate in candidates:
        try:
            os.makedirs(candidate, exist_ok=True)
            probe = os.path.join(candidate, ".makefun_write_probe")
            with open(probe, "w", encoding="utf-8") as fh:
                fh.write("probe")
            os.remove(probe)
            return candidate
        except OSError:
            continue
    return tempfile.gettempdir()


def main():
    validate()
    out_dir = resolve_output_dir()
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="") as fh:
        fh.write(ENTRY)
    return 0


if __name__ == "__main__":
    sys.exit(main())
