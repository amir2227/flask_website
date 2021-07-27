from flask import Flask, render_template, url_for, flash
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = "falhdfuo@!^(*#khjSA98713dnK&(#@FDJF83R3"

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@invskills.com' and form.password.data == 'admin':
            flash('you loged in successfully', 'success')
            return render_template(url_for('dashbord'))
        else:
            flash('Unsuccessful login. Please check Email and Password.', 'danger')
    return render_template('login.html', title='Login', form=form)

if __name__ == "__main__":
    app.run(debug=True)