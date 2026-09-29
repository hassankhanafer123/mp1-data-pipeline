"""
Data Processing Pipeline - CLI Template

DS 3500 - MP1

Usage:
    python pipeline.py --input data.csv --output clean.csv
    python pipeline.py --input data.csv --output results.json --format json --verbose
"""

import argparse
import logging
import sys
from pathlib import Path


logger = logging.getLogger(__name__)

## Verbosity = how much information is printed to the console. The higher the level, the more information is printed.
def setup_logging(verbose=False):
    """Configure logging for the pipeline."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        datefmt="%H:%M:%S",
        format="%(asctime)s [%(levelname)s] %(message)s")
    pass  # TODO: implement


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Process a data file.")

    parser.add_argument("--input", "-i", required=True,
                        help="Path to the input file")
    parser.add_argument("--output", "-o", required=True,
                        help="Path to the output file")
    parser.add_argument("--format", choices=["csv", "json"], default="csv",
                        help="Output format")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Enable verbose logging")

    return parser.parse_args()
    pass  # TODO: implement


def validate_input(filepath):
    """Check whether the input path exists and is a file."""
    if not Path(filepath).is_file():
        logger.error(f"Input file not found: {filepath}")
        return False

    logger.info(f"Input file validated: {filepath}")
    return True
    pass  # TODO: implement


def main():
    """Main pipeline function."""
    args = parse_arguments()
    setup_logging(args.verbose)
    logger.debug(f"Arguments received: {args}")
    if not validate_input(args.input):
        sys.exit(1)
    pass  # TODO: implement


if __name__ == "__main__":
    main()