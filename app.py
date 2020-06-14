from flask import Flask, render_template, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow 
from send_mail import send_mail
import os
import requests
import json

app = Flask(__name__)

ENV = 'dev'
WEBHOOK_URL = os.getenv('SLACK_WEBHOOK')

if ENV == 'dev':
  app.debug = True
  app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
else:
  app.debug = False
  app.config['SQLALCHEMY_DATABASE_URI'] = '<PUT IN REMOTE DB URI FOR PROD HERE>'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) # Init Schema and Models
ma = Marshmallow(app) # Init ORM

# Product Class/Model
class Product(db.Model):
  __tablename__ = 'products'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), unique=True)
  description = db.Column(db.String(200))
  price = db.Column(db.Float)
  qty = db.Column(db.Integer)

  def __init__(self, name, description, price, qty):
    self.name = name
    self.description = description
    self.price = price
    self.qty = qty

# Product Schema
class ProductSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'description', 'price', 'qty')

# Define schema relationships
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


# Home Route
@app.route('/')
def index():
  ### SLACK MESSAGE ###
  message = {'text': "Home Page Visitor!!"}
  requests.post(WEBHOOK_URL, data=json.dumps(message))
  # Get products
  all_products = Product.query.all()
  # return array of all products
  data = products_schema.dump(all_products)
  return render_template('index.html', data=data)

# Home Route
@app.route('/about')
def about():
  ### SLACK MESSAGE ###
  message = {'text': "About Page Visitor!!"}
  requests.post(WEBHOOK_URL, data=json.dumps(message))
  return render_template('about.html')

# Home Route
@app.route('/documentation')
def documentation():
  ### SLACK MESSAGE ###
  message = {'text': "Documentation Page Visitor!!"}
  requests.post(WEBHOOK_URL, data=json.dumps(message))
  return render_template('documentation.html')


#Create a product
@app.route('/api/product', methods=['POST'])
def add_product():
  name = request.json['name']
  description = request.json['description']
  price = request.json['price']
  qty = request.json['qty']

  new_product = Product(name, description, price, qty)

  db.session.add(new_product)
  db.session.commit()

  # Slack Message
  if new_product:
    message = {'text': "New Product Added!"}
    requests.post(WEBHOOK_URL, data=json.dumps(message))

  return product_schema.jsonify(new_product)


# Get All Product
@app.route('/api/product', methods=['GET'])
def get_products():
  message = {'text': "User requesting all products!"}
  requests.post(WEBHOOK_URL, data=json.dumps(message))
  # query db for all products
  all_products = Product.query.all()
  # return array of all products
  result = products_schema.dump(all_products)
  return jsonify(result)


# Get Single Product
@app.route('/api/product/<id>', methods=['GET'])
def get_product(id):
  message = {'text': f"User requested Product {id}"}
  requests.post(WEBHOOK_URL, data=json.dumps(message))
  # query db for all products
  product = Product.query.get(id)
  return product_schema.jsonify(product)


#Create a product
@app.route('/api/product/<id>', methods=['PUT'])
def update_product(id):
  # find item we'd like to change
  product = Product.query.get(id)
  # init request variables
  name = request.json['name']
  description = request.json['description']
  price = request.json['price']
  qty = request.json['qty']
  # save new model params
  product.name = name
  product.description = description
  product.price = price
  product.qty = qty
  # commit the change
  db.session.commit()

    # Output slack channel message
  if product.name:
    message = {'text': "Updated Product!"}
    requests.post(WEBHOOK_URL, data=json.dumps(message))

  return product_schema.jsonify(product)


# Get Single Product
@app.route('/api/product/<id>', methods=['DELETE'])
def delete_product(id):
  # slack message
  message = {'text': f"User deleted Product {id}"}
  requests.post(WEBHOOK_URL, data=json.dumps(message))
  # find product to delete
  product = Product.query.get(id)
  db.session.delete(product)
  db.session.commit()

  # return the deleted object
  return product_schema.jsonify(product)

#Run Sever
if __name__ == '__main__':
  app.run(debug=True)