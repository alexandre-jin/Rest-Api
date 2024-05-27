from flask import Blueprint, request, jsonify
from app import mysql

products = Blueprint('products', __name__)

@products.route('/products', methods=['POST'])
def create_product():
    try:
        data = request.json
        cursor = mysql.connection.cursor()
        cursor.execute(
            'INSERT INTO products (NameProduct, TypeProduct, DescriptionProduct, Price, StatusProduct, Image) VALUES (%s, %s, %s, %s, %s, %s)',
            (data['NameProduct'], data['TypeProduct'], data['DescriptionProduct'], data['Price'], data['StatusProduct'], data['Image'])
        )
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Product created successfully!'}), 201
    except Exception as e:
        return jsonify({'message': 'Failed to create product', 'error': str(e)}), 400


@products.route('/products', methods=['GET'])
def get_products():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM products')
        products = cursor.fetchall()
        cursor.close()
        return jsonify(products), 200
    except Exception as e:
        return jsonify({'message': 'Failed to retrieve products', 'error': str(e)}), 400

@products.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM products WHERE ProductId = %s', (product_id,))
        product = cursor.fetchone()
        cursor.close()
        if product:
            return jsonify(product), 200
        else:
            return jsonify({'message': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'message': 'Failed to retrieve product', 'error': str(e)}), 400


@products.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    try:
        data = request.json
        cursor = mysql.connection.cursor()
        cursor.execute(
            'UPDATE products SET NameProduct = %s, TypeProduct = %s, DescriptionProduct = %s, Price = %s, StatusProduct = %s, Image = %s WHERE ProductId = %s',
            (data['NameProduct'], data['TypeProduct'], data['DescriptionProduct'], data['Price'], data['StatusProduct'], data['Image'], product_id)
        )
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Product updated successfully!'}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to update product', 'error': str(e)}), 400


@products.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM products WHERE ProductId = %s', (product_id,))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Product deleted successfully!'}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to delete product', 'error': str(e)}), 400
