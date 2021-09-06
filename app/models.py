from app import db
from flask_login import UserMixin
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash
from app import login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(75))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    created_on = db.Column(db.DateTime, default=dt.utcnow)

    def __repr__(self):
        return f'<User: {self.id} | {self.email} >'

    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = self.hash_password(data['password'])
        self.save()

    def hash_password(self, original_password):
        return generate_password_hash(original_password)

    def check_hashed_password(self, login_password):
        return check_password_hash(self.password,login_password)

    def save(self):
        db.session.add(self)
        db.session.commit()

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Product(db.Model):
    id = db.Column (db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    price = db.Column(db.Float(75))
    description = db.Column(db.String(100))
    category_id = db.Column(db.Integer)
    image_url = db.Column(db.String(250))
    
    def __repr__(self):
        return f'<Product: {self.id} >'

    def from_dict(self, data):
        self.name = data['name']
        self.price = data['price']
        self.description = data['description']
        self.category = data['category']
        self.image_url = data ['image_url']
        self.save()

class Cart (db.Model):
    cart_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, db.ForeignKey('product.name'))
    price = db.Column(db.Float, db.ForeignKey('product.price'))

    def __repr__(self):
        return f'<Cart: {self.cart_id} >'


# class Category(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(200))

#     def __repr__(self):
#         return f'<Category: {self.id} | {self.name}>'

#     def save(self):
#         db.session.add(self)
#         db.session.commit()
    
#     def delete(self):
#         db.session.delete(self)
#         db.session.commit()

#     def to_dict(self):
#         data={
#             "id":self.id,
#             "name":self.name
#         }
#         return data