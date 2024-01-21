import sqlite3

b = 2345
with sqlite3.connect("journeys.db") as con:
    cur = con.cursor()
    result = cur.execute(f"""UPDATE the_best
                            SET first = {b}
                            WHERE first < {b}
                    """)
    con.commit()

