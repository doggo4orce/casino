import sqlite3

con = sqlite3.connect(":memory:")
con.row_factory = sqlite3.Row

curs = con.cursor()

curs.execute("CREATE TABLE testtable (first text, last text, age int, PRIMARY KEY (first, last))")
curs.execute("INSERT INTO testtable (first, last, age) VALUES ('roobiki', 'tendo', 40)")
curs.execute("INSERT INTO testtable (first, last, age) VALUES ('doggo', 'rover', 41)")
curs.execute("INSERT INTO testtable (first, last, age) VALUES ('doggo', 'rover', 42)")
con.commit()

curs.execute("SELECT * FROM testtable")

for row in curs.fetchall():
  print(str(dict(row)))

