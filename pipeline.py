"""
Data Processing Pipeline - CLI Template

DS 3500 - MP1

Usage:
    python pipeline.py --input data.csv --output clean.csv
    python pipeline.py --input data.csv --output results.json --format json --verbose
"""
from src import (
    create_cleaning_report,
    load_data,
    process_data,
    save_data,
    setup_logging,
    validate_dataframe,
    validate_input,
)

import argparse
import logging
import sys
from pathlib import Path


logger = logging.getLogger(__name__)


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
    required_columns = config["validation"]["required_columns"]
    numeric_columns = config["validation"]["numeric_columns"]
    rows_before_validation = len(data)
    try:
        data = validate_dataframe(data, required_columns, numeric_columns)
    except ValueError as e:
        logger.error(f"Validation failed: {e}")
        sys.exit(1)
    logger.info(f"Validation complete: {rows_before_validation} -> {len(data)} rows")
    original_data = data.copy()
    try:
        cleaned_data = process_data(data, config)
    except ValueError as e:
        logger.error(f"Failed to process data: {e}")
        sys.exit(1)

    report = create_cleaning_report(original_data, cleaned_data)
    logger.info(f"Cleaning report: {report}")

    output_path = save_data(cleaned_data, args.output)
    logger.info(f"Saved cleaned data to {output_path}")
    print(f"Processing report: {report}")
    


if __name__ == "__main__":
    main()