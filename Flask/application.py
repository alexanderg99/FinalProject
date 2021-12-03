from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import re
from datetime import date
import pymysql.cursors
import random


userPrimaryKey = None
loginType = None
permissions = None
airline = None


labels = [
    'JAN', 'FEB', 'MAR', 'APR',
    'MAY', 'JUN', 'JUL', 'AUG',
    'SEP', 'OCT', 'NOV', 'DEC'
]


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

	global  userPrimaryKey
	global  loginType
	global permissions
	global airline

	userPrimaryKey = None
	loginType = None
	permissions = None
	airline = None



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
				with cnx.cursor() as cur:

					sql = '''INSERT INTO airline_staff VALUES ('{}','{}','{}','{}','{}','{}')'''.format(username,password1,first_name,last_name,dob,airlineName)



					sql2 = '''INSERT INTO permission VALUES ('{}', 'None')'''.format(username)

					cur.execute(sql)
					cur.execute(sql2)

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

					return render_template('booking_agent_purchasing.html',ticket_ID=ticket_ID,today=today)

					#return booking_agent_purchasing(ticket_ID,today)
					#return redirect(url_for('booking_agent_purchasing',ticket_ID=ticket_ID,today=today))
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
	return render_template('customer_ticketspurchased.html', message=message, loginType = loginType)


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

		if permissions == 'Operator':

			flight_num = request.form.get('flight_num')
			airline_name = request.form.get('airline_name')
			print(airline_name)
			print(flight_num)
			return render_template('change_status.html',flight_num=flight_num,airline_name=airline_name)

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
def booking_agent_purchasing():

	if request.method == 'POST':
		if request.form.get('customer_email'):
			print("Harraozzzz")
			with cnx.cursor() as cur:
				email = request.form.get('customer_email')
				ticket_ID = request.form.get('ticket_ID')
				today = request.form.get('today')

				print(ticket_ID)

				user = userPrimaryKey
				query = '''INSERT INTO purchases VALUES ('{}','{}','{}','{}')'''.format(ticket_ID, email, user, today)
				cur.execute(query)

			cnx.commit()

			message = 'You have helped user with email {} buy the ticket! Your ticket number is {}'.format(email,
																								  ticket_ID)

			print("Hello")
			return customer_ticketspurchased(message)
	#return render_template('booking_agent_purchasing.html')




@app.route('/airline_staff_home')
def airline_staff_home():
	global userPrimaryKey
	global loginType
	global airline
	global permissions

	airline = 'China Eastern'
	userPrimaryKey = 'alexg99'
	loginType = 'staff'

	with cnx.cursor() as cur:
		query = "SELECT airline_name from airline_staff where username = '{}'".format(userPrimaryKey)
		cur.execute(query)
		data = cur.fetchone()
		airline = data['airline_name']



	with cnx.cursor() as cur:
		query = "SELECT permission_type from permission where username = '{}'".format(userPrimaryKey)
		cur.execute(query)
		data = cur.fetchone()
		if data['permission_type'] == 'Admin':
			permissions = 'Admin'
		elif data['permission_type'] == 'Operator':
			permissions = 'Operator'


	if permissions:
		return render_template('airline_staff_home.html', name=permissions)


	return render_template('airline_staff_home.html', name='Alex G')

@app.route('/create_flight', methods=['GET','POST'])
def create_flight():

	if request.method == 'POST':


		flight_num = request.form.get('flight_num')
		departure_airport = request.form.get('departure_airport')
		departure_time = request.form.get('departure_time')
		arrival_airport = request.form.get('arrival_airport')
		arrival_time = request.form.get('arrival_time')
		price = request.form.get('price')
		status = request.form.get('status')
		airplane_ID = request.form.get('airplane_number')

		query = "INSERT INTO flight VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(airline,flight_num,departure_airport,departure_time,arrival_airport,arrival_time,price,status,airplane_ID)

		with cnx.cursor() as cur:
			cur.execute(query)

		cnx.commit()

		message = 'Successfully Created!'

		generate_seats(airline,flight_num,airplane_ID)

		return render_template('customer_ticketspurchased.html', message=message, loginType=loginType)
	return render_template('create_flight.html')



def generate_seats(airline_name,flight_num,airplane_ID):
	query = "SELECT airplane.seats from airplane natural join flight where flight.airplane_ID = '{}' and flight.airline_name = '{}'".format(airplane_ID,airline_name)
	with cnx.cursor() as cur:
		cur.execute(query)
	cnx.commit()


	data = cur.fetchone()
	print(data['seats'])



	for i in range(data['seats']):
		with cnx.cursor() as cur:
			query = "INSERT INTO ticket VALUES ('{}','{}','{}')".format(random.randint(10,999999),airline_name,flight_num)
			cur.execute(query)
			print('Added Ticket!')
		cnx.commit()









@app.route('/add_airplane', methods=['GET','POST'])
def add_airplane():

	if request.method == 'POST':

		airline_name = request.form.get('airline_name')
		flight_ID = request.form.get('flight_ID')
		seats = request.form.get('seats')

		query = "INSERT INTO flight VALUES ('{}','{}','{}')".format(airline_name,flight_ID,seats)
		with cnx.cursor() as cur:
			cur.execute(query)

		cnx.commit()

		message = 'Successfully Created!'

		return render_template('customer_ticketspurchased.html', message=message, loginType=loginType)
	return render_template('add_airplane.html')


@app.route('/add_airport', methods=['GET','POST'])
def add_airport():

	if request.method == 'POST':

		airport_name = request.form.get('airport_name')
		airport_city = request.form.get('airport_city')

		query = "INSERT INTO airport VALUES ('{}','{}')".format(airport_name,airport_city)

		with cnx.cursor() as cur:
			cur.execute(query)

		cnx.commit()

		message = 'Successfully Created!'

		return render_template('customer_ticketspurchased.html', message=message, loginType=loginType)
	return render_template('add_airport.html')

@app.route('/change_status', methods=['GET','POST'])
def change_status():

	if request.method == 'POST':

		airline_name = request.form.get('airline_name')
		flight_number = request.form.get('flight_num')
		new_status = request.form.get('new_status')

		print(airline_name)
		print(flight_number)

		query = "UPDATE flight SET status = '{}' WHERE airline_name = '{}' and flight_num = '{}'".format(new_status,airline_name,flight_number)

		with cnx.cursor() as cur:
			cur.execute(query)

		cnx.commit()

		message = 'Successfully Updated!'

		return render_template('customer_ticketspurchased.html', message=message, loginType=loginType)

	return render_template('change_status.html')

@app.route('/view_flights', methods=['GET','POST'])
def view_flights():
	if loginType == 'staff':
		with cnx.cursor() as cur:
			query = "SELECT * FROM flight WHERE airline_name = '{}'".format(airline)
			cur.execute(query)
			data = cur.fetchall()
			print(permissions)

	return render_template('customer_searchforflights.html', data=data, permission=permissions)


@app.route('/view_agents', methods=['GET','POST'])
def view_agents():
	if loginType == 'staff':
		with cnx.cursor() as cur:
			query = "SELECT * FROM booking_agent natural join booking_agent_work_for WHERE airline_name = '{}'".format(airline)
			cur.execute(query)
			data = cur.fetchall()


	return render_template('view_agents.html', data=data, permission=permissions)






@app.route('/view_customers', methods=['GET','POST'])
def view_customers():
	if loginType == 'staff':
		with cnx.cursor() as cur:
			query = "SELECT customer.name FROM ticket natural join purchases natural join customer WHERE ticket.airline_name = '{}'".format(airline)
			print(airline)
			cur.execute(query)
			data = cur.fetchall()
			print(data)


	return render_template('view_customers.html', data=data, permission=permissions)



@app.route('/view_reports', methods=['GET','POST'])
def view_reports():
	if loginType == 'staff':
		with cnx.cursor() as cur:


			query = "SELECT sum(flight.price) as sales FROM ticket natural join purchases natural join flight WHERE ticket.airline_name = '{}'".format(airline)
			print(airline)
			cur.execute(query)
			data = cur.fetchall()
			print(data)


	return render_template('view_reports.html', data=data, permission=permissions)

@app.route('/compare_revenue_earned', methods=['GET','POST'])
def compare_revenue_earned():
	if loginType == 'staff':
		with cnx.cursor() as cur:


			query = "SELECT sum(flight.price) as sales FROM ticket natural join purchases natural join flight WHERE ticket.airline_name = '{}'".format(airline)
			print(airline)
			cur.execute(query)
			data = cur.fetchall()
			print(data)


	return render_template('compare_revenue_earned.html', data=data, permission=permissions)



@app.route('/view_destinations', methods=['GET','POST'])
def view_destinations():
	if loginType == 'staff':
		with cnx.cursor() as cur:
			query = "SELECT * FROM airport"
			cur.execute(query)
			data = cur.fetchall()
			print(data)


	return render_template('view_destinations.html', data=data, permission=permissions)


@app.route('/grant_new_permissions', methods=['GET','POST'])
def grant_new_permissions():
	if permissions == "Admin":

		if request.method == 'POST':

			new_status = request.form.get('new_status')
			username = request.form.get('username')

			print(new_status)
			print(username)
			query = "UPDATE permission SET permission_type = '{}' WHERE username = '{}'".format(new_status,
																											 username)
			with cnx.cursor() as cur:
				cur.execute(query)

			cnx.commit()

			message = 'Permission Changed!'

			return render_template('customer_ticketspurchased.html', message=message, loginType=loginType)




		with cnx.cursor() as cur:
			query = "SELECT * FROM airline_staff left join permission on airline_staff.username = permission.username"
			print(airline)
			cur.execute(query)
			data = cur.fetchall()
			print(data)


	return render_template('grant_new_permissions.html', data=data, permission=permissions)


@app.route('/add_agents', methods=['GET','POST'])
def add_agents():

	if request.method == 'POST':

		email = request.form.get('email')

		with cnx.cursor() as cur:
			query = "INSERT INTO booking_agent_work_for values ('{}','{}')".format(email,airline)
			cur.execute(query)
		cnx.commit()




	with cnx.cursor() as cur:
		query = "SELECT booking_agent.* FROM booking_agent left join booking_agent_work_for on booking_agent.email = booking_agent_work_for.email where booking_agent_work_for.airline_name is null"
		cur.execute(query)
		data = cur.fetchall()
		print(data)


	return render_template('view_agents.html', data=data, redir=add_agents)









if __name__ == '__main__':
    app.run()

'''
@app.errorhandler(404):
def page_not_found(e):
	return render_template("404.html")
'''