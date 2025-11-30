from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, current_user
# from App.controllers.position import get_shortlist_by_position
# from App.controllers.student import get_shortlist_by_student
from App.controllers.application import add_application_to_shortlist


shortlist_views = Blueprint('shortlist_views', __name__, template_folder='../templates')

@shortlist_views.route('/api/shortlist/student/<int:student_id>', methods = ['GET'])
@jwt_required()
def get_student_shortlist(student_id):
    
    if current_user.role == 'student' and current_user.id != student_id:
         return jsonify({"message": "Unauthorized user"}), 403
     
     
    shortlists = get_shortlist_by_student(student_id)
    
    return jsonify([s.toJSON() for s in shortlists]), 200

@shortlist_views.route('/api/shortlist/position/<int:position_id>', methods=['GET'])
@jwt_required()
def get_position_shortlist(position_id):
    if current_user.role != 'employer' and current_user.role != 'staff':
        return jsonify({"message": "Unauthorized user"}), 403
    
    
    shortlists = get_shortlist_by_position(position_id)
    return jsonify([s.toJSON() for s in shortlists]), 200 
     