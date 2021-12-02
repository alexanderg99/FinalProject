from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import re
from datetime import date
import pymysql.cursors


userPrimaryKey = None
loginType = None

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
	flash("Harrao")

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

		print(name,password)

	return render_template('login.html', name=name, password=password, form=form)


@app.route('/registers',  methods=['GET', 'POST'])
def registers():

	if request.method == 'POST':


		registerType =  request.form.get('LoginType')

		if registerType == "1":

			return redirect(url_for('register_customer'))

		elif registerType == "2":
			return redirect(url_for('register_agent'))

		elif registerType == "3":

			return redirect(url_for('register_staff'))


		print(registerType)

	return render_template('register.html')

@app.route('/register_agent',methods = ['GET','POST'])
def register_agent():
	if request.method == 'POST':
		email = request.form.get('email')
		password1 = request.form.get('password1')
		password2 = request.form.get('password2')

		agentID = request.form.get('agentID')
		with cnx.cursor() as cur:
			query = "SELECT * FROM booking_agent WHERE email = '{}'".format(email)

			cur.execute(query)
			data = cur.fetchone()

			if (data):
				error = "This user already exists!"
				return render_template('register_customer.html', error=error)

			else:
				sql = '''INSERT INTO booking_agent VALUES ('{}','{}','{}')'''.format(email, password1, agentID)
				with cnx.cursor() as cur:
					cur.execute(sql)

				cnx.commit()

				return redirect(url_for('register_success'))

	return render_template('register_agent.html')


@app.route('/register_staff',methods = ['GET','POST'])
def register_staff():
	if request.method == 'POST':
		username = request.form.get('username')
		password1 = request.form.get('password1')
		password2 = request.form.get('password2')
		first_name = request.form.get('firstName')
		last_name = request.form.get('lastName')
		airlineName = request.form.get('airlineName')
		dob = request.form.get('Date of Birth')
		agentID = request.form.get('agentID')

		with cnx.cursor() as cur:
			query = "SELECT * FROM airline_staff WHERE username = '{}'".format(username)

			cur.execute(query)
			data = cur.fetchone()

			if (data):
				error = "This user already exists!"
				return render_template('register_staff.html', error = error)
			else:

				sql = '''INSERT INTO airline_staff VALUES ('{}','{}','{}','{}','{}','{}')'''.format(username,password1,first_name,last_name,dob,airlineName)
				with cnx.cursor() as cur:
					cur.execute(sql)

				cnx.commit()

				return redirect(url_for('register_success'))

	return render_template('register_staff.html')

@app.route('/register_customer',  methods = ['GET','POST'])
def register_customer():



	if request.method == 'POST':
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

		with cnx.cursor() as cur:
			query = "SELECT * FROM customer WHERE email = '{}'".format(email)

			cur.execute(query)
			data = cur.fetchone()

			if (data):
				error = "This user already exists!"
				return render_template('register_customer.html', error=error)
			else:

				sql = '''INSERT INTO customer VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')'''.format(email, first_name,
																									 password1, buildingNumber,
																									 street, city, state,
																									 phoneNumber,
																									 passportNumber,
																									 passportExpiration,
																			 passportCountry, dob)


				with cnx.cursor() as cur:
					cur.execute(sql)

				cnx.commit()

				return redirect(url_for('register_success'))

	return render_template('register_customer.html')

@app.route('/register_success')
def register_success():
	return render_template('register_success.html')


@app.route('/search')
def search():
	return render_template('search.html')
#if name = customer, else if name = booking agent



@app.route('/view_public_info', methods=['GET', 'POST'])
def view_public_info():
	pass


@app.route('/customer_home')
def customer_home():

	global userPrimaryKey
	userPrimaryKey = 'coreychen@nyu.edu'
	return render_template('customer_home.html', name='Corey Chen')


@app.route('/customer_purchasetickets', methods = ['GET','POST'])
def customer_purchasetickets(flight):

	global loginType

	if request.method == 'POST':

		with cnx.cursor() as cur:
			#search for unbought tickets.
			query2 = "SELECT flight.flight_num,ticket.ticket_ID FROM (flight natural join ticket) left join purchases on ticket.ticket_id = purchases.ticket_id where flight.status = 'Upcoming' and ticket.flight_num = '{}' and purchases.customer_email is null".format(
				flight)
			cur.execute(query2)

			data = cur.fetchone()
			if not data:
				message = 'There is no tickets!'
				return customer_ticketspurchased(message)
			else:


				today = date.today()
				today = today.strftime("%m-%d-%y")
				ticket_ID = data['ticket_ID']
				email = userPrimaryKey

				if loginType == 'agent':

					#redirect agent to enter the customer email

					return booking_agent_purchasing(ticket_ID,today)



				else:

					query = '''INSERT INTO purchases VALUES ('{}','{}',null,'{}')'''.format(ticket_ID, email, today)
				cur.execute(query)

			cnx.commit()
		message = 'You have bought the ticket! Your ticket number is {} for flight {}'.format(data['ticket_ID'],
																							  data['flight_num'])

		print("Hello")
		return customer_ticketspurchased(message)


	return render_template('customer_purchasetickets.html', user=userPrimaryKey)

@app.route('/customer_ticketspurchased')
def customer_ticketspurchased(message):
	return render_template('customer_ticketspurchased.html', message=message)


@app.route('/customer_searchforflights',methods = ['GET','POST'])
def customer_searchforflights():
	user = userPrimaryKey
	with cnx.cursor() as cur:
		query = "SELECT * FROM flight WHERE status = 'Upcoming'"
		cur.execute(query)
		data = cur.fetchall()
		print(type(data))
		print(data)
		print(request.method)

	if request.method == 'POST':

		flight_num = request.form.get('flight_num')
		#return redirect(url_for('customer_purchasetickets', flight= flight_num))
		return customer_purchasetickets(flight_num)



	return render_template('customer_searchforflights.html', data=data)

@app.route('/customer_trackmyspending')
def customer_trackmyspending():
	with cnx.cursor() as cur:
		query = "SELECT sum(flight.price) FROM ticket natural join purchases natural join flight WHERE purchases.customer_email = '{}'".format(userPrimaryKey)
		cur.execute(query)
		data = cur.fetchall()
		total = data


	return render_template('customer_trackmyspending.html', data=data[0]['sum(flight.price)'])


@app.route('/customer_viewmyflights')
def customer_viewmyflights():
	global userPrimaryKey
	user = userPrimaryKey
	with cnx.cursor() as cur:
		query = "SELECT * FROM flight natural join ticket natural join purchases WHERE purchases.customer_email = '{}'".format(user)
		cur.execute(query)
		data = cur.fetchall()

		print(type(data))
		print(data)
	return render_template('customer_viewmyflights.html', data=data)


@app.route('/booking_agent_home')
def booking_agent_home():
	global userPrimaryKey
	global loginType
	userPrimaryKey = 23
	loginType = 'agent'
	return render_template('booking_agent_home.html', name='Agent Smith')



@app.route('/booking_agent_viewmyflights')
def booking_agent_viewmyflights():
	global userPrimaryKey
	user = userPrimaryKey
	print(user)
	with cnx.cursor() as cur:
		query = "SELECT * FROM flight natural join ticket natural join purchases WHERE purchases.booking_agent_id = '{}'".format(user)
		cur.execute(query)
		data = cur.fetchall()

		print(type(data))
		print(data)
	return render_template('customer_viewmyflights.html', data=data)


@app.route('/booking_agent_purchasing',methods = ['GET','POST'])
def booking_agent_purchasing(ticket_ID,today):

	if request.method == 'POST':

		if not request.form.get('customer_email'):
			return render_template('booking_agent_purchasing.html')


		else:

			with cnx.cursor() as cur:
				email = request.form.get('customer_email')

				user = userPrimaryKey
				query = '''INSERT INTO purchases VALUES ('{}','{}','{}','{}')'''.format(ticket_ID, email, user, today)
				cur.execute(query)

			cnx.commit()
	return render_template('booking_agent_purchasing.html')

if __name__ == '__main__':
    app.run()

'''
@app.errorhandler(404):
def page_not_found(e):
	return render_template("404.html")
'''