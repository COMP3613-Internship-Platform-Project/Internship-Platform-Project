from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from App.models import Employer
from App.controllers import (
    is_employer,
    get_user_by_username,
    create_employer,
    get_shortlisted_applications_for_employer,
    accept_student,
    reject_student,
    get_jwt_identity
)

employer_views = Blueprint('employer_views', __name__, template_folder='../templates')

@employer_views.route('/api/employer', methods=['POST'])
def create_employer_endpoint():
    data = request.json 

    if get_user_by_username(data['username']):
        return jsonify(error='Username already exists'), 400
    
    employer = create_employer(data['username'], data['password'], data['email'])

    try:
        if employer is None:
            return jsonify({"error": "Failed to create employer"}), 400
        return jsonify({"message": "Employer account created", "employer_id": employer.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@employer_views.route('/api/employer/<employer_id>/shortlists', methods=['GET'])
@jwt_required()
def view_shortlisted_applications(employer_id):
    authenticated_employer_id = get_jwt_identity()

    #check if the requester is an employer
    if not is_employer(authenticated_employer_id):
        return jsonify({"error": "Access denied - employer authorization required"}), 401
    
    #check for employer id format
    try:
        int_employer_id = int(employer_id)
    except ValueError:  
        return jsonify({"error": "Invalid employer ID format"}), 400
    
    #check if the employer exists
    employer = Employer.query.get(int_employer_id)
    if not employer:
        return jsonify({"error": "Employer not found"}), 404

    #check if the requester is trying to access their own shortlisted applications
    if str(authenticated_employer_id) != str(employer_id):
        return jsonify({"error": "Access denied - can only view shortlisted applications for your own position"}), 401
    
    try:
        result = get_shortlisted_applications_for_employer(int(employer_id))
        if result is None:
            return jsonify({"error": "No shortlisted applications found"}), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@employer_views.route('/api/positions/<position_id>/accept/<student_id>', methods=['POST'])
@jwt_required()
def accept_student_endpoint(position_id, student_id):
    employer_id = get_jwt_identity()
    
    if not is_employer(employer_id):
        return jsonify({"error": "Access denied - employer authorization required"}), 401
    
    #check for employer id format
    try:
        int_position_id = int(position_id)
        int_student_id = int(student_id)
        int_employer_id = int(employer_id)
    except ValueError:
        return jsonify({"error": "Invalid ID format"}), 400

    result = accept_student(int_employer_id, int_position_id, int_student_id)

    if isinstance(result, str):
        if "accepted" in result:
            return jsonify({"message": result}), 200
        return jsonify({"error": result}), 400

    return jsonify({"message": f"Student ID {student_id} has been accepted"}), 200

@employer_views.route('/api/positions/<position_id>/reject/<student_id>', methods=['POST'])
@jwt_required()
def reject_student_endpoint(position_id, student_id):
    employer_id = get_jwt_identity()

    if not is_employer(employer_id):
        return jsonify({"error": "Access denied - employer authorization required"}), 401

    #check for employer id format
    try:
        int_position_id = int(position_id)
        int_student_id = int(student_id)
        int_employer_id = int(employer_id)
    except ValueError:
        return jsonify({"error": "Invalid ID format"}), 400

    result = reject_student(int_employer_id, int_position_id, int_student_id)

    if isinstance(result, str):
        if "rejected" in result:
            return jsonify({"message": result}), 200
        return jsonify({"error": result}), 400

    return jsonify({"message": f"Student ID {student_id} has been rejected"}), 200