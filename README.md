# datacleaner-lite

[![PyPI version](https://img.shields.io/pypi/v/datacleaner-lite.svg)](https://pypi.org/project/datacleaner-lite/)
[![Actions Status](https://github.com/sergiduran2011-droid/datacleaner-lite/workflows/CI/badge.svg)](https://github.com/sergiduran2011-droid/datacleaner-lite/actions)
[![Python Versions](https://img.shields.io/pypi/pyversions/datacleaner-lite.svg)](https://pypi.org/project/datacleaner-lite/)
[![License](https://img.shields.io/pypi/l/datacleaner-lite.svg)](https://opensource.org/licenses/MIT)

Utilities for inspecting, cleaning and streaming CSV datasets with a small CLI
and a simple Python API.

---

## Features

- Detect CSV delimiter and encoding (gzip + BOM aware)
- Normalize column names
- Remove duplicate rows and trim padding
- Stream large files without loading everything into memory
- CLI and programmatic API

---

## Installation

Install from PyPI:

```bash
pip install datacleaner-lite
```

Or install from source:

```bash
pip install -e .
```

---

## CLI

The package exposes a `datacleaner` CLI entry point.

Basic usage:

```bash
# Inspect a CSV (detect delimiter, encoding, basic metrics)
datacleaner inspect input.csv

# Clean a CSV, write to output (removes duplicates and trims whitespace)
datacleaner clean input.csv -o cleaned.csv

# Show help
datacleaner --help
```

Options (examples):

- `inspect <path>` — Prints detected delimiter, total rows/cols and sample
- `clean <path> -o <out>` — Streams cleaned CSV to `<out>` (defaults to stdout if not provided)

Use `datacleaner --help` for a full list of flags and options.

---

## Python API

Import the package and call the high-level helpers:

```python
import datacleaner as dc

# Inspect a file (returns a dict with metrics)
metrics = dc.inspect_csv("data.csv")
print(metrics)

# Clean a file and return the output path (supports .gz input/output)
out_path = dc.clean_file("data.csv", output_path="cleaned.csv")

# Clean a file streaming to stdout
dc.clean_file("data.csv")

# Generate a report (human-readable) from metrics
report = dc.generate_report(metrics)
print(report)

# Normalize column names
cols = [" First Name ", "AGE (years)"]
clean_cols = dc.clean_column_names(cols)
print(clean_cols)
```

API reference (important functions):

- `inspect_csv(path)` → dict
- `clean_file(in_path, output_path=None, deduplicate=True)` → Path or None
- `clean_column_name(name)` → str
- `clean_column_names(list_of_names)` → list[str]
- `detect_delimiter(path)` → str
- `generate_report(metrics)` → str

---

## Contributing

Contributions welcome. Run tests locally with `pytest` and follow the style
guidelines (pre-commit hooks are configured to run `black`, `isort`, and
`flake8`).

```bash
pre-commit install
pytest -q
```

---

## License

MIT — see `LICENSE` for details.
