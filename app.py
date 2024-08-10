from flask import Flask,session,render_template,request,redirect,url_for,flash
from user import user_operation
from encryption import Encryption
import speechapp
import talkingapp
import time



app=Flask(__name__)
app.secret_key = 'nahsgtwjmbhkacsbkjvjvsv' 

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/choice')
def choice():
	msg = "welcome to voice mailing app. Choose either you want to login or register give your choice" 
	talkingapp.talk(msg)
	try:
		data = speechapp.say()
		if(data=='login'):
			return redirect(url_for('user_email'))
		elif(data=='register'):
			return redirect(url_for('user_name'))
		else:
			msg = "You have choose an incorrect option. please choose a valid option." 
			talkingapp.talk(msg)
			return redirect(url_for('choice'))
	except Exception as e:
		msg = "Your Voice is not audible."
		talkingapp.talk(msg)
		return redirect(url_for('choice'))


@app.route('/user_name')
def user_name():
		msg = "please tell me your name"
		talkingapp.talk(msg)
		try:
			data = speechapp.say()
			if(data):
				data = data.replace(" ","")
			return render_template('user_name.html',name=data)
		
		except Exception as e:
			msg = "Your Voice is not audible."
			talkingapp.talk(msg)
			return redirect(url_for('user_name'))

@app.route('/user_create_email')
def user_create_email():
		msg = "please tell me your email id"
		talkingapp.talk(msg)
		name=request.args.get('name')
		try:
			data = speechapp.say()
			if(data):
				data = str.lower(data)
				data = data.replace(" ","")
				data = data.replace("attherate","@")
				return render_template('user_create_email.html',email=data,name=name)
			else:
				talkingapp.talk("something wrong")
				return redirect(url_for('user_create_email',name=name))
		except Exception as e:
			msg = "Your Voice is not audible."
			talkingapp.talk(msg)
			return redirect(url_for('user_create_email',name=name))

@app.route('/user_create_password',methods=['GET','POST'])
def user_create_password():
		msg = "please tell me Password"
		talkingapp.talk(msg)
		email=request.args.get('email')
		name=request.args.get('name')
		try:
			data = speechapp.say()
			if(data):
				data = str.lower(data)
				data = data.replace(" ","")
				data = data.replace("attherate","@")
				return render_template('user_create_password.html',password=data,email=email,name=name)
			else:
				talkingapp.talk("something wrong")
				return redirect(url_for('user_create_password',email=email,name=name))
		except Exception as e:
			msg = "Your Voice is not audible."
			talkingapp.talk(msg)
			return redirect(url_for('user_create_password',email=email,name=name))
				
@app.route('/user_signup',methods=['GET','POST'])
def user_signup():
	if(request.method=='POST'):
		name = request.form['name']
		email = request.form['email']
		password = request.form['password']
		e = Encryption()
		password = e.convert(password)
		ob = user_operation()
		ob.user_signup(name,email,password)
		msg = "Successfully Registered. Thank you. You can login now."
		talkingapp.talk(msg)
		return redirect(url_for('user_email'))
		
		


@app.route('/user_email')
def user_email():
		msg = "please tell me your email id"
		talkingapp.talk(msg)
		try:
			data = speechapp.say()
			if(data):
				data = str.lower(data)
				data = data.replace(" ","")
				data = data.replace("attherate","@")
				return render_template('user_email.html',email=data)
			else:
				talkingapp.talk("something wrong")
				return redirect(url_for('user_email'))
		except Exception as e:
			msg = "Your Voice is not audible."
			talkingapp.talk(msg)
			return redirect(url_for('user_email'))
	


@app.route('/user_password',methods=['GET','POST'])
def user_password():
		msg = "please tell me Password"
		talkingapp.talk(msg)
		email=request.args.get('email')
		name=request.args.get('name')
		try:
			data = speechapp.say()
			if(data):
				data = str.lower(data)
				data = data.replace(" ","")
				data = data.replace("attherate","@")
				if(name==None):
					return render_template('user_password.html',password=data,email=email)
				else:
					return render_template('user_create_password.html',password=data,email=email,name=name)
		except Exception as e:
			msg = "Your Voice is not audible."
			talkingapp.talk(msg)
			return redirect(url_for('user_password',email=email))
		
@app.route('/user_login_verify',methods=['GET','POST'])
def user_login_verify():
	if(request.method=='POST'):
		email = request.form['email']
		password = request.form['password']
		e = Encryption()
		password = e.convert(password)
		ob = user_operation()
		rc = ob.user_login(email,password)
		if(rc==0):
			msg = "Invalid email Or password please try again"
			talkingapp.talk(msg)
			return redirect(url_for('user_email'))
		else:
			msg = "Welcome "+ session['name']
			talkingapp.talk(msg)
			return redirect(url_for('user_dashboard'))
			



@app.route('/user_logout')
def user_logout():
	if('email' in session):
		session.clear()
		msg = "Logged out successfully"
		talkingapp.talk(msg)
		return redirect(url_for('user_login'))
	else:
		return redirect(url_for('index'))
	
@app.route('/user_dashboard')
def user_dashboard():
	if('email' in session):
		msg = "Welcome" + session['name'] + "to V Mail"
		talkingapp.talk(msg)
		ob = user_operation()
		record = ob.user_inbox_mails()
		return render_template('user_dashboard.html',record = record)
	else:
		msg = "You are not authorized ! Please login first"
		talkingapp.talk(msg)
		return redirect(url_for('user_email'))


@app.route('/user_command')
def user_command():
	if('email' in session):
		msg = "Please say OK MAIL to get your virtual assistant"
		talkingapp.talk(msg)
		try:
			data = speechapp.say()
			if(data):
				if(data == "ok mail"):
					return redirect(url_for('user_assistant'))
				else:
					msg = "invalid command"
					talkingapp.talk(data)
					return redirect(url_for('user_command'))
		except Exception as e:
			msg = "Your Voice is not audible."
			talkingapp.talk(msg)
			return redirect(url_for('user_command'))


@app.route('/user_assistant')
def user_assistant():
	if('email' in session):
		msg = "Please tell a command to proceed like compose mail, read mail or logout"
		talkingapp.talk(msg)
		try:
			data = speechapp.say()
			if(data):
				if(data == "compose mail"):
					return redirect(url_for('user_compose_to'))
				elif(data == "read mail"):
					return redirect(url_for('user_read_mail'))
				elif(data == "logout" ):
					return redirect(url_for('user_logout'))
		except Exception as e:
			msg = "Your Voice is not audible."
			talkingapp.talk(msg)
			return redirect(url_for('user_assistant'))
	else:
		msg = "You are not login yet"
		talkingapp.talk(msg)
		return redirect(url_for('user_email'))

@app.route('/user_compose_to')
def user_compose_to():
		if('email' in session):
			msg = "please tell me receiver email"
			talkingapp.talk(msg)
			try:
				data = speechapp.say()
				if(data):
					data = data.replace(" ","")
					data = data.replace("attherate","@")
				return render_template('user_compose_to.html',receiver=data)
			except Exception as e:
				msg = "Your Voice is not audible."
				talkingapp.talk(msg)
				return redirect(url_for('user_compose_to'))
			
		else:
			msg = "you are not login yet"
			talkingapp.talk()
			return redirect(url_for('user_email'))

@app.route('/user_compose_subject')
def user_compose_subject():
		if('email' in session):
			msg = "please tell me email subject"
			talkingapp.talk(msg)
			rec = request.args.get('rec')	
			try:
				data = speechapp.say()		
				return render_template('user_compose_subject.html',receiver=rec,subject=data)
			except Exception as e:
				msg = "Your Voice is not audible."
				talkingapp.talk(msg)
				return redirect(url_for('user_compose_subject',receiver = rec))			
		else:
			msg = "you are not login yet"
			talkingapp.talk()
			return redirect(url_for('user_email'))

@app.route('/user_compose_message')
def user_compose_message():
		if('email' in session):
			msg = "please tell me email message"
			talkingapp.talk(msg)
			rec = request.args.get('rec')
			sub = request.args.get('sub')	
			try:
				data = speechapp.say()				
				return render_template('user_compose_message.html',receiver=rec,subject=sub,message=data)
			except Exception as e:
				msg = "Your Voice is not audible."
				talkingapp.talk(msg)				
				return redirect(url_for('user_compose_message',receiver = rec,subject = sub))			
		else:
			msg = "you are not login yet"
			talkingapp.talk()
			return redirect(url_for('user_email'))
		
@app.route('/user_compose_mail',methods=['GET','POST'])
def user_compose_mail():
		if('email' in session):
			msg = "Are you sure you want to send this mail ,if yes then say send else say cancel"
			talkingapp.talk(msg)
			rec = request.form['receiver']
			sub = request.form['subject']
			message = request.form['message']	
			try:
				data = speechapp.say()
				if(data):
					if(data=="send"):
						ob = user_operation()
						ob.user_send_mail(rec,sub,message)
						msg = "Mail sent successfully"
						talkingapp.talk(msg)
						return redirect(url_for('user_dashboard'))				
					elif(data=="cancel"):
						msg="your message is not sent"
						talkingapp.talk(msg)
						return redirect(url_for('user_dashboard'))
					else:
						msg = "invalid command"
						talkingapp.talk(msg)
						return redirect(url_for('user_compose_mail',receiver = rec,subject = sub, message = message))
			except Exception as e:
				msg = "Your Voice is not audible."
				talkingapp.talk(msg)
				rec = request.args.get('rec')
				message = request.args.get('message')
				return redirect(url_for('user_compose_mail',receiver = rec,subject = sub, message = message))			
		else:
			msg = "you are not login yet"
			talkingapp.talk()
			return redirect(url_for('user_email'))





if __name__==("__main__"):
	app.run(debug=True)
