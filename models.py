from views import db

class Task(db.Model):
	__tablename__ = 'tasks'
	task_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)
	priority = db.Column(db.Integer, nullable=False)
	status = db.Column(db.Integer, nullable=False)
	due_date = db.Column(db.Date, nullable=False)
	posted_date = db.Column(db.Date, nullable= False)
	user_id  = db.Column(db.Integer, db.ForeignKey('users.id'))

	def __init__(self, name, due_date, priority, status, posted_date, user_id):
		self.name = name
		self.priority = priority
		self.status = status
		self.due_date = due_date
		self.posted_date = posted_date
		self.user_id = user_id

	def __repr__(sel):
		return '{} with a priority {}. The current status is {} and due by {}.'.format(self.name, self.priority, self.status, self.due_date)



class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, unique=True, nullable=False)
	email = db.Column(db.String, unique=True, nullable=False)
	password = db.Column(db.String, nullable=False)
	tasks = db.relationship('Task', backref='poster')

	def __init__(self, name, email, password):
		self.name = name
		self.email = email
		self.password = password

	def __repr__(self):
		return '<User {}>'.format(self.name)

