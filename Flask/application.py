from flask import Flask, render_template, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from forms import MusicSearchForm

from flaskext.mysql import MySQL
import pymysql.cursors
import mysql.connector






#create Flask instance
app = Flask(__name__)

#app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_DATABASE_PORT'] = 8080
#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = ''
#app.config['MYSQL_DB'] = 'DatabaseProject'


cnx = pymysql.connect(

							  host='localhost',
							user='root',
	#port=8080,

							  db='FinalProject',
	cursorclass=pymysql.cursors.DictCursor,


                              )



#route create
@app.route('/')
def index():

	#cursor.execute('''INSERT INTO airline VALUES ('Sam')''')
	return render_template('index.html')

#route user
@app.route('/user/<name>')
def user(name):

	return render_template('user.html', name = name)


#form class
app.config['SECRET_KEY'] = "Alexander Gunawan"
class register(FlaskForm):
	name = StringField("Username: ", validators=[DataRequired()])
	password = StringField("Password: ", validators=[DataRequired()])
	submit = SubmitField("Submit")

#login page
@app.route('/login', methods=['GET', 'POST'])
def login():
	name = None
	password = None
	form = register()


	if form.validate_on_submit():

		print('hello')
		name = form.name.data
		form.name.data = ''
		password = form.password.data
		form.password.data = ''
#form.logintype?
		print(name,password)

	return render_template('login.html', name=name, password=password, form=form)

@app.route('/registers',  methods=['GET', 'POST'])
def registers():

	
	

	if request.method == 'POST':


		registerType =  request.form.get('LoginType')



		email = request.form.get('email')
		first_name = request.form.get('firstName')
		password1 = request.form.get('password1')
		password2 = request.form.get('password2')
		buildingNumber = request.form.get('buildingnumber')
		street = request.form.get('Street')
		city = request.form.get('City')
		state = request.form.get('State')
		phoneNumber = request.form.get('Phone Number')
		passportNumber = request.form.get('Passport Number')
		passportExpiration = request.form.get('Passport Expiration')
		passportCountry = street = request.form.get('Street')
		dob = request.form.get('Date of Birth')


		#assert types


		print(registerType)





		if len(email) < 4:
			  flash('Email must be greater than 3 characters.', category='error')




		elif len(first_name) < 2:
		   flash('First name must be greater than 1 character.', category='error')
		elif password1 != password2:
		   flash('Passwords don\'t match.', category='error')
		elif len(password1) < 7:
		   flash('Password must be at least 7 characters.', category='error')
		else:
			pass

		

	return render_template('register.html')

					   
@app.route('/search')
def search():
	return render_template('search.html')
#if name = customer, else if name = booking agent



@app.route('/view_public_info', methods=['GET', 'POST'])
def view_public_info():



	pass


if __name__ == '__main__':
    app.run()

'''
@app.errorhandler(404):
def page_not_found(e):
	return render_template("404.html")
'''