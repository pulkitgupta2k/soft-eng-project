from flask import Flask, render_template, request, url_for, redirect, flash, \
session, abort
from flask_sqlalchemy import sqlalchemy, SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from iot import netcat

# Change dbname here
db_name = "auth.db"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{db}'.format(db=db_name)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# SECRET_KEY required for session, flash and Flask Sqlalchemy to work
app.config['SECRET_KEY'] = 'configure strong secret key here'

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    pass_hash = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return '' % self.username

class Device(db.Model):
    __tablename__ = 'device'
    did = db.Column(db.Integer, primary_key=True)
    dev_name = db.Column(db.String(100), unique=True, nullable=False)
    dev_ip = db.Column(db.String(100), nullable=False)
    username = db.Column(db.Integer, db.ForeignKey('user.username'))


def create_db():
    """ # Execute this first time to create new db in current directory. """
    db.create_all()


@app.route("/signup/", methods=["GET", "POST"])
def signup():
    """
    Implements signup functionality. Allows username and password for new user.
    Hashes password with salt using werkzeug.security.
    Stores username and hashed password inside database.
    Username should to be unique else raises sqlalchemy.exc.IntegrityError.
    """

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        if not (username and password):
            flash("Username or Password cannot be empty")
            return redirect(url_for('signup'))
        else:
            username = username.strip()
            password = password.strip()
            email = email.strip()

        # Returns salted pwd hash in format : method$salt$hashedvalue
        hashed_pwd = generate_password_hash(password, 'sha256')

        new_user = User(username=username, pass_hash=hashed_pwd, email=email)
        db.session.add(new_user)

        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            flash("Username {u} is not available.".format(u=username))
            return redirect(url_for('signup'))

        flash("User account has been created.")
        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/login/", methods=["GET", "POST"])
def login():
    """
    Provides login functionality by rendering login form on get request.
    On post checks password hash from db for given input username and password.
    If hash matches redirects authorized user to home page else redirect to
    login page with error message.
    """

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if not (username and password):
            flash("Username or Password cannot be empty.")
            return redirect(url_for('login'))
        else:
            username = username.strip()
            password = password.strip()

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.pass_hash, password):
            session[username] = True
            return redirect(url_for("user_home", username=username))
        else:
            flash("Invalid username or password.")

    return render_template("login_form.html")


@app.route("/add_device/<username>/", methods=["POST"])
def add_device(username):
    if request.method == "POST":
        dev_name = request.form['dev_name'].strip()
        dev_ip = request.form['dev_ip'].strip()
        new_device = Device(username=username, dev_name=dev_name, dev_ip=dev_ip)
        db.session.add(new_device)
        db.session.commit()
        flash("Device has been added")
    
    return redirect(url_for('user_home', username=username))

@app.route("/user/<username>/")
def user_home(username):
    """
    Home page for validated users.
    """
    if not session.get(username):
        abort(401)
    devices = Device.query.filter_by(username=username).all()
    devs = list()
    for device in devices:
        dev = []
        dev.append(device.dev_name)
        dev.append(device.dev_ip)
        devs.append(dev)
    return render_template("user_home.html", username=username, devs = devs)

@app.route("/user/<username>/<dev_name>/<action>")
def action(username, dev_name, action):
    device = Device.query.filter_by(username=username, dev_name= dev_name).first()
    netcat(device.dev_ip, 4444, action)
    return redirect(url_for('user_home', username=username))


@app.route("/logout/<username>")
def logout(username):
    """ Logout user and redirect to login page with success message."""
    session.pop(username, None)
    flash("successfully logged out.")
    return redirect(url_for('login'))


if __name__ == "__main__":
    # create_db()
    app.run(port=5000, debug=True)