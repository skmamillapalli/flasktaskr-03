from _config import DATABASE_PATH
from views import db
from models import Task
from datetime import date 

db.create_all()
#db.session.add(Task("Finish this tutorial", date(2016, 9, 22), 10, 1))
#db.session.add(Task("Finish Real Python Course 2", date(2015, 10, 3), 10, 1))
db.session.commit()
#with sqlite3.connect(DATABASE_PATH) as con:
#	cur = con.cursor()
#	cur.execute('CREATE TABLE IF NOT EXISTS tasks(task_id INTEGER  PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, due_date TEXT NOT NULL, priority INTEGER NOT NULL, status INTEGER NOT NULL )')
#	cur.execute(
#	'INSERT INTO tasks (name, due_date, priority, status)'
##
#	)
#	cur.execute(
#	'INSERT INTO tasks (name, due_date, priority, status)'
#	'VALUES("Finish Real Python Course 2", "03/25/2015", 10, 1)'
#	)


