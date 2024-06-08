from flask import Blueprint, request, jsonify
from app import mysql

users = Blueprint('users', __name__)

@users.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.json
        print("Received data:", data)
        cursor = mysql.connection.cursor()
        cursor.execute(
            'INSERT INTO users (FirstName, LastName, Password, Email) VALUES (%s, %s, %s, %s)',
            (data['FirstName'], data['LastName'], data['Password'], data['Email'])
        )
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'User created successfully!'}), 201
    except Exception as e:
        return jsonify({'message': 'Failed to create user', 'error': str(e)}), 400

@users.route('/users', methods=['GET'])
def get_users():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        cursor.close()
        return jsonify(users), 200
    except Exception as e:
        return jsonify({'message': 'Failed to retrieve users', 'error': str(e)}), 400

@users.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE UserId = %s', (user_id,))
        user = cursor.fetchone()
        cursor.close()
        if user:
            return jsonify(user), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'message': 'Failed to retrieve user', 'error': str(e)}), 400

@users.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.json
        print("Received data:", data)
        cursor = mysql.connection.cursor()
        cursor.execute(
            'UPDATE users SET FirstName = %s, LastName = %s, Password = %s, Email = %s WHERE UserId = %s',
            (data['FirstName'], data['LastName'], data['Password'], data['Email'], user_id)
        )
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'User updated successfully!'}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to update user', 'error': str(e)}), 400

@users.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM users WHERE UserId = %s', (user_id,))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'User deleted successfully!'}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to delete user', 'error': str(e)}), 400
