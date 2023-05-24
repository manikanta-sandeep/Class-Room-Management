from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabom.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db = SQLAlchemy(app)
app.app_context().push()


class roles(db.Model):
    __tablename__="roles"
    role_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name=db.Column(db.String, unique=True)
    last_update=db.Column(db.String)

    
class country(db.Model):
    __tablename__="country"
    country_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    country=db.Column(db.String, unique=True)
    last_update=db.Column(db.String)


class state(db.Model):
    __tablename__="state"
    state_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    state=db.Column(db.String, unique=True)
    country_id=db.Column(db.Integer, ForeignKey("country.country_id"))
    last_update=db.Column(db.String)


class city(db.Model):
    __tablename__="city"
    city_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    city=db.Column(db.String, unique=True)
    state_id=db.Column(db.Integer, ForeignKey("state.state_id"))
    last_update=db.Column(db.String)

class address(db.Model):
    __tablename__="address"
    address_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    address=db.Column(db.String)
    address2=db.Column(db.String)
    district=db.Column(db.String)
    city_id=db.Column(db.Integer,  ForeignKey("city.city_id"))
    postal_code=db.Column(db.String)
    phone=db.Column(db.Integer)
    last_update=db.Column(db.String)

class user(db.Model):
    __tablename__="user"
    user_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    email=db.Column(db.String, unique=True)
    name=db.Column(db.String)
    dob=db.Column(db.String)
    gender=db.Column(db.Integer)
    aadhar=db.Column(db.Integer)
    password=db.Column(db.String)
    phone=db.Column(db.Integer)
    profile_description=db.Column(db.String)
    address_id=db.Column(db.Integer, ForeignKey("address.address_id"))
    profile_picture=db.Column(db.LargeBinary,default=None)
    created_time=db.Column(db.String)
    last_update=db.Column(db.String)
    role=db.Column(db.Integer, ForeignKey("roles.role_id"))




class item_type(db.Model):
    __tablename__="item_type"
    item_type_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_name=db.Column(db.String)

class immediate_type(db.Model):
    __tablename__="immediate_type"
    immediate_type_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_name=db.Column(db.String)

class units(db.Model):
    __tablename__="units"
    unit_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    unit_name=db.Column(db.String)

class discount(db.Model):
    __tablename__="discount"
    discount_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    discount_details=db.Column(db.String)
    discount_amount=db.Column(db.Float)
    last_update=db.Column(db.String)

class status(db.Model):
    __tablename__="status"
    status_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    status_name=db.Column(db.String)
    description=db.Column(db.String)
    last_update=db.Column(db.String)




class chat(db.Model):
    __tablename__="chat"
    message_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_id=db.Column(db.Integer, ForeignKey("user.user_id"))
    reveiver_id=db.Column(db.Integer, ForeignKey("user.user_id"))
    message=db.Column(db.String)
    send_time=db.Column(db.String)
    seen=db.Column(db.Integer)
    last_update=db.Column(db.String)

class comments(db.Model):
    __tablename__="comments"
    comment_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    inventory_id=db.Column(db.Integer, ForeignKey("inventory.inventory_id"))
    user_id=db.Column(db.Integer, ForeignKey("user.user_id"))
    comment=db.Column(db.String)
    commented_time=db.Column(db.String)
    last_updated=db.Column(db.String)

class rating_type(db.Model):
    __tablename__="rating_type"
    rating_type_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    rating_on=db.Column(db.String)
    description=db.Column(db.String)


class rating(db.Model):
    __tablename__="rating"
    rating_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    rating_on=db.Column(db.Integer, ForeignKey("rating_type.rating_type_id"))
    rating=db.Column(db.Float)
    feedback=db.Column(db.String)
    last_update=db.Column(db.String)


class item(db.Model):
    __tablename__="item"
    item_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_name=db.Column(db.String)
    item_type_id=db.Column(db.Integer, ForeignKey("item_type.item_type_id"))
    item_category=db.Column(db.String)
    description=db.Column(db.String)
    joined_time=db.Column(db.String)
    last_update=db.Column(db.String)
    immediate=db.Column(db.Integer, ForeignKey("immediate_type.immediate_type_id"))


class requirement(db.Model):
    __tablename__="requirement"
    requirement_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id=db.Column(db.Integer, ForeignKey("user.user_id"))
    item_id=db.Column(db.Integer, ForeignKey("item.item_id"))
    quantity_required=db.Column(db.Float)
    measured_in=db.Column(db.Integer, ForeignKey("units.unit_id"))
    min_price=db.Column(db.Integer)
    max_price=db.Column(db.Integer)
    status=db.Column(db.Integer, ForeignKey("status.status_id"))
    address=db.Column(db.Integer)
    description=db.Column(db.String)
    time_posted=db.Column(db.String)
    last_updated=db.Column(db.String)
    discount=db.Column(db.Integer, ForeignKey("user.user_id"))


class inventory(db.Model):
    __tablename__="inventory"
    inventory_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id=db.Column(db.Integer, ForeignKey("user.user_id"))
    item_id=db.Column(db.Integer, ForeignKey("item.item_id"))
    price_per_unit=db.Column(db.Float)
    address=db.Column(db.Integer)
    due=db.Column(db.Integer)
    picture=db.Column(db.LargeBinary,default=None)
    description=db.Column(db.String)
    joined_time=db.Column(db.String)
    last_updated=db.Column(db.String)
    view=db.Column(db.Integer)
    measured_in=db.Column(db.Integer, ForeignKey("units.unit_id"))
    quantity_added=db.Column(db.Integer)
    quanity_sold=db.Column(db.Integer)
    quantity_remaining=db.Column(db.Integer)
    quantity_last_updated=db.Column(db.String)


class cart(db.Model):
    __tablename__="cart"
    cart_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_id=db.Column(db.Integer, ForeignKey("item.item_id"))
    user_id=db.Column(db.Integer, ForeignKey("user.user_id"))
    description=db.Column(db.String)
    send_time=db.Column(db.String)
    last_update=db.Column(db.String)



class order(db.Model):
    __tablename__="order"
    order_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id=db.Column(db.Integer, ForeignKey("user.user_id"))
    inventory_id=db.Column(db.Integer, ForeignKey("inventory.inventory_id"))
    quantity_required=db.Column(db.Float)
    status=db.Column(db.Integer, ForeignKey("status.status_id"))
    delivery_charges=db.Column(db.Float)
    description=db.Column(db.String)
    ordered_time=db.Column(db.String)
    last_updated=db.Column(db.String)
    discount=db.Column(db.Integer, ForeignKey("discount.discount_id"))

class payment(db.Model):
    __tablename__="payment"
    payment_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id=db.Column(db.Integer, ForeignKey("user.user_id"))
    order_id=db.Column(db.Integer, ForeignKey("order.order_id"))
    amount=db.Column(db.Float)
    status=db.Column(db.Integer, ForeignKey("status.status_id"))
    payment_date=db.Column(db.Integer)
    last_update=db.Column(db.String)

