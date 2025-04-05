from flask import Flask, request, jsonify, send_from_directory
import sqlite3
from flask_cors import CORS
import os

app = Flask(__name__, static_url_path='', static_folder='.')
CORS(app)

# Database connection helper
def get_db_connection():
    conn = sqlite3.connect('floretworld.db')
    conn.row_factory = sqlite3.Row
    return conn

# Register route
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'status': 'fail', 'message': 'Missing email or password'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, password))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success', 'message': 'User registered successfully'})
    except sqlite3.IntegrityError:
        return jsonify({'status': 'fail', 'message': 'Email already exists'}), 409
    except Exception as e:
        return jsonify({'status': 'fail', 'message': str(e)}), 500

# Login route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({'status': 'success', 'message': 'Login successful'})
    else:
        return jsonify({'status': 'fail', 'message': 'Invalid email or password'}), 401

# Serve HTML files
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    app.run(debug=True)
