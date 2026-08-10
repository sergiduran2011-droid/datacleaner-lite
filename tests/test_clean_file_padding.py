import csv

import datacleaner as dc


def test_padding_and_fill(tmp_path):
    p = tmp_path / "in.csv"
    # second row has only two columns -> should be padded to match headers
    p.write_text("A,B,C\n1,2\n3,4,5\n", encoding="utf-8")

    out = dc.clean_file(p)
    assert out.exists()

    with open(out, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        hdr = next(reader)
        rows = list(reader)
        assert len(rows[0]) == len(hdr)
        # missing value padded as empty string
        assert rows[0][2] == ''
