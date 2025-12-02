from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from App.controllers.auth import is_staff
from App.models import Position, Shortlist
from App.controllers.shortlist import create_shortlist


shortlist_views = Blueprint('shortlist_views', __name__, template_folder='../templates')

@shortlist_views.route('/api/shortlist', methods = ['POST'])
@jwt_required()
def create_shortlist_route():
    authenticated_staff_id = get_jwt_identity()
    if not is_staff(authenticated_staff_id):
        return jsonify({"error": "Access Denied - Staff authorization required"}), 401
     
    data = request.json
    
    position_id = data['position_id']
    position = Position.query.get(position_id)
    if not position:
        return jsonify({"error": f"Position with ID {position_id} does not exist"}), 400
    
    duplicate = Shortlist.query.filter_by(position_id=position_id).first()
    if duplicate:
        return jsonify({"error": "A shortlist for this position already exists"}), 400
    
    try:
        new_shortlist = create_shortlist(position_id, authenticated_staff_id)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Shortlist Created", 
                    "shortlist_id": f"{new_shortlist.id}"
                    }), 200
    