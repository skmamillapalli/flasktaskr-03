from flask import Flask, request, session, url_for, redirect, render_template, flash, g
from functools import wraps
import _config
import sqlite3
from forms import AddTaskForm

app = Flask(__name__)
app.config.from_object(_config)


def login_required(func):
	@wraps(func)
	def inner(*args, **kwargs):
		if 'logged_in' in session:
			return func(*args, **kwargs)
		else:
			flash("Please login to view the page.")
			return redirect(url_for('login'))
	return inner


@app.route("/", methods=["GET","POST"])
def login():
	status_code = 200
	error = None
	#print(type(request.form))
	if request.method == 'POST':
		if request.form['username'] == app.config['USERNAME'] and request.form['username'] == app.config['PASSWORD']:
			session['logged_in'] = True
			flash('Welcome')
			return redirect(url_for('tasks'))
		else:
			status_code = 401
			error = 'Invalid credentials, please login again.'
			return render_template('login.html', error=error)
	return render_template('login.html')


@app.route("/logout")
@login_required
def logout():
	session.pop('logged_in', None)
	flash('Logged out successfully.')
	return redirect(url_for('login'))

@app.route("/tasks")
@login_required
def tasks():
	g.db = sqlite3.connect(app.config['DATABASE_PATH'])
	cur = g.db.cursor()
	cur.execute("SELECT name, due_date, priority, task_id from TASKS where status=1")
	open_tasks = [dict(name=row[0], due_date=row[1], priority=row[2], task_id=row[3])  for row in cur.fetchall()]
	cur.execute("SELECT name, due_date, priority, task_id from TASKS where status=0")
	closed_tasks = [dict(name=row[0], due_date=row[1], priority=row[2], task_id=row[3])  for row in cur.fetchall()]
	return render_template('tasks.html', form=AddTaskForm(request.form), closed_tasks=closed_tasks, open_tasks=open_tasks)

# Add new task
@app.route('/add/', methods=['POST'])		
@login_required
def new_task():	
	g.db = sqlite3.connect(app.config['DATABASE_PATH'])
	name = request.form['name']
	due_date = request.form['due_date']
	priority = request.form['priority']
	status = 1
	if not name or not due_date or not priority:
		flash('All fields are mandatory')
		return redirect(url_for('tasks'))
	g.db.execute("INSERT INTO TASKS(name, due_date, priority, status) VALUES(?,?,?,?)", [name, due_date, priority, 1])
	g.db.commit()
	g.db.close()
	flash('New entry was posted successfully, Thanks!')
	return redirect(url_for('tasks'))	

#Mark a task as complete
@app.route('/complete/<int:task_id>/')
@login_required
def complete(task_id):
	g.db=sqlite3.connect(app.config['DATABASE_PATH'])
	g.db.execute('UPDATE tasks set status=0 where task_id='+str(task_id))
	g.db.commit()
	g.db.close()
	flash('The task status was updated')
	return redirect(url_for('tasks'))

@app.route('/delete/<int:task_id>/')
@login_required
def delete_entry(task_id):
	g.db = sqlite3.connect(app.config['DATABASE_PATH'])
	g.db.execute('DELETE from tasks where task_id='+str(task_id))
	g.db.commit()
	g.db.close()
	flash('Record deleted successfully!')
	return redirect(url_for('tasks'))





