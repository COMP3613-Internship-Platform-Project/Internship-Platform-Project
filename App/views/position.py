from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required, current_user
from App.controllers import create_position, close_position, reopen_position, list_positions_by_employer
from App.models import Position

position_views = Blueprint('position_views', __name__, template_folder='../templates')

# for creating a position 
@position_views.route('/api/positions', methods = ['POST'])
@jwt_required()
def create_position_route():
    authenticated_employer_id = get_jwt_identity()
    if not authenticated_employer_id:
        return jsonify({"error": "Access Denied - Employer authorization required"}), 401
    
    data = request.json
    try:
        employer_id = authenticated_employer_id
        title=data['title']
        number_of_positions=int(data['number'])
    except KeyError as e:
        return jsonify({"error": "title and number of positions are required"}), 400

    duplicate_position = Position.query.filter_by(employer_id=employer_id, title=title).first()
    if duplicate_position:
        return jsonify({"error": "Duplicate Position: You cannot create an internship position with the same title"}), 500
    
    try:
        position = create_position(employer_id, title, number_of_positions)
    except:
        return jsonify({"error": "Failed to create position"}), 400
    
    return jsonify({"message": "Position Created", 
                    "position_id": f"{position.id}",
                    "employer_id": f"{position.employer_id}"
                    }), 200

@position_views.route('/api/positions/<position_id>/close', methods=['POST'])
@jwt_required()
def close_position_route(position_id):
    authenticated_employer_id = get_jwt_identity()
    if not authenticated_employer_id:
        return jsonify({"error": "Access Denied - Employer authorization required"}), 401
    
    position = Position.query.filter_by(id=position_id, employer_id=authenticated_employer_id).first()
    if not position:
        return jsonify({"error": "Position not found or access denied"}), 404
    
    if position.status == 'closed':
        return jsonify({"error": "Position is already closed"}), 400
    
    try:
        message = close_position(position_id, authenticated_employer_id)
        return jsonify({"message": f"{message}"}), 200
    except Exception as e:
        return jsonify({"error": "Error Closing Position"}), 400
    
@position_views.route('/api/positions/<position_id>/reopen', methods=['POST'])
@jwt_required()
def reopen_position_route(position_id):
    authenticated_employer_id = get_jwt_identity()
    if not authenticated_employer_id:
        return jsonify({"error": "Access Denied - Employer authorization required"}), 401
    
    position = Position.query.filter_by(id=position_id, employer_id=authenticated_employer_id).first()
    if not position:
        return jsonify({"error": "Position not found or access denied"}), 404
    
    if position.status == 'open':
        return jsonify({"error": "Position is already open"}), 400
    
    try:
        message = reopen_position(position_id, authenticated_employer_id)
        return jsonify({"message": f"{message}"}), 200
    except Exception as e:
        return jsonify({"error": "Error Reopening Position"}), 400
