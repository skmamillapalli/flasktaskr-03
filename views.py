from flask import Flask, request, session, url_for, redirect, render_template, flash, g
from functools import wraps
import _config
import sqlite3
from forms import AddTaskForm, RegisterForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
import datetime


app = Flask(__name__)
app.config.from_object(_config)
db = SQLAlchemy(app)

from models import Task, User

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
	print(request.form)
	form = LoginForm(request.form)
	#print(type(request.form))
	if request.method == 'POST':
		if form.validate_on_submit():
			#print(form.user.data)
			#print(form.password.data)
			#print(dir(db.session.query(User).filter_by(name=form.user.data)))
			#print(dir(User.query.filter_by(name=form.user.name)))
			# Few diff between above two methods
			c_user = User.query.filter_by(name=form.user.data).first()
			print(c_user)
			if c_user is not None and form.password.data == c_user.password:
				session['logged_in'] = True
				session['user_id'] = c_user.id
				flash('Welcome, ' + form.user.data)
				return redirect(url_for('tasks'))
			else:
				status_code = 401
				error = 'Invalid credentials, please login again.'
				return render_template('login.html', error=error, form=form)
		else:
			error="All fields are required"
	return render_template('login.html', error=error, form=form)

@app.route('/register/', methods=['GET','POST'])
def register():
	error=None
	form = RegisterForm(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			db.session.add(User(form.name.data,form.email.data,form.password.data))
			db.session.commit()
			flash('New user added successfully!! Please login to Continue.')
			return redirect(url_for('login'))
	return render_template('register.html', error=error, form=form)


@app.route("/logout")
@login_required
def logout():
	session.pop('logged_in', None)
	session.pop('user_id', None)
	flash('Logged out successfully.')
	return redirect(url_for('login'))

@app.route("/tasks")
@login_required
def tasks():
	open_tasks = db.session.query(Task).filter_by(status='1').order_by(Task.due_date.asc())
	closed_tasks = db.session.query(Task).filter_by(status='0').order_by(Task.due_date.asc())	
	return render_template('tasks.html', form=AddTaskForm(request.form), closed_tasks=closed_tasks, open_tasks=open_tasks)


####--------https://wtforms.readthedocs.io/en/latest/crash_course.html#rendering-fields--------####
# Add new task
@app.route('/add/', methods=['POST'])		
@login_required
def new_task():	
	form = AddTaskForm(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			new_task = Task(form.name.data,
							form.due_date.data,
							form.priority.data,
							'1',
							datetime.datetime.utcnow(),							
							session['user_id']
							)
			db.session.add(new_task)			
			db.session.commit()
			flash('New entry was posted successfully, Thanks!')
		else:
			flash("Please enter the data in correct format.")
	return redirect(url_for('tasks'))	

#Mark a task as complete
@app.route('/complete/<int:task_id>/')
@login_required
def complete(task_id):
	db.session.query(Task).filter_by(task_id=task_id).update({"status":"0"})
	db.session.commit()
	flash('The task status was updated')
	return redirect(url_for('tasks'))

#Delete the record with the given id
@app.route('/delete/<int:task_id>/')
@login_required
def delete_entry(task_id):
	db.session.query(Task).filter_by(task_id=task_id).delete()
	db.session.commit()	
	flash('Record deleted successfully!')
	return redirect(url_for('tasks'))