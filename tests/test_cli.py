import csv
import sys

import datacleaner as dc


def test_report_cli(tmp_path, capsys, monkeypatch):
    p = tmp_path / "data.csv"
    p.write_text("id,name\n1,Alice\n2,Bob\n", encoding="utf-8")

    monkeypatch.setattr(sys, "argv", ["datacleaner", "report", str(p)])
    dc.main()
    captured = capsys.readouterr()
    assert p.name in captured.out
    assert "Filas" in captured.out


def test_clean_cli(tmp_path, monkeypatch):
    p = tmp_path / "in.csv"
    p.write_text("Name , Age\nAlice , 30\nAlice , 30\n\n", encoding="utf-8")
    out = tmp_path / "out.csv"

    monkeypatch.setattr(sys, "argv", ["datacleaner", "clean", str(p), "-o", str(out)])
    dc.main()

    assert out.exists()
    with open(out, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        hdr = next(reader)
        rows = list(reader)
        assert any("name" in h for h in hdr)
        # duplicates removed -> only 1 data row
        assert len(rows) == 1
