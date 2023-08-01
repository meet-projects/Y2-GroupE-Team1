from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
from flask_mail import Mail, Message
import pyrebase


config = {
  "apiKey": "AIzaSyD3j7p217EVs74H4hI3fw_4Ny_z2AwGjXk",
  "authDomain": "travelpack-88791.firebaseapp.com",
  "databaseURL": "https://travelpack-88791-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "travelpack-88791",
  "storageBucket": "travelpack-88791.appspot.com",
  "messagingSenderId": "394939009464",
  "appId": "1:394939009464:web:d331e26c4197a9f97c674d"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'kostande.siaga@gmail.com'
app.config['MAIL_PASSWORD'] = 'llvehmkbmsqshamr'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

   # msg = Message('Hello', sender = 'yourId@gmail.com', recipients = ['someone1@gmail.com'])
   # msg.body = "This is the email body"
   # mail.send(msg)

#Code goes below here


@app.route('/' , methods = ['GET','POST'])
def newsl():
  if request.method=='POST':
    db.child('Email').push(request.form['email'])
  letter = db.child('letter').get().val()
  if letter == None:
    return render_template('newsletter.html')
  return render_template('newsletter.html' , letter = letter)

@app.route('/admin' , methods=['GET' , 'POST'])
def change():
  error = ""
  mails = db.child('Email').get().val()
  if request.method == 'POST':
    news = request.form['newspaper']
    # try: 
    recipients=[]
    db.child('letter').set({'newspaper': news})
    for i in mails : 
      recipients.append(mails[i])
    msg = Message('newsletter' , sender= ' kostande.siaga@gmail.com' , recipients = recipients)
    msg.body = news
    mail.send(msg)
    return redirect(url_for('newsl'))
    # except:
    error = 'somthing went wrong'
  if mails != None:
    return render_template('letter.html' , mails = mails , error = error)
  return render_template('letter.html' , error = error)




#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)