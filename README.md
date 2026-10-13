# MP1 Data Pipeline

This project is a command-line data pipeline that loads a raw data file, validates it, cleans it, and saves the cleaned result as a CSV. Data moves through four stages: the input file and a YAML configuration are loaded, the DataFrame is validated, the enabled cleaning steps are applied, and the cleaned data is written to the output path. `pipeline.py` coordinates the whole run, parsing the command-line arguments and calling each stage in order. The `src/` package holds the modules: `data_loaders.py` reads CSV, JSON, and YAML files based on their extension, and `data_validator.py` checks that the required columns exist and removes rows with invalid numeric values. `data_processor.py` removes duplicates, missing values, and outliers (IQR or z-score) according to the settings in `config/config.yaml`, and also builds a cleaning report. `data_output.py` saves the cleaned DataFrame, creating the output directory if needed, while `utils.py` provides logging setup and input-file validation. Because every cleaning setting lives in the configuration file, the pipeline's behavior can be changed without editing any code.

## Usage

```bash
python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
```

## Example Output

```text
21:11:12 DEBUG    __main__ — Arguments received: Namespace(input='fixtures/sample_data.csv', output='output/clean.csv', config='config/config.yaml', verbose=True)
21:11:12 INFO     src.utils — Input file validated: fixtures/sample_data.csv
21:11:12 INFO     src.utils — Input file validated: config/config.yaml
21:11:12 INFO     __main__ — Data loaded successfully from fixtures/sample_data.csv
21:11:12 INFO     __main__ — Configuration loaded successfully from config/config.yaml
21:11:12 WARNING  src.data_validator — Removed 2 rows with invalid numeric values in rating
21:11:12 DEBUG    src.data_validator — Validation: 100 -> 98 rows (2 removed)
21:11:12 INFO     __main__ — Validation complete: 100 -> 98 rows
21:11:12 DEBUG    src.data_processor — before removing duplicates: 98 rows, after: 96 rows, removed: 2 rows
21:11:12 DEBUG    src.data_processor — before handling missing values: 96 rows, after: 94 rows, removed: 2 rows
21:11:12 DEBUG    src.data_processor — Column 'rating' (method=iqr, threshold=1.5): removed 2 rows
21:11:12 INFO     __main__ — Cleaning report: {'rows_before': 98, 'rows_after': 92, 'rows_removed': 6, 'columns_before': 5, 'columns_after': 5, 'columns_removed': 0}
21:11:12 DEBUG    src.data_output — Saved 92 rows to output\clean.csv
21:11:12 INFO     __main__ — Saved cleaned data to output\clean.csv
Processing report: {'rows_before': 98, 'rows_after': 92, 'rows_removed': 6, 'columns_before': 5, 'columns_after': 5, 'columns_removed': 0}
```
