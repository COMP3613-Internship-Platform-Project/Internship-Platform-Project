from flask import Blueprint, jsonify, request
from flask_jwt_extended import decode_token, get_jwt_identity, jwt_required, get_jwt, unset_jwt_cookies
from App.controllers.auth import jwt_authenticate

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')

@auth_views.route('/api/login', methods=['POST'])
def login_user():
    data = request.json

    if not data or not data.get('username') or not data.get('password'):
        return jsonify(error='Username and password are required'), 400

    token = jwt_authenticate(data['username'], data['password'])
    if not token:
        return jsonify(error='Invalid credentials'), 401
    
    decoded_token = decode_token(token)
    user_id = decoded_token['sub']
    username = decoded_token.get('username')
    user_type = decoded_token.get('user_type')
    
    return jsonify(
        access_token=token,
        user_id=user_id,
        username=username,
        user_type=user_type
    ), 200

@auth_views.route('/identify', methods=['GET'])
@jwt_required()
def identify():
    try:
        claims = get_jwt()
        user_id = get_jwt_identity()  
        username = claims.get('username')  
        user_type = claims.get('user_type', 'unknown') 
        
        return jsonify({
            'user_id': user_id,
            'username': username,
            'user_type': user_type,
            'message': f'Logged in as {username} ({user_type})'
        }), 200
    except Exception as e:
        return jsonify(error='Unable to identify user'), 401
    
@auth_views.route('/api/logout', methods=['GET'])
def logout():
    response = jsonify({"message": "Logged out successfully"})
    unset_jwt_cookies(response)
    return response