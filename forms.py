from flask_wtf import FlaskForm 
from wtforms import IntegerField, DateField, SelectField, StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Email
class AddTaskForm(FlaskForm):
	task_id = IntegerField()
	name = StringField('Task Name', validators=[DataRequired()])
	due_date = DateField('Date Due() mm/dd/yyyy',validators=[DataRequired()], format='%m/%d/%Y')
	priority = SelectField('Priority', validators=[DataRequired()],
		choices = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'),
('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')
]		)
	status = IntegerField("Status")

class RegisterForm(FlaskForm):
	name = StringField('Username', validators=[DataRequired(), Length(min=3, max=25)])
	email = StringField('Email', validators=[DataRequired(), Email(), Length(min=3, max=40)])	
	password = PasswordField('Password', validators=[DataRequired(), Length(min=3, max=60)])
	confirm = PasswordField('Confirm', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])

class LoginForm(FlaskForm):
	user = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
