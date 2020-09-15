import argparse
from typing import Optional, Sequence


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    args = parser.parse_args(argv)  # noqa: F841

    return 0
