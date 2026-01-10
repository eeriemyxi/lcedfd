import json
import re
import sqlite3
from io import StringIO
from pathlib import Path

PACKAGE_NAME = "lcedfd"
RE_LINK = re.compile(r"\[(?P<id>\d+)\.\W+(?P<name>.+)\]\((?P<link>.*)\)")


def initialize(root, version, build_data):
    assets = root / "assets"
    out = root / "src" / PACKAGE_NAME / "data"
    out.mkdir(parents=True, exist_ok=True)
    (out / "__init__.py").touch() # fails without it

    def process(data: str):
        for match in RE_LINK.finditer(data):
            yield match.groupdict()

    def cleanup(data):
        ds = set()
        for d in data:
            if d["id"] in ds:
                print(f"INFO: Skipping {d=} as part of cleanup")
                continue
            ds.add(d["id"])
            yield d

    # --- read & extract section ---
    with open(assets / "data.md", "r") as file:
        raw = StringIO()
        found = False
        for line in file.readlines():
            if not found:
                if "## Editorials" in line:
                    found = True
                continue
            if "## Premium Problems" in line:
                break
            raw.write(line)

    data_list = list(cleanup(process(raw.getvalue())))

    (out / "data.json").write_text(json.dumps(data_list))

    con = sqlite3.connect(out / "data.db")
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS lceds;")
    cur.execute(
        "CREATE TABLE IF NOT EXISTS lceds("
        "id INTEGER PRIMARY KEY, "
        "name TEXT NOT NULL, "
        "link TEXT NOT NULL UNIQUE)"
    )
    cur.execute(
        "CREATE VIRTUAL TABLE IF NOT EXISTS lceds_fts USING fts5(name, content='lceds', content_rowid='id');"
    )

    cur.executemany(
        "INSERT INTO lceds VALUES (?, ?, ?);",
        (list(e.values()) for e in data_list),
    )
    cur.execute("INSERT INTO lceds_fts(rowid, name) SELECT id, name FROM lceds;")

    con.commit()
    con.close()

    print(
        f"INFO: processed {len(data_list)} matches "
        "into data.json and data.db (SQLite3)"
    )
