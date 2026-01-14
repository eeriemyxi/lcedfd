import argparse
import sqlite3
import webbrowser

from . import *


def get_version():
    return f"{PACKAGE_NAME} version {VERSION} ({GIT_HASH} {COMP_DATE})"


def main(argv=None) -> None:
    con = sqlite3.connect(DATA_DB)
    parser = argparse.ArgumentParser(description=DESCRIPTION)

    parser.add_argument("query", nargs="?", help="Search text/id/link (inferred)")

    parser.add_argument(
        "--by-id", type=int, help="Find a single entry by ID (overrides query)"
    )

    parser.add_argument(
        "-N",
        "--no-open",
        action="store_true",
        help="Do not open the first result in a web browser",
    )

    parser.add_argument(
        "--version",
        "-V",
        "-v",
        action="version",
        version=get_version(),
    )

    args = parser.parse_args(argv)

    def open_if_needed(row):
        if not args.no_open and row is not None:
            link = row[2]
            print(f"INFO: opened {link=} in your browser")
            webbrowser.open(link, autoraise=True, new=2)

    def find_id(id_):
        row = find_by_id(con, int(id_))
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

    link = match_link(args.query)
    if link:
        print(f"INFO: detected LeetCode link, parsing it as: {link['name']!r}")
        args.query = link["name"]

    rows = find_matches_like(con, args.query)
    if not rows:
        print("ERROR: no results found")
        return

    for row in rows:
        print(format_row(row))

    open_if_needed(rows[0])
