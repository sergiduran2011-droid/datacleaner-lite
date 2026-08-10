import csv
from pathlib import Path

import datacleaner as dc


def test_clean_column_names():
    headers = ["  Name / Surname ", "Age", "Age", "e-mail"]
    cleaned = dc.clean_column_names(headers)
    assert cleaned[0] == "name_surname"
    assert cleaned[1] == "age"
    assert cleaned[2].startswith("age_")


def test_detect_delimiter_and_inspect(tmp_path: Path):
    data = "id;name;age\n1;Alice;30\n2;Bob;25\n"
    p = tmp_path / "sample.csv"
    p.write_text(data, encoding="utf-8")

    delim = dc.detect_delimiter(p)
    assert delim == ";"

    metrics = dc.inspect_csv(p)
    assert metrics["total_rows"] == 2
    assert metrics["total_cols"] == 3
    assert "id" in metrics["headers"]


def test_clean_file(tmp_path: Path):
    data = "Name , Age\nAlice , 30\nAlice , 30\n\n"
    in_file = tmp_path / "in.csv"
    in_file.write_text(data, encoding="utf-8")

    out = dc.clean_file(in_file)
    assert out.exists()
    # leer archivo resultado y comprobar encabezados
    with open(out, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        hdr = next(reader)
        assert "name" in hdr[0]
        rows = list(reader)
        # duplicate row removed -> only 1 data row
        assert len(rows) == 1
