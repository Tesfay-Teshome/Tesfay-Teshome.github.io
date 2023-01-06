from flask import Blueprint,request,redirect,url_for,flash,render_template
from ..extentions import db
from flask_login import login_user, logout_user,current_user,login_required
from werkzeug.security import generate_password_hash, check_password_hash
from bookcafe.model.users import User
from bookcafe.model.categories import Category

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET','POST'])
def login():
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user :
            if check_password_hash(user.password, password):
                flash('Loged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('view.books'))
            else:
                flash('Incorect Password pleas  try again!', category='error')
        else:
            flash('Email does not exist!', category='error')

    return render_template("login.html", user = current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign_up', methods=['GET','POST'])
def sign_up():
    email = request.form.get('email')
    favorite_category = Category.query.all()
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        category = request.form.getlist('fav')
        favorite = ','.join(category)
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exist', category='error')
        elif len(email) < 4:
            flash('Please enter a working email', category='error')    
        elif password1!=password2:
            flash('Passwords must match', category='error')
          
        elif len(password1) < 4:
            flash('Password must above 7 characters', category='error')
          
        else:
            new_user = User( username = username, email = email, category=favorite, password= generate_password_hash(password1, method='sha256'))

            db.session.add(new_user)
            db.session.commit()
            # login_user(user, remember=True)
            flash('Successfully Registered', category='success')
            return redirect(url_for('view.books'))
            
    return render_template("sign_up.html", user=current_user, favorite_category=favorite_category)
