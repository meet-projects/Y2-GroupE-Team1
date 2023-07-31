from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
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
app.config['SECRET_KEY'] = 'super-secret-key'

#Code goes below here

@app.route('/admin' , methods=['GET' , 'POST'])
def change():
  error = ""
  if request.method== 'POST':
    letter = request.form['letter']
    try: 
        db.child('letter').set({'text':letter})
        return redirect(url_for('newsl'))
    except:
      error = 'somthing went wrong'
  return render_template('letter.html' , error = error)


@app.route('/' , methods = ['GET','POST'])
def newsl():
  if request.method=='POST':
    db.child('Email').push(request.form['email'])
  letter = db.child('letter').get().val()
  if letter == None:
    return render_template('newsletter.html')
  return render_template('newsletter.html' , letter = letter)



#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)