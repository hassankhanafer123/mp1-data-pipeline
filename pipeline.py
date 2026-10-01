"""
Data Processing Pipeline - CLI Template

DS 3500 - MP1

Usage:
    python pipeline.py --input data.csv --output clean.csv
    python pipeline.py --input data.csv --output results.json --format json --verbose
"""
from data_loaders import load_data
from data_processor import process_data, create_cleaning_report

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
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s")
    pass  # TODO: implement


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Process a data file.")

    parser.add_argument("--input", "-i", required=True,
                        help="Path to the input file")
    parser.add_argument("--output", "-o", required=True,
                        help="Path to the output file")
    parser.add_argument("--config", "-c", required=True,
                        help="Path to YAML configuration file")
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
    if not validate_input(args.config):
        sys.exit(1)
    try:
        data = load_data(args.input)
        logger.info(f"Data loaded successfully from {args.input}")
        config = load_data(args.config)
        logger.info(f"Configuration loaded successfully from {args.config}")
    except ValueError as e:
        logger.error(f"Failed to load files: {e}")
        sys.exit(1)
    original_data = data.copy()
    try:
        cleaned_data = process_data(data, config)
    except ValueError as e:
        logger.error(f"Failed to process data: {e}")
        sys.exit(1)

    report = create_cleaning_report(original_data, cleaned_data)
    print(f"Processing report: {report}")
    logger.info(f"Cleaning report: {report}")

    cleaned_data.to_csv(args.output, index=False)
    logger.info(f"Cleaned data saved to {args.output}")
    


if __name__ == "__main__":
    main()