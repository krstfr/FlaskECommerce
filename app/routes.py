from flask import render_template, request, redirect, url_for, session
import requests
from app import app
from .forms import LoginForm, RegisterForm, ProductForm, CartForm
from .models import User, Product, Cart
from flask_login import login_user, logout_user, current_user, login_required


@app.route('/')
@login_required
def home():
    return render_template("home.html.j2")

@app.route('/product', methods=['GET', 'POST'])
@login_required
def product():
    if request.method == 'POST':
        cart = request.form.get('name')
        data = ProductForm
        response = request.get(ProductForm)

        if response.ok:
            data = response.data('name','price')
            if not data:
                error_string=f"Seems like we're either out of stock or don't have it"
                return render_template ("product.html.j2", error=error_string)
            data = ProductForm
            cart_items = []
            for product in data:
                product_dict={
                    'name': product['name'],
                    'price': product['price'],
                    'description': product['description'],
                    'image_url': product['image_url']
                }
                cart_items.append(product_dict)
            return render_template("product.html.j2", product=cart_items)
    else: 
        error_string="Hold On. Something's Off"
        products = Product.query.all()
        return render_template("product.html.j2", products=products, error=error_string)
    return render_template("product.html.j2")

@app.route('/cart', methods=['GET'])
@login_required
def view_cart():
    form = CartForm()
    return render_template("cart.html.j2", form = form)
    


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    if current_user is not None:
        logout_user()
        return redirect(url_for('login'))


@app.route('/contact_us')
def contact():
    return render_template("contact.html.j2")

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        # try:
        new_user_data={
            "first_name": form.first_name.data.title(),
            "last_name": form.last_name.data.title(),
            "email": form.email.data.lower(),
            "password": form.password.data
        }
        new_user_object = User ()
        new_user_object.from_dict(new_user_data)
        # except:
            # error_string = "There's an issue getting you into the shop. Try creating your account again"
            # return render_template('register.html.j2',form=form, error=error_string)
        return redirect(url_for('login'))

    return render_template('register.html.j2', form=form )
        

@app.route('/login',methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST'and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        u = User.query.filter_by(email=email).first()
        print (u)
        if u is not None and u.check_hashed_password(password):
            login_user(u)
            #feedback
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))
    return render_template("login.html.j2", form=form)

# @app.route('/addcart', methods=['POST'])
# @login_required
# def add_cart():
#     try:
#         product_id = request.form.get('id')
#         product = Product.quert.filter_by(id=product_id).first()

#         if product_id and product and request.method == 'POST':
#             DictItems = {product_id:{'name': product.name, 'price': product.price, 'image': product.image_url}}

#             if 'view_cart' in session:
#                 print(session['view_cart'])

#                 if product_id in session['view_cart']:
#                     print("This item is already in your cart")
                
#                 else:
#                     return redirect(request.referrer)
#             else:
#                 session['cart'] = DictItems
#                 return redirect(request.referrer)
    
#     except:
#         pass
