from flask import Flask,redirect,flash,url_for
from flask import render_template
from forms import RegistrationForm, LoginForm

app = Flask(__name__, template_folder='templates')

app.config['SECRET_KEY'] = '65ed7f070f0943200fa33cdb18faf156'

example_event = [
    {
        'eventName': 'Joker',
        'eventDate': '20.10.2019',
        'eventPlace': 'Cinemaximum',
        'eventType': 'Movie'
    },
    {
        'eventName': 'Batman',
        'eventDate': '20.11.2029',
        'eventPlace': 'Cinepink',
        'eventType': 'Movie'
    }
]

@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html', events= example_event)


@app.route("/about")
def about_page():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])

def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        return redirect(url_for('home_page'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])

def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == "__main__":
    app.run()
