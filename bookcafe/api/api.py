from flask import Blueprint,request,render_template,flash,url_for,redirect,jsonify,json
from bookcafe.model.books import Book
from bookcafe.model.categories import Category
from werkzeug.security import generate_password_hash, check_password_hash
from bookcafe.model.users import User,UserSchema
from flask_login import login_user, logout_user,current_user,login_required
from ..extentions import db



api = Blueprint('api', __name__)

@api.route("/user", methods=['GET','POST'])
def get_users():
    if request.method == 'GET':
        users =[]
        content ={}
        all_user = User.query.all()
        for user in all_user:
            content = {
                'id':user.id,'username':user.username,'email':user.email,'category':user.category,'password':user.password
            }            
            users.append(content)
        return jsonify({"Users":users})
    if request.method == 'POST':
        users =[]
        content ={}
        username = request.json['username']
        email = request.json['email']
        category = request.json['category']
        password1 = request.json['password1']
        password2 = request.json['password2']
        user = User.query.filter_by(email=email).first()
        user_name = User.query.filter_by(username=username).first()
        if user_name:
            return {"Error":"Username Taken please try something else"}
        elif user:
            return {"Error":"Email Already exist"}
        elif len(email) < 4:
            return {"Error":"Please Use A valid email"}  
        elif len(password1) < 4:
            return {"Error":"Password must be greater than 4 character"} 
        elif password1!=password2:
            return {"Error":"Password do nor match"}   
        else:
            password= generate_password_hash(password1, method='sha256')
            user = User(username = username, email = email,category = category, password = password)
            db.session.add(user)
            db.session.commit()
            content = {
                'id':user.id,'username':user.username,'email':user.email,'category':user.category,
                'password':user.password , 'created_at':user.created_at
                }            
            users.append(content)
            return jsonify({"Users":users})

@api.route('/user/<string:id>', methods= ['GET','PUT','DELETE'] )
def user(id):
    user = User.query.get_or_404(str(id))
    usr = []
    content={}
    if request.method == 'GET':
        
        content = {
                'id':user.id,'username':user.username,'email':user.email,'category':user.category,'password':user.password
            }            
        usr.append(content)
        return jsonify({"user":usr})
    if request.method == 'PUT':
        username = request.json['username']
        email = request.json['email']
        category = request.json['category']
        password1 = request.json['password1']
        password2 = request.json['password2']
        user = User.query.filter_by(email=email).first()
        # username = User.query.filter_by(username=username).first()
        # if username:
        #     return {"Error":"Username Taken please try something else"}
        # if user:
        #     return {"Error":"Email Already exist"}
        # elif len(email) < 4:
        #     return {"Error":"Please Use A valid email"}  
        # elif len(password1) < 4:
        #     return {"Error":"Password must be greater than 4 character"} 
        if password1!=password2:
             return {"Error":"Password do nor match"}   
        else:
            password= generate_password_hash(password1, method='sha256')
            user.username = username
            user.email = email
            user.category = category
            user.password = password
            user = User(username = username, email = email,category = category, password = password)
            db.session.commit()

            content = {
                'id':user.id,'username':user.username,'email':user.email,'category':user.category,'password':user.password
                }            
            usr.append(content)
            return jsonify({"Users":usr})
    if request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({}), 200
    
@api.route("/create", methods=['GET','POST'])
def create_book():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        category = request.form.get('category')
        description = request.form.get('description')
        new_book = Book( title = title, author = author, category = category, description= description)
        db.session.add(new_book)
        db.session.commit()
        flash('added successfull', category='success')
        return redirect(url_for('view.books',user=current_user))
    if request.method == "GET":
        return render_template("addbooks.html",user=current_user)
    

    
@api.route("/book", methods=['GET','POST'])
def get_books():
    book = []
    content={}
    if request.method == 'POST':        
        title = request.json['title']
        author = request.json['author']
        category = request.json['category_id']
        description = request.json['description']
        new_book = Book(title = title, author = author, category_id = category, description= description)
        db.session.add(new_book)
        db.session.commit()
        content = {
                'id':new_book.id,'title':new_book.title,'author':new_book.author,'category':new_book.category,'description':new_book.description
            }            
        book.append(content)
        return jsonify({"Book":book})
    if request.method == 'GET': 

        all_book = Book.query.all()
        if len(all_book) < 1:
            return jsonify({"Error":"No record found"})

        for books in all_book:
            content = {
                'id':books.id,'title':books.title,'author':books.author,'category':books.category_id,'description':books.description
            }            
            book.append(content)
        return jsonify({"Books":book})

@api.route("/book/<string:id>", methods= ['GET','DELETE','PUT'])
def book(id):
    book = []
    content={}
    if request.method == 'GET': 
        new_book = Book.query.get_or_404(str(id))
        content = {
                'id':new_book.id,'title':new_book.title,'author':new_book.author,
                'category':new_book.category,'description':new_book.description,'created_at':new_book.created_at,
            }            
        book.append(content)
        return jsonify({"Book":book})
    if request.method == 'PUT':
        update_book = Book.query.get_or_404(str(id))
        title = request.json['title']
        author = request.json['author']
        category = request.json['category_id']
        description = request.json['description']
        update_book.title = title
        update_book.author = author
        update_book.category = category
        update_book.description = description
        db.session.commit()
        content = {
                'id':update_book.id,'title':update_book.title,'author':update_book.author,
                'category':update_book.category_id,'description':update_book.description,'created_at':update_book.created_at
            }            
        book.append(content)
        return jsonify({"Book":book})
        return "Updated successfully!!"
    if request.method == 'DELETE':
        book = Book.query.get_or_404(str(id))
        db.session.delete(book)
        db.session.commit()
        
        return jsonify({}), 200

@api.route("/categories", methods=['GET','POST'])
def add_category():
    categories = []
    content = {}
    if request.method == 'POST': 
        category = request.json['category']
        new_category = Category(category=category)
        db.session.add(new_category)
        db.session.commit()
        content = {
                'id':new_category.id,'category':new_category.category
            }            
        categories.append(content)
        return jsonify({"Categories":categories})
    if request.method == 'GET':
        all_category = Category.query.all()
        for category in all_category:
            content = {
                    'id':category.id,'category':category.category
                }            
            categories.append(content)
        return jsonify({"Categories":categories})


@api.route("/categories/<string:id>", methods=['GET','PUT','DELETE'])
def category(id):
    categories=[]
    content={}
    if request.method == 'GET': 
        category = Category.query.get_or_404(str(id))
        content = {
                'id':category.id,'category':category.category
            }            
        categories.append(content)
        return jsonify(categories)

    if request.method == 'PUT':
        cat = Category.query.get_or_404(str(id))
        category = request.json['category']
        db.session.commit()
        content = {
                'id':cat.id,'category':cat.category
            }            
        categories.append(content)
        return jsonify({"Category":categories})

    if request.method == 'DELETE':
        category = Category.query.get_or_404(str(id))
        db.session.delete(category)
        db.session.commit()
        return jsonify({})
