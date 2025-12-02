from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from App.models import Staff
from App.controllers import (
    get_user_by_username,
    is_staff,
    create_staff,
    list_students,
    get_all_shortlists,
    get_shortlist_by_position_staff,
    get_all_applications,
    get_applications_by_position,
    view_positions
)
from App.models.position import Position

staff_views = Blueprint('staff_views', __name__, template_folder='../templates')

@staff_views.route('/api/staff', methods=['POST'])
def create_staff_endpoint():

    data = request.get_json()
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    email = data.get("email", "").strip()

    if not username or not password or not email:
        return jsonify({"error": "username, password, and email are required"}), 400

    if get_user_by_username(data['username']):
        return jsonify({"error": "username already taken"}), 400
    
    staff = create_staff(username, password, email)
    if staff is None:
        return jsonify({"error": "Failed to create staff"}), 400
    return jsonify({"message": "Staff account created", "staff": staff.get_json()}), 201

    
@staff_views.route('/api/staff/<staff_id>/students', methods=['GET'])
@jwt_required()
def get_students(staff_id):
    authenticated_staff_id = get_jwt_identity()

    #check if the requester is a staff member
    if not is_staff(authenticated_staff_id):
        return jsonify({"error": "Access denied - staff authorization required"}), 401
    
    #check for staff id format
    try:
        int_staff_id = int(staff_id)
    except ValueError:  
        return jsonify({"error": "Invalid staff ID format"}), 400
    
    #check if the staff exists
    staff = Staff.query.get(int_staff_id)
    if not staff:
        return jsonify({"error": "Staff not found"}), 404

    try:
        students = list_students(int_staff_id)
        if students is None:
            return jsonify({"error": "No students found"}), 404
        return jsonify(students), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@staff_views.route('/api/staff/<staff_id>/shortlists', methods=['GET'])
@jwt_required()
def get_shortlists(staff_id):
    authenticated_staff_id = get_jwt_identity()

    #check if the requester is a staff member
    if not is_staff(authenticated_staff_id):
        return jsonify({"error": "Access denied - staff authorization required"}), 401
    
    #check for staff id format
    try:
        int_staff_id = int(staff_id)
    except ValueError:  
        return jsonify({"error": "Invalid staff ID format"}), 400
    
    #check if the staff exists
    staff = Staff.query.get(int_staff_id)
    if not staff:
        return jsonify({"error": "Staff not found"}), 404

    try:
        shortlists = get_all_shortlists(int_staff_id)
        if shortlists is None:
            return jsonify({"error": "No shortlists found"}), 404
        return jsonify(shortlists), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@staff_views.route('/api/staff/<staff_id>/shortlists/<position_id>', methods=['GET'])
@jwt_required()
def get_shortlist_by_position(staff_id, position_id):
    authenticated_staff_id = get_jwt_identity()

    #check if the requester is a staff member
    if not is_staff(authenticated_staff_id):
        return jsonify({"error": "Access denied - staff authorization required"}), 401

    #check for valid staff and position ID format
    try:
        int_staff_id = int(staff_id)
        int_position_id = int(position_id)
    except ValueError:
        return jsonify({"error": "Invalid staff ID format"}), 400

    #check if the staff exists
    staff = Staff.query.get(int_staff_id)
    if not staff:
        return jsonify({"error": "Staff not found"}), 404

    position = Position.query.get(int_position_id)
    if not position:
        return jsonify({"error": f"Position does not exist."}), 404

    try:
        shortlists = get_shortlist_by_position_staff(int_position_id, int_staff_id)
        if shortlists is None:
            return jsonify({"error": "No shortlists found for this position"}), 404
        return jsonify(shortlists), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@staff_views.route('/api/staff/<staff_id>/applications', methods=['GET'])
@jwt_required()
def get_applications(staff_id):
    authenticated_staff_id = get_jwt_identity()

    #check if the requester is a staff member
    if not is_staff(authenticated_staff_id):
        return jsonify({"error": "Access denied - staff authorization required"}), 401
    
    #check for staff id format
    try:
        int_staff_id = int(staff_id)
    except ValueError:  
        return jsonify({"error": "Invalid staff ID format"}), 400
    
    #check if the staff exists
    staff = Staff.query.get(int_staff_id)
    if not staff:
        return jsonify({"error": "Staff not found"}), 404

    try:
        applications = get_all_applications(int_staff_id)
        if applications is None:
            return jsonify({"error": "No applications found"}), 404
        return jsonify(applications), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@staff_views.route('/api/staff/<staff_id>/applications/<position_id>', methods=['GET'])
@jwt_required()
def get_applications_by_position(staff_id, position_id):
    authenticated_staff_id = get_jwt_identity()

    #check if the requester is a staff member
    if not is_staff(authenticated_staff_id):
        return jsonify({"error": "Access denied - staff authorization required"}), 401

    #check for valid staff and position ID format
    try:
        int_staff_id = int(staff_id)
        int_position_id = int(position_id)
    except ValueError:
        return jsonify({"error": "Invalid staff ID format"}), 400

    #check if the staff exists
    staff = Staff.query.get(int_staff_id)
    if not staff:
        return jsonify({"error": "Staff not found"}), 404
    
    position = Position.query.get(int_position_id)
    if not position:
        return jsonify({"error": f"Position does not exist."}), 404

    try:
        applications = get_applications_by_position(int_staff_id, int_position_id)
        if applications is None:
            return jsonify({"error": "No applications found for this position"}), 404
        return jsonify(applications), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@staff_views.route('/api/staff/<staff_id>/positions', methods=['GET'])
@jwt_required() 
def get_positions(staff_id):
    authenticated_staff_id = get_jwt_identity()

    #check if the requester is a staff member
    if not is_staff(authenticated_staff_id):
        return jsonify({"error": "Access denied - staff authorization required"}), 401
    
    #check for staff id format
    try:
        int_staff_id = int(staff_id)
    except ValueError:  
        return jsonify({"error": "Invalid staff ID format"}), 400
    
    #check if the staff exists
    staff = Staff.query.get(int_staff_id)
    if not staff:
        return jsonify({"error": "Staff not found"}), 404

    try:
        positions = view_positions(int_staff_id)
        if positions is None:
            return jsonify({"error": "No positions found"}), 404
        return jsonify(positions), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500