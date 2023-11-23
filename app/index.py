from flask import Flask, redirect, render_template, request, session, url_for
import config
import firebase_admin
from firebase_admin import credentials, auth, firestore


cred = credentials.Certificate("todolist-72743-firebase-adminsdk-lc4vw-65935aff33.json")
firebase_admin.initialize_app(cred)
db_firestore = firestore.client()

app = Flask(__name__)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = user['idToken']
            return redirect(url_for('dashboard'))
        except auth.AuthError as e:
            return render_template('acesso.html', error=str(e))

    return render_template('acesso.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            user = auth.create_user(email=email, password=password)
            return redirect(url_for('dashboard'))
        except auth.AuthError as e:
            return render_template('register.html', error=str(e))

    return render_template('register.html')

@app.route('/esqueci_senha', methods=['GET', 'POST'])
def esqueci_senha():
    if request.method == 'POST':
        email = request.form['email']
        auth.send_password_reset_email(email)
        return render_template('acesso_usuario.hmtl')
    return render_template('resetar_senha.html')
        

@app.route('/')
def index():
    return '<h1>Hello, World!</h1>'

if __name__ == '__main__':
    app.run(debug=True)