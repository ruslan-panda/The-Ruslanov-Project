import sqlite3

with sqlite3.connect("journeys.db") as con:
    cur = con.cursor()
    result = cur.execute("""SELECT * FROM the_best
                    """)
    con.commit()
for i in result:
    print(i)
