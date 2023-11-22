from flask import Flask, render_template, request
import config
import pyrebase


firebase = pyrebase.initialize_app(config)

auth = firebase.auth()



app = Flask(__name__)


@app.route('acesso_usuario', methods=['GET', 'POST'])
def acesso_usuario():
    campo_email = request.form['email']
    campo_senha = request.form['senha']
    try:
        if request.method == 'POST':
            auth.sign_in_with_email_and_password(campo_email, campo_senha)
            info_usuario = auth.sign_in_with_email_and_password(campo_email, campo_senha)
            info_conta = auth.get_account_info(info_usuario['idToken'])
            if info_conta['user'][0]['emailVerified'] == False:
                mensagem_verificar = 'Verifique seu email'
                return render_template('acesso_usuario.html', mensagem_verificar=mensagem_verificar)
        return render_template('pagina_principal.html')
    except:
        mensagem_sem_sucesso = 'Email/Senha Incorretos'
        return render_template('acesso_usuario.html', mensagem_sem_sucesso=mensagem_sem_sucesso)

@app.route('/cadastro_usuario', methods=['GET', 'POST'])
def cadastro_usuario():
    if request.method == 'POST':
        campo_email = request.form['email']
        campo_senha = request.form['senha']
        campo_confirme_sua_senha = request.form['confirme_sua_senha']

        if campo_senha == campo_confirme_sua_senha:
            try:
                new_user = auth.create_user_with_email_and_password(campo_email, campo_senha)
                auth.send_email_verification(new_user['idToken'])
                return render_template('verifica_email.html')
            except:
                conta_existe = 'Esse email já está sendo usado!'
                render_template('cadastro_usuario.html', mensagem_existe=conta_existe)

    return render_template('cadastro_usuario.html')

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