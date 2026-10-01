import logging
import pandas as pd

logger = logging.getLogger(__name__)

def remove_duplicates(df):
    """Remove duplicate rows."""
    df_nodup = df.drop_duplicates()
    logger.debug("before removing duplicates: %d rows, after: %d rows", len(df), len(df_nodup))
    return df_nodup


def handle_missing(df, axis="rows"):
    """Drop rows or columns containing missing values."""
    if axis == "rows":
        df_clean = df.dropna(axis=0)
        logger.debug("before handling missing values: %d rows, after: %d rows", len(df), len(df) - len(df_clean))
    elif axis == "columns":
        df_clean = df.dropna(axis=1)
        logger.debug("before handling missing values: %d columns, after: %d columns", df.shape[1],"total removed: %d", df.shape[1]- df_clean.shape[1])
    else:
        raise ValueError(f"Unsupported axis: {axis}")

    return df_clean


def remove_outliers(df, columns, method, threshold):
    """Remove outliers from the specified numeric columns."""
    if method not in ["zscore", "iqr"]:
        logger.error("Unsupported outlier method: %s", method)
        raise ValueError(f"Unsupported method: {method}")

    for col in columns:
        if col not in df.columns:
            logger.warning("Column '%s' not found, skipping", col)
            continue
        if not pd.api.types.is_numeric_dtype(df[col]):
            logger.warning("Column '%s' is not numeric, skipping", col)
            continue
        rows_before = len(df)  
        if method == "zscore":
            mean = df[col].mean()
            std = df[col].std()
            if std != 0:
                df = df[(df[col] - mean).abs() <= threshold * std]
        elif method == "iqr":
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            df = df[(df[col] >= Q1 - threshold * IQR) & (df[col] <= Q3 + threshold * IQR)]
        rows_after = len(df)
        logger.debug("Column '%s': before removing outliers: %d rows, after: %d rows", col, rows_before, rows_after)
    return df


def process_data(df, config):
    """Apply the processing steps enabled in the configuration."""
    df_processed = df.copy()
    if config.get("remove_duplicates", False):
        df_processed = remove_duplicates(df_processed)
    if config.get("handle_missing", False):
        axis = config.get("handle_missing_axis", "rows")
        df_processed = handle_missing(df_processed, axis=axis)
    if config.get("remove_outliers", False):
        columns = config.get("outlier_columns", [])
        method = config.get("outlier_method", "zscore")
        threshold = config.get("outlier_threshold", 3)
        df_processed = remove_outliers(df_processed, columns, method, threshold)
    return df_processed
    pass


def create_cleaning_report(df_before, df_after):
    """Return a dictionary summarizing the cleaning results."""
    pass