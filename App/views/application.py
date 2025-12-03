from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from App.controllers.application import create_application, add_application_to_shortlist
from App.controllers.auth import is_staff, is_student
from App.controllers.student import get_application_by_student_and_position

application_views = Blueprint('application_views', __name__, template_folder='../templates')

@application_views.route('/api/application' , methods=['POST'])
@jwt_required()
def create_application_endpoint():
    authenticated_student_id = get_jwt_identity()
    if not is_student(authenticated_student_id):
        return jsonify({"error": "Student authentication required"}), 401

    data = request.json

    existing = get_application_by_student_and_position(authenticated_student_id, data['position_id'])
    if isinstance(existing, dict):
        return jsonify({"error": "Application for this position by the student already exists"}), 400
    application = create_application(authenticated_student_id, position_id=data['position_id'])

    try:
        if application is None:
            return jsonify({"error": application}), 400
        return jsonify({"message": "Application created", "application_id": application.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@application_views.route('/api/application/<application_id>/shortlist', methods=['PUT'])
@jwt_required()
def add_application_to_shortlist_endpoint(application_id):
    authenticated_staff_id = get_jwt_identity()
    if not is_staff(authenticated_staff_id):
        return jsonify({"error": "Staff authentication required"}), 401
    
    application = add_application_to_shortlist(staff_id=authenticated_staff_id, application_id=application_id)
    try:
        if application is None:
            return jsonify({"error": application}), 400
        return jsonify({"message": "Application added to shortlist", "application_id": application.id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500