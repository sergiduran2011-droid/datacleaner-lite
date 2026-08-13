import gzip
from pathlib import Path

import datacleaner as dc


def test_gzip_detect_and_inspect(tmp_path: Path):
    p = tmp_path / "data.csv.gz"
    content = "id;name\n1;Álvaro\n2;Bea\n"
    # write with BOM to test utf-8-sig handling
    with gzip.open(p, mode="wt", encoding="utf-8") as f:
        f.write("\ufeff" + content)

    # detect delimiter and inspect should work on .gz
    delim = dc.detect_delimiter(p)
    assert delim == ";"

    metrics = dc.inspect_csv(p)
    assert metrics["total_rows"] == 2
    assert metrics["total_cols"] == 2


def test_clean_writes_gzip(tmp_path: Path):
    in_p = tmp_path / "in.csv.gz"
    content = "A,B\n1,2\n1,2\n"
    with gzip.open(in_p, mode="wt", encoding="utf-8") as f:
        f.write(content)

    out_p = tmp_path / "out.csv.gz"
    res = dc.clean_file(in_p, output_path=out_p)
    assert res == out_p
    assert out_p.exists()

    # read back
    with gzip.open(out_p, mode="rt", encoding="utf-8") as f:
        lines = f.read().splitlines()
        assert lines[0].lower().startswith("a")
        # only one data row because duplicate removed
        assert len([l for l in lines if l.strip()]) == 2
