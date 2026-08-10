"""Datacleaner: utilidades para inspección y limpieza de CSV.

Exporta las funciones principales del paquete para uso desde la línea
de comandos o como librería importable.
"""

from .core import (
    clean_column_name,
    clean_column_names,
    detect_delimiter,
    inspect_csv,
    generate_report,
    clean_file,
    main,
)

__all__ = [
    "clean_column_name",
    "clean_column_names",
    "detect_delimiter",
    "inspect_csv",
    "generate_report",
    "clean_file",
    "main",
]

__version__ = "0.1.0"
from .core import (
    clean_column_name,
    clean_column_names,
    detect_delimiter,
    inspect_csv,
    generate_report,
)

__version__ = "0.1.0"

__all__ = [
    "clean_column_name",
    "clean_column_names",
    "detect_delimiter",
    "inspect_csv",
    "generate_report",
]