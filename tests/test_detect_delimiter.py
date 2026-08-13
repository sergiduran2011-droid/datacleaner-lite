import datacleaner as dc


def test_detect_commas(tmp_path):
    p = tmp_path / "a.csv"
    p.write_text("a,b,c\n1,2,3\n", encoding="utf-8")
    assert dc.detect_delimiter(p) == ","


def test_detect_semicolon(tmp_path):
    p = tmp_path / "a.csv"
    p.write_text("a;b;c\n1;2;3\n", encoding="utf-8")
    assert dc.detect_delimiter(p) == ";"


def test_detect_tab(tmp_path):
    p = tmp_path / "a.csv"
    p.write_text("a\tb\tc\n1\t2\t3\n", encoding="utf-8")
    assert dc.detect_delimiter(p) == "\t"
