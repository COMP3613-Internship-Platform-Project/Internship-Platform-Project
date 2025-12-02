from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from App.controllers.student import student_reject_position
from App.models.student import Student
from App.controllers import ( 
    get_user_by_username, 
    is_student, 
    create_student, 
    view_open_positions_by_student,
    get_applications_by_student,
    get_application_by_student_and_position,
    view_my_shortlisted_applications
)

student_views = Blueprint('student_views', __name__, template_folder='../templates')

@student_views.route('/api/student', methods=['POST'])
def create_student_endpoint():
    data = request.json

    if get_user_by_username(data['username']):
        return jsonify({"error": "username already taken"}), 400
    
    student = create_student(
        username=data['username'],
        password=data['password'],
        email=data['email'],
        skills=data['skills']
    )

    try:
        if student is None:
            return jsonify({"error": "Failed to create student"}), 400
        return jsonify({"message": "Student account created", "student_id": student.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@student_views.route('/api/student/<student_id>/positions', methods=['GET'])
@jwt_required()
def get_open_positions(student_id):
    authenticated_student_id = get_jwt_identity()

    #check if the requester is a student
    if not is_student(authenticated_student_id):
        return jsonify({"error": "Access denied - student authorization required"}), 401
    
    #check for student id format
    try:
        int_student_id = int(student_id)
    except ValueError:  
        return jsonify({"error": "Invalid student ID format"}), 400
    
    #check if the student exists
    student = Student.query.get(int_student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    #check if the requester is trying to access their own positions
    if int(authenticated_student_id) != int_student_id:
        return jsonify({"error": "Access denied - can only view your own positions"}), 401
    
    try:
        positions = view_open_positions_by_student(int_student_id)
        if positions is None:
            return jsonify({"error": "No open positions found"}), 404
        return jsonify(positions), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@student_views.route('/api/student/<student_id>/applications', methods=['GET'])
@jwt_required()
def view_my_applications_endpoint(student_id):
    authenticated_student_id = get_jwt_identity()

    #check if the requester is a student
    if not is_student(authenticated_student_id):
        return jsonify({"error": "Access denied - student authorization required"}), 401
    
    #check for student id format
    try:
        int_student_id = int(student_id)
    except ValueError:  
        return jsonify({"error": "Invalid student ID format"}), 400
    
    #check if the student exists
    student = Student.query.get(int_student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    
    #check if the requester is trying to access their own applications
    if int(authenticated_student_id) != int_student_id:
        return jsonify({"error": "Access denied - can only view your own applications"}), 401

    try:
        result = get_applications_by_student(int_student_id)
        if result is None:
            return jsonify({"error": "No applications found"}), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@student_views.route('/api/student/<student_id>/application/<position_id>', methods=['GET'])
@jwt_required()
def get_application_by_student_and_position_endpoint(student_id, position_id):
    authenticated_student_id = get_jwt_identity()

    # Check if the requester is a student
    if not is_student(authenticated_student_id):
        return jsonify({"error": "Access denied - student authorization required"}), 401

    # Validate IDs
    try:
        int_student_id = int(student_id)
        int_position_id = int(position_id)
    except ValueError:
        return jsonify({"error": "Invalid ID format"}), 400

    # Check if the student exists
    student = Student.query.get(int_student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    # Only allow the student to view their own application
    if int(authenticated_student_id) != int_student_id:
        return jsonify({"error": "Access denied - can only view your own application"}), 401

    try:
        result = get_application_by_student_and_position(int_student_id, int_position_id)
        if isinstance(result, dict):
            return jsonify(result), 200
        else:
            return jsonify({"error": result}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@student_views.route('/api/student/<student_id>/shortlists', methods=['GET'])
@jwt_required()
def view_my_shortlisted_applications_endpoint(student_id):
    authenticated_student_id = get_jwt_identity()

    #check if the requester is a student
    if not is_student(authenticated_student_id):
        return jsonify({"error": "Access denied - student authorization required"}), 401
    
    #check for student id format
    try:
        int_student_id = int(student_id)
    except ValueError:  
        return jsonify({"error": "Invalid student ID format"}), 400
    
    #check if the student exists
    student = Student.query.get(int_student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    
    # check if the requester is trying to access their own shortlists
    if int(authenticated_student_id) != int_student_id:
        return jsonify({"error": "Access denied - can only view your own shortlists"}), 401

    try:
        result = view_my_shortlisted_applications(int_student_id)
        if result is None:
            return jsonify({"error": "No shortlists found"}), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@student_views.route('/api/student/<student_id>/reject/<position_id>', methods=['PUT'])
@jwt_required()
def reject_position_endpoint(student_id, position_id):
    authenticated_student_id = get_jwt_identity()

    #check if the requester is a student
    if not is_student(authenticated_student_id):
        return jsonify({"error": "Access denied - student authorization required"}), 401
    
    #check for student id format
    try:
        int_student_id = int(student_id)
        int_position_id = int(position_id)
    except ValueError:  
        return jsonify({"error": "Invalid ID format"}), 400
    
    #check if the student exists
    student = Student.query.get(int_student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    
    # check if the requester is trying to access their own shortlists
    if int(authenticated_student_id) != int_student_id:
        return jsonify({"error": "Access denied - can only reject positions for yourself"}), 401

    try:
        result = student_reject_position(int_student_id, int_position_id)
        if isinstance(result, str):
            if "has rejected" in result.lower():
                return jsonify({"message": result}), 200
            return jsonify({"error": result}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500