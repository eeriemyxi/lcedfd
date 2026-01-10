import argparse
import sqlite3
import webbrowser
from importlib.resources import files

from . import COMP_DATE, GIT_HASH, VERSION

data_db = files("lcedfd.data") / "data.db"
con = sqlite3.connect(data_db)


def find_matches_like(query: str):
    cur = con.cursor()
    cur.execute(
        """
        SELECT lceds.*
        FROM lceds_fts
        JOIN lceds ON lceds.id = lceds_fts.rowid
        WHERE lceds_fts MATCH ?
        ORDER BY rank;
    """,
        (f'"{query}"',),
    )
    return cur.fetchall()


def find_by_id(id: int):
    cur = con.cursor()
    cur.execute("SELECT * FROM lceds WHERE id = ?;", [id])
    return cur.fetchone()


def format_row(row):
    if row is None:
        return "No result"

    return "\n".join(f"{k:>8}: {v}" for k, v in zip(("id", "name", "link"), row))


def get_version():
    return f"lcedfd version {VERSION} ({GIT_HASH} {COMP_DATE})"


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(description="Search lceds database")

    parser.add_argument("query", nargs="?", help="Search text/id (inferred)")

    parser.add_argument(
        "--by-id", type=int, help="Find a single entry by ID (overrides query)"
    )

    parser.add_argument(
        "-o",
        "--open",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Open the first result in a web browser (default: on)",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=get_version(),
    )

    args = parser.parse_args(argv)

    def open_if_needed(row):
        if args.open and row is not None:
            link = row[2]
            print(f"INFO: Opened {link=} in your browser")
            webbrowser.open(link, autoraise=True, new=2)

    def find_id(id_):
        row = find_by_id(int(id_))
        if row is None:
            print("ERROR: no result found")
            return
        print(format_row(row))
        open_if_needed(row)

    if args.by_id is not None:
        find_id(args.by_id)
        return

    if args.query is None:
        parser.error("missing search text")

    if args.query.isdigit():
        find_id(args.query)
        return

    rows = find_matches_like(args.query)
    if not rows:
        print("ERROR: no results found")
        return

    for row in rows:
        print(format_row(row))

    open_if_needed(rows[0])
