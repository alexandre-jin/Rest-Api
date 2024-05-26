from flask import Blueprint, request, jsonify
from app import mysql

products = Blueprint('products', __name__)

@products.route('/products', methods=['POST'])
def create_product():
    data = request.json
    cursor = mysql.connection.cursor()
    cursor.execute(
        'INSERT INTO products (NameProduct, TypeProduct, DescriptionProduct, Price, StatusProduct) VALUES (%s, %s, %s, %s, %s)',
        (data['NameProduct'], data['TypeProduct'], data['DescriptionProduct'], data['Price'], data['StatusProduct'])
    )
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'Product created successfully!'}), 201

@products.route('/products', methods=['GET'])
def get_products():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    cursor.close()
    return jsonify(products)

@products.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM products WHERE ProductId = %s', (product_id,))
    product = cursor.fetchone()
    cursor.close()
    return jsonify(product)

@products.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.json
    cursor = mysql.connection.cursor()
    cursor.execute(
        'UPDATE products SET NameProduct = %s, TypeProduct = %s, DescriptionProduct = %s, Price = %s, StatusProduct = %s WHERE ProductId = %s',
        (data['NameProduct'], data['TypeProduct'], data['DescriptionProduct'], data['Price'], data['StatusProduct'], product_id)
    )
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'Product updated successfully!'})

@products.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM products WHERE ProductId = %s', (product_id,))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'Product deleted successfully!'})
