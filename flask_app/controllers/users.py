from flask import Flask, render_template, request, session, redirect, flash
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


# Home page - Register
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')

# Login user confirm


@app.route('/login/user', methods=['POST'])
def login_user():
    from flask_app.models.user import User
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid email or password", "login")
        return render_template('login.html')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid password", "login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/register/user', methods=['POST'])
def register_user():
    from flask_app.models.user import User
    if not User.validate_reg(request.form):
        return render_template('register.html')
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id
    return redirect('/')


@app.route('/user')
def user():
    return render_template('login.html')


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
