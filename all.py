from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLalchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///factory.db' # Use your database URI
db.SQLAlchemy(app)

# Models
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'quantity': self.quantity
        }

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db. Float, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price
        }
    
# Route
@app.route('/orders', methods=['GET'])
def get_orders():
    page = request.args.get('page', 1, type=int) # Defualt page is 1
    per_page = request.args.get('per_page', 10, type=int) # Defualt per_page is 10


    orders = Order.query.paginate(page=page, per_page=per_page, error_out=False)

    if not orders.items:
        return jsonify({'message': 'No orders found for this page'}), 404
    
    return jsonify({
        'orders': [order.to_dict() for order in orders.items],
        'total_orders': orders.total,
        'total_pages': orders.pages,
        'current_page': orders.page
    })

@app.route('/products', methods=['GET'])
def get_products():
    page = request.args.get('page', 1, type=int) # Defualt page is 1
    per_page = request.args.get('per_page', 10, type=int) # Default per_page is 10

    products = Product.query.paginate(page=page, per_page=per_page, error_out=False)

    if not products.items:
        return jsonify({'message': 'No products found for this page'}), 404
    

    return jsonify({
        'products': [product.to_dict() for product in products.items],
        'total_products': products.total,
        'total_pages': products.pages,
        'current_page': products.page
    })

# Create database and tables
@app.before_first_request
def create_tables():
    db.create_all()

# Run the application 
if __name__ == '__main__':
    app.run(debug=True)
    
