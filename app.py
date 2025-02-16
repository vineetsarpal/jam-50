import os
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import error
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Space, Booking
from helpers import login_required
from datetime import datetime, timedelta

app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY')

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jam.db'

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    featured_spaces = db.session.query(Space).limit(3).all()
    return render_template('index.html', featured_spaces=featured_spaces)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return error("must provide a username", 400)

        user = db.session.query(User).filter_by(username=username).first()
        if user:
            flash('Username already exists')
            return error("Username already exists", 400)
        
        new_user = User(username=username)

        if not password:
            return error("must enter a password", 400)
        if password != confirmation:
            return error("Passwords do not match", 400)
        
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()
       
        flash('Registration successful')

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        guest = request.form.get("guest")
        if guest:
            username = guest
            user = db.session.query(User).filter_by(username=username).first()
            user_id = user.id
        
        else:
            username = request.form.get("username")
            password = request.form.get("password")

            if not username:
                return error("must provide username", 403)

            # Ensure password was submitted
            elif not password:
                return error("must provide password", 403)

            # Query database for username
            user = db.session.query(User).filter_by(username=username).first()
            if not user:
                return error("invalid username", 403)

            user_id = user.id
            user_pwd = user.password_hash

            # Ensure password is correct
            if not check_password_hash(user_pwd, password):
                return error("invalid password", 403)
            

        # Remember which user has logged in
        session["user_id"] = user_id
        session["username"] = username

        # Redirect user to home page
        flash(f"Welcome, {username}")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
    

@app.route("/logout")
def logout():
    """Log user out"""
    username = session.get("username")
    if username == "guest":
        user_id = session.get("user_id")
        db.session.query(Booking).filter_by(user_id=user_id).delete()
        db.session.commit()
    session.clear()
    flash("Logged out successfully!")
    return redirect("/")    

@app.route("/spaces")
@login_required
def spaces():

    # Add a new space

    # new_space = Space(
    #     name="Garage Pad",
    #     description="A rehearasl space to practice for hours on end",
    #     capacity=6,
    #     hourly_rate=40.00,
    #     address="51 Grunge Avenue, Paddington, NY 65870",
    #     amenities="Drum kit, cymbals, guitar amps, synth, mic, soundproofing",
    #     image="/static/images/jam1.jpg"
    # )

    # db.session.add(new_space)
    # db.session.commit()

    spaces = db.session.query(Space).all()

    return render_template("spaces.html", spaces=spaces)

@app.route("/spaces/<int:space_id>")
@login_required
def space(space_id):
    space = db.session.query(Space).get(space_id)
    return render_template("space.html", space=space)

@app.route("/book", methods=["POST"])
@login_required
def book():
    user_id = session.get("user_id")
    space_id = request.form.get("space_id")
    hourly_rate = request.form.get("rate")
    start_time_str = request.form.get("bookDateTime")
    start_time = datetime.strptime(start_time_str, "%Y-%m-%dT%H:%M")
    duration_hours = int(request.form.get("duration"))

    # calculate end time by adding duration (in hours) to start time
    end_time = start_time + timedelta(hours=duration_hours)
    
    # total cost
    total_cost = float(hourly_rate) * (duration_hours)
    
    new_booking = Booking(
        user_id=user_id,
        space_id=space_id,
        start_time=start_time,
        end_time=end_time,
        total_cost=total_cost
    )

    db.session.add(new_booking)
    db.session.commit()

    flash("Booking successful!")
    return redirect("/spaces")

@app.route("/bookings")
@login_required
def bookings():
    user_id = session.get("user_id")
    bookings = db.session.query(Booking).filter_by(user_id=user_id).all()
    for booking in bookings:
        space = db.session.query(Space).get(booking.space_id)
        booking.space_name = space.name
    return render_template("bookings.html", bookings=bookings)

if __name__ == '__main__':
    app.run(debug=True)