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

# datacleaner-lite

[![PyPI version](https://img.shields.io/pypi/v/datacleaner-lite.svg)](https://pypi.org/project/datacleaner-lite/)
[![CI status](https://github.com/sergiduran2011-droid/datacleaner-lite/actions/workflows/ci.yml/badge.svg)](https://github.com/sergiduran2011-droid/datacleaner-lite/actions)
[![Python Versions](https://img.shields.io/pypi/pyversions/datacleaner-lite.svg)](https://pypi.org/project/datacleaner-lite/)
[![License](https://img.shields.io/pypi/l/datacleaner-lite.svg)](https://opensource.org/licenses/MIT)

Utilities to inspect, clean and stream CSV datasets. Provides a small CLI
(`datacleaner`) and an ergonomic Python API suitable for pipelines and
batch processing.

---

## Table of contents

- Quickstart
- CLI examples
- Python API
- Development
- Publishing
- Contributing & Support

---

## Quickstart

Install from PyPI:

```bash
pip install datacleaner-lite
```

Inspect a CSV:

```bash
datacleaner inspect data.csv
```

Clean and write output (supports .gz input/output transparently):

```bash
datacleaner clean data.csv -o cleaned.csv
```

Or use programmatically:

```python
import datacleaner as dc

metrics = dc.inspect_csv("data.csv")
print(dc.generate_report(metrics))

dc.clean_file("data.csv", output_path="cleaned.csv")
```

---

## CLI

Usage: `datacleaner <command> [options]`

Common commands:

- `inspect <path>` — detects delimiter, encoding, counts rows/cols and shows a small sample
- `clean <path> -o <out>` — cleans rows (trim, dedupe) and writes CSV to `out` (or stdout)

Examples:

```bash
# Inspect gzipped CSV with BOM
datacleaner inspect data.csv.gz

# Clean, remove duplicate rows, and compress output
datacleaner clean input.csv -o output.csv.gz

# Clean and stream to stdout (pipe into another tool)
datacleaner clean large.csv | gzip > clean.gz
```

Options you may find useful (CLI flags):

- `-o, --output` : output path (if omitted prints to stdout)
- `--deduplicate/--no-deduplicate` : enable/disable deduplication
- `--delimiter` : force delimiter detection override (e.g. `,` or `;`)
- `--encoding` : force input encoding (use with care; default tries detection)

Run `datacleaner <command> --help` for per-command options.

---

## Python API

High-level functions (short API reference):

- `inspect_csv(path: str | Path) -> dict` — Returns metrics: `total_rows`, `total_cols`, `sample_rows`, `delimiter`, `encoding`.
- `clean_file(in_path: str | Path, output_path: Optional[str|Path]=None, deduplicate: bool=True) -> Optional[Path]` — Streams cleaned CSV to `output_path` (or stdout) and returns the output path when given.
- `clean_column_name(name: str) -> str` — Normalizes a single column name (strip, lowercase, remove punctuation).
- `clean_column_names(names: Iterable[str]) -> List[str]` — Applies `clean_column_name` to a sequence.
- `detect_delimiter(path: str | Path) -> str` — Heuristic delimiter detection with fallback.
- `generate_report(metrics: dict) -> str` — Human-readable report string from `inspect_csv` metrics.

Example (detailed):

```python
from pathlib import Path
import datacleaner as dc

in_file = Path("data.csv.gz")
metrics = dc.inspect_csv(in_file)
print(dc.generate_report(metrics))

out = Path("cleaned.csv.gz")
dc.clean_file(in_file, output_path=out)
print("Wrote:", out)
```

Notes:

- `clean_file` will preserve gzip compression if the output filename ends with `.gz`.
- Encoding detection attempts to handle UTF-8 BOM and common encodings; use `--encoding` or `encoding=` parameter to override when necessary.

---

## Development

Run tests and linters locally:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pre-commit install
pre-commit run --all-files
pytest -q
```

Formatting / style:

- `black .`
- `isort --profile black .`

---

## Publishing (PyPI) — OIDC (recommended)

This repository includes `.github/workflows/publish.yml` which builds with `python -m build` and uses the `pypa/gh-action-pypi-publish` action. It is configured to request `id-token: write` so the job can authenticate to PyPI using GitHub's OIDC provider and a Trusted Publisher on PyPI.

Steps to enable Trusted Publisher on PyPI:

1. Go to https://pypi.org/manage/account/ and under *API tokens / Trusted publishers* follow the instructions to register this GitHub repository or organization as a trusted publisher.
2. Ensure the workflow has `permissions: id-token: write` (already present in the workflow file).
3. Create a test release on GitHub and use the manual *Run workflow* button (workflow_dispatch) to trigger publish once configured.

If you prefer using a classic API token (less recommended), create a `PYPI_API_TOKEN` secret in GitHub and switch the workflow to use it instead.

---

## Contributing & Support

Contributions, bug reports and PRs are welcome. Open an issue with a minimal repro if you find a bug.

For questions or maintenance contact: Sergi Durán <sergiduran@local>

Please follow the contributor checklist in `CONTRIBUTING.md` if you add features.

---

## License

MIT — see `LICENSE` for details.
