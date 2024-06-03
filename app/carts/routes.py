from flask import Blueprint, request, jsonify
from app import mysql

carts = Blueprint('carts', __name__)

@carts.route('/carts/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM cart_items WHERE CartId = (SELECT CartId FROM carts WHERE UserId = %s)', (user_id,))
        cart_items = cursor.fetchall()
        cursor.close()
        return jsonify(cart_items), 200
    except Exception as e:
        return jsonify({'message': 'Failed to retrieve cart', 'error': str(e)}), 400

@carts.route('/carts/<int:user_id>/add', methods=['POST'])
def add_to_cart(user_id):
    try:
        data = request.json
        product_id = data['product_id']
        quantity = data['quantity']

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT CartId FROM carts WHERE UserId = %s', (user_id,))
        cart_id = cursor.fetchone()

        if not cart_id:
            cursor.execute('INSERT INTO carts (UserId) VALUES (%s)', (user_id,))
            mysql.connection.commit()
            cart_id = cursor.lastrowid
        else:
            cart_id = cart_id[0]

        cursor.execute(
            'INSERT INTO cart_items (CartId, ProductId, Quantity) VALUES (%s, %s, %s)',
            (cart_id, product_id, quantity)
        )
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Product added to cart'}), 201
    except Exception as e:
        return jsonify({'message': 'Failed to add product to cart', 'error': str(e)}), 400

@carts.route('/carts/<int:user_id>/remove', methods=['DELETE'])
def remove_from_cart(user_id):
    try:
        data = request.json
        product_id = data['product_id']

        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM cart_items WHERE CartId = (SELECT CartId FROM carts WHERE UserId = %s) AND ProductId = %s', (user_id, product_id))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Product removed from cart'}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to remove product from cart', 'error': str(e)}), 400
