import re
from importlib.resources import files

from ._version import *

DATA_DB = files("lcedfd.data") / "data.db"
RE_LC_LINK = re.compile(
    r"https?:\/\/leetcode.com\/problems\/(?P<name>[a-z,A-Z,\-]+)\/?"
)


def find_matches_like(con, query: str):
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


def find_by_id(con, id: int):
    cur = con.cursor()
    cur.execute("SELECT * FROM lceds WHERE id = ?;", [id])
    return cur.fetchone()


def format_row(row):
    if row is None:
        return "No result"

    return "\n".join(f"{k:>8}: {v}" for k, v in zip(("id", "name", "link"), row))


def match_link(text: str):
    return RE_LC_LINK.match(text)
