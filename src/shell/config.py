import argparse


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="UNIX-like shell emulator"
    )

    parser.add_argument(
        "--vfs",
        help="Path to VFS configuration file",
    )

    parser.add_argument(
        "--script",
        help="Path to startup script",
    )

    return parser.parse_args()