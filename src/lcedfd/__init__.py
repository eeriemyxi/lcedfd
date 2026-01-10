from ._version import *
from importlib.resources import files

DATA_DB = files("lcedfd.data") / "data.db"


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
