"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask_debugtoolbar import DebugToolbarExtension

from flask import Flask, render_template, redirect, request, flash, session

from model import User, Rating, Movie, connect_to_db, db

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")



@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)



@app.route("/register", methods=["GET"])
def register_form():
    """ """

    return render_template("register_form.html")



@app.route("/register", methods=["POST"])
def register_process():
    """Handle processing the registration form."""
    registration_email = request.form['email']
    registration_pass = request.form['password']

    user = User.query.filter_by(email=registration_email).first()
    
    if user:
        print("There is an account associated with this email address! Please Login!")
    else:
        new_user = User(email=registration_email, password=registration_pass)

        db.session.add(new_user)
        db.session.commit()



    return redirect("/")



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
