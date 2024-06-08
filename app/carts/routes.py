from flask import Blueprint, request, jsonify
from app import mysql

carts = Blueprint('carts', __name__)

@carts.route('/carts/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''
            SELECT ci.CartId, ci.ProductId, ci.Quantity, p.NameProduct, p.Price 
            FROM cart_items ci
            JOIN products p ON ci.ProductId = p.ProductId
            WHERE ci.CartId = (SELECT CartId FROM carts WHERE UserId = %s)
        ''', (user_id,))
        cart_items = cursor.fetchall()
        cursor.close()
        
        items = []
        for item in cart_items:
            items.append({
                'CartId': item['CartId'],
                'ProductId': item['ProductId'],
                'Quantity': item['Quantity'],
                'NameProduct': item['NameProduct'],
                'Price': item['Price']
            })
        
        return jsonify(items), 200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({'message': 'Failed to retrieve cart items', 'error': str(e)}), 400


@carts.route('/carts/<int:user_id>/add', methods=['POST'])
def add_to_cart(user_id):
    try:
        data = request.get_json()
        print("Received data:", data)  # Debug

        if not data:
            raise ValueError("No data provided")

        product_id = data.get('product_id')
        quantity = data.get('quantity')

        if product_id is None or quantity is None:
            raise ValueError("Missing product_id or quantity")

        if not isinstance(product_id, int):
            raise ValueError(f"product_id must be an integer, got {type(product_id).__name__}")
        if not isinstance(quantity, int):
            raise ValueError(f"quantity must be an integer, got {type(quantity).__name__}")

        cursor = mysql.connection.cursor()

        cursor.execute('SELECT CartId FROM carts WHERE UserId = %s', (user_id,))
        cart_id = cursor.fetchone()
        print("Cart ID fetched:", cart_id) 

        if not cart_id:

            cursor.execute('INSERT INTO carts (UserId) VALUES (%s)', (user_id,))
            mysql.connection.commit()
            cart_id = cursor.lastrowid
            print("New cart created with ID:", cart_id) 
        else:
            cart_id = cart_id['CartId'] 
            print("Existing cart ID:", cart_id) 

        cursor.execute('SELECT Quantity FROM cart_items WHERE CartId = %s AND ProductId = %s', (cart_id, product_id))
        existing_item = cursor.fetchone()
        print("Existing item fetched:", existing_item)  

        if existing_item:

            new_quantity = existing_item['Quantity'] + quantity
            cursor.execute('UPDATE cart_items SET Quantity = %s WHERE CartId = %s AND ProductId = %s', (new_quantity, cart_id, product_id))
            print("Updated item quantity:", new_quantity) 
        else:
            
            cursor.execute('INSERT INTO cart_items (CartId, ProductId, Quantity) VALUES (%s, %s, %s)', (cart_id, product_id, quantity))
            print("Inserted new item into cart")

        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Product added to cart'}), 201
    except Exception as e:
        print("Error occurred:", str(e))  
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
