from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = "falhdfuo@!^(*#khjSA98713dnK&(#@FDJF83R3"

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)

if __name__ == "__main__":
    app.run(debug=True)