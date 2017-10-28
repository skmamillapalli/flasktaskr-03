import sqlite3
from _config import DATABASE_PATH
from views import db
from models import Task,User
from datetime import datetime
with sqlite3.connect(DATABASE_PATH) as con:
	cur = con.cursor()
	print(cur.execute("select name from sqlite_master where type = 'table';"))
	print(cur.fetchall())
	#cur.execute("ALTER TABLE task RENAME to old_tasks")
	#db.create_all()
	# Fetch che data from old table
	#cur.execute("SELECT name, due_date, priority, status from old_tasks order by task_id asc")
	#print(cur.fetchall())
	# Get the date from old table

	#data = [(row[0], row[1], row[2], row[3], datetime.now(),1) for row in cur.fetchall()]
	data = [('Finish Real Python Course 2', '2015-10-03', 10, 0, datetime.now(),1), ('test-CI', '2017-10-21',
 1, 0, datetime.now(), 1)]
	#insert into new table
	cur.executemany("INSERT INTO tasks (name,due_date, priority, status, posted_date, user_id) values (?,?,?,?,?,?)", data)
	con.commit()
	#delete old table data
	#cur.execute("drop table old_tasks")