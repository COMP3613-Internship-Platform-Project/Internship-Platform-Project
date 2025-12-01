from flask import jsonify
import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.controllers.application import create_application
from App.main import create_app
from App.database import db, create_db
from App.models import User, Employer, Staff, Student
from App.controllers import (
    create_user,
    get_all_users,
    create_student,
    create_staff,
    create_employer,
    get_all_users_json,
    login,
    authenticate,
    jwt_authenticate,
    is_staff,
    is_employer,
    is_student,
    logout,
    list_students,
    create_position, 
    close_position, 
    list_positions_by_employer, 
    create_shortlist,
    add_application_to_shortlist, 
    create_application,
    get_all_shortlists,
    get_shortlist_by_position_staff, 
    get_all_applications, 
    get_applications_by_position, 
    get_applications_by_student,
    get_application_by_student_and_position,
    get_shortlist_by_position_employer, 
    get_all_shortlists_by_employer, 
    view_my_shortlisted_applications, 
    accept_student, 
    reject_student
)


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "bobpass", "bob@example.com")
        assert user.username == "bob"
        assert user.email == "bob@example.com"

    def test_get_json(self):
        user = User("bob", "bobpass", "bob@example.com")
        user_json = user.get_json()
        self.assertDictEqual(user_json, {
            "id": user.id,
            "username": "bob",
            "email": "bob@example.com"
        })

    def test_hashed_password(self):
        password = "bobpass"
        user = User("bob", password,"bob@example.com") 
        assert user.password != password

    def test_check_password(self):
        password = "bobpass"
        user = User("bob", password, "bob@example.com") 
        assert user.check_password(password)


    def test_new_student(self):
            student = Student("john", "johnpass", "john@example.com", {"Python", "SQL"})
            assert student.username == "john"
            assert student.email == "john@example.com"
            assert student.skills == {"Python", "SQL"}


    def test_new_staff(self):
        staff = Staff("trudy", "trudypass", "trudy@mail.com")
        assert staff.username == "trudy"
        assert staff.email == "trudy@mail.com"

    def test_new_employer(self):
        employer = Employer("Microsoft", "microsoftpass", "microsoft@mail.com")
        assert employer.username == "Microsoft"
        assert employer.email == "microsoft@mail.com"

    
       

   
'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="function")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    
    with app.app_context():
        create_db()
        yield app.test_client()
        db.drop_all()


class UserIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        user = create_user("bob", "bobpass", "bob@example.com")
        users = get_all_users()
        self.assertIn(user, users)

    def test_create_student(self):
        student = create_student("student", "studentpass","student@mail.com", ["Java", "C++"])
        users = get_all_users()
        self.assertIn(student, users)

    def test_create_staff(self):
        staff = create_staff("trudy", "trudypass","trudy@mail.com")
        users = get_all_users()
        self.assertIn(staff, users)

    def test_create_employer(self):
        employer = create_employer("Microsoft", "microsoftpass","microsoft@mail.com")
        users = get_all_users()
        self.assertIn(employer, users)

    def test_get_all_users_json(self):
        user = create_user("mimi", "mimipass","mimi@example.com")
        users_json = get_all_users_json()
        self.assertIn({"id": 1, 
                       "username":"mimi", 
                       "email":"mimi@example.com",} , users_json)
        
    #authentication test
    def test_login(self): 
        user = create_user("bob", "bobpass","bob@example.com")
        assert login("bob", "bobpass") != None

    def test_invalid_login(self): #add to doc 
        user = create_user("bob", "bobpass","bob@example.com")
        assert login("bob", "wrongpass") == None

    def test_duplicate_user_creation(self): #add to doc 
        user = create_user("bob", "bobpass","bob@example.com")
        with self.assertRaises(Exception):create_user("bob", "anotherpass","bob2@example.com")

    def test_authenticate(self):
        student = create_student("student", "studentpass", "student@mail.com", ["Java", "C++"])
        staff = create_staff("trudy", "trudypass","trudy@mail.com")
        employer = create_employer("Microsoft", "microsoftpass","microsoft@mail.com")
        assert authenticate("student", "studentpass") == student
        assert authenticate("trudy", "trudypass") == staff
        assert authenticate("Microsoft", "microsoftpass") == employer

    def test_jwt_authenticate(self):
        staff = create_staff("trudy", "trudypass","trudy@mail.com")
        student = create_student("student", "studentpass","student@mail.com", ["Java", "C++"])
        employer = create_employer("Microsoft", "microsoftpass","microsoft@mail.com")
        assert jwt_authenticate("trudy", "trudypass") != None
        assert jwt_authenticate("student", "studentpass") != None
        assert jwt_authenticate("Microsoft", "microsoftpass") != None

    def test_is_staff(self):
        staff = create_staff("trudy", "trudypass","trudy@mail.com")
        assert is_staff(staff.id) == True

    def test_is_employer(self):
        employer = create_employer("Microsoft", "microsoftpass","microsoft@mail.com")
        assert is_employer(employer.id) == True

    def test_is_student(self):
        student = create_student("student", "studentpass","student@mail.com", ["Java", "C++"])
        assert is_student(student.id) == True

    def test_logout(self):
        user = create_user("bob", "bobpass","bob@example.com")
        response = login("bob", "bobpass")
        response = jsonify({"msg": "logout successful"})
        assert logout(response) != None

    def test_list_students(self):
        student = create_student("student", "studentpass", "student@mail.com", ["Java", "C++"])
        staff = create_staff("trudy", "trudypass", "trudy@mail.com")
        students_list = list_students(staff.id)
        expected_student = {
            "id": student.id,
            "username": "student",
            "email": "student@mail.com",
            "skills": "Java, C++",
            "type": "student"
        }
        self.assertIn(expected_student, students_list)

    def test_create_position(self):
        employer = create_employer("Google", "googlepass","google@mail.com")
        position = create_position(employer.id, "Software Intern", 5)
        assert position != None
        assert position.status == "Open"

    def test_close_position(self):
        employer = create_employer("Amazon", "amazonpass","amazon@mail.com")
        position = create_position(employer.id, "Data Analyst Intern", 3)
        close_position(position.id, employer.id)
        assert position.status == "Closed"

    def test_close_position_unauthorized(self): #add to doc 
        employer1 = create_employer("Amazon", "amazonpass","amazon@mail.com")
        employer2 = create_employer("eBay", "ebaypass","ebay@mail.com")
        position = create_position(employer1.id, "Data Analyst Intern", 3)
        result = close_position(position.id, employer2.id)
        assert result == f"Employer with ID {employer2.id} is not authorized to close this position."

    def test_close_already_closed_position(self): #add to doc
        employer = create_employer("Amazon", "amazonpass","amazon@mail.com")
        position = create_position(employer.id, "Data Analyst Intern", 3)
        close_position(position.id, employer.id)
        result = close_position(position.id, employer.id)
        assert result == f"Position with ID {position.id} has been closed."

    def test_view_all_positions(self):
        employer = create_employer("Facebook", "facebookpass","facebook@mail.com")
        position1 = create_position(employer.id, "Web Developer Intern", 4)
        position2 = create_position(employer.id, "App Developer Intern", 2)
        positions = list_positions_by_employer(employer.id)
        self.assertIn(position1.toJSON(), positions)
        self.assertIn(position2.toJSON(), positions)


    # tests for Application functionalities can be added here

    def test_create_application(self):
        employer = create_employer("Airbnb", "airbnbpass","airbnb@mail.com")
        position = create_position(employer.id, "Hospitality Intern", 4)
        student = create_student("alice", "alicepass","alice@mail.com", ["JavaScript", "React"])
        application = create_application(student.id, position.id)
        assert application != None

    def test_create_application_position_closed(self): #add to doc 
        employer = create_employer("Airbnb", "airbnbpass","airbnb@mail.com")
        position = create_position(employer.id, "Web developer Intern", 4)
        student = create_student("alice", "alicepass","alice@mail.com", ["JavaScript", "React"])
        message = close_position(position.id, employer.id)
        result = create_application(student.id, position.id)
        assert result == f"Cannot apply to Position ID {position.id} as it is not open."

    def test_create_application_nonexistent_position(self): #add to doc
        student = create_student("alice", "alicepass","alice@mail.com", ["JavaScript", "React"])
        result = create_application(student.id, 82)  # Assuming 82 is a non-existent position ID
        assert result == f"Position with ID 82 does not exist."

    def test_view_all_applications(self):
        employer = create_employer("Tesla", "teslapass","tesla@mail.com")
        staff = create_staff("trudy", "trudypass","trudy@mail.com")
        position = create_position(employer.id, "Engineering Intern", 3)
        student1 = create_student("bob", "bobpass","bob@mail.com", ["Python", "Django"])
        student2 = create_student("carol", "carolpass","carol@mail.com", ["Java", "Spring"])
        application1 = create_application(student1.id, position.id)
        application2 = create_application(student2.id, position.id)
        applications = get_all_applications(staff.id)
        expected_application1 = {
            "application_id": application1.id,
            "employer_name": employer.username,
            "position_title": position.title,
            "application_status": application1.state_value,
            "student_email": student1.email,
            "student_id": student1.id,
            "student_username": student1.username,
        }
        expected_application2 = {
            "application_id": application2.id,
            "employer_name": employer.username,
            "position_title": position.title,
            "application_status": application2.state_value,
            "student_email": student2.email,
            "student_id": student2.id,
            "student_username": student2.username,
        }
        self.assertIn(expected_application1, applications)
        self.assertIn(expected_application2, applications)

    def test_get_applications_by_position(self):
        employer = create_employer("LinkedIn", "linkedinpass","linkedin@mail.com")
        position = create_position(employer.id, "Marketing Intern", 2)
        position2 = create_position(employer.id, "Sales Intern", 2)
        staff = create_staff("trudy", "trudypass","trudy@mail.com")
        student = create_student("dave", "davepass","dave@mail.com", ["Marketing", "SEO"])
        application = create_application(student.id, position.id)
        application2 = create_application(student.id, position2.id) # application for second position
        applications = get_applications_by_position(staff.id, position.id) #shows only applications for first position
        expected_application = {
            "application_id": application.id,
            "employer_name": employer.username,
            "position_title": position.title,
            "application_status": application.state_value,
            "student_email": student.email,
            "student_id": student.id,
            "student_username": student.username,
        }
        expected_application2 = {
            "application_id": application2.id,
            "employer_name": employer.username,
            "position_title": position2.title,
            "application_status": application2.state_value,
            "student_email": student.email,
            "student_id": student.id,
            "student_username": student.username,
        }
        self.assertIn(expected_application, applications)
        self.assertNotIn(expected_application2, applications)


    def test_get_applications_by_student(self):
        employer = create_employer("Adobe", "adobepass","adobe@mail.com")
        position = create_position(employer.id, "Design Intern", 2)
        student = create_student("eva", "evapass","eva@mail.com", ["Design", "Photoshop"])
        student2 = create_student("frank", "frankpass","frank@mail.com", ["Design", "Illustrator"])
        application = create_application(student.id, position.id)
        application2 = create_application(student2.id, position.id) # application for second student
        applications = get_applications_by_student(student.id) #shows only applications for first student
        expected_application = {
            "employer_name": employer.username,
                    "position_title": position.title,
                    "application_status": application.state_value,
                    "studnet_email": student.email,
                    "student_id": student.id,
                    "student_username": student.username,
                    "student_skills": student.skills,
        }
        expected_application2 = {
            "employer_name": employer.username,
                    "position_title": position.title,
                    "application_status": application2.state_value,
                    "studnet_email": student2.email,
                    "student_id": student2.id,
                    "student_username": student2.username,
                    "student_skills": student2.skills,
        }
        self.assertIn(expected_application, applications)
        self.assertNotIn(expected_application2, applications) # second student application should not be in the first student's application list

    def test_get_application_by_student_and_position(self):
        employer = create_employer("Intel", "intelpass","intel@mail.com")
        position = create_position(employer.id, "Hardware Intern", 2)
        student = create_student("gina", "ginapass","gina@mail.com", ["C", "C++"])
        application = create_application(student.id, position.id)
        retrieved_application = get_application_by_student_and_position(student.id, position.id)
        expected_application = {
            "application_id": application.id,
            "employer_name": employer.username,
            "position_title": position.title,
            "application_status": application.state_value,
            "student_email": student.email,
            "student_id": student.id,
            "student_username": student.username,
        }
        self.assertDictEqual(expected_application, retrieved_application)

    #Marishel - Just added tests for shortlist functionalities

    def test_create_shortlist(self):
        employer = create_employer("Netflix", "netflixpass","netflix@mail.com")
        position = create_position(employer.id, "Content Intern", 2)
        staff = create_staff("trudy", "trudypass","trudy@mail.com")
        shortlist = create_shortlist(position.id, staff.id)
        assert shortlist != None

    def test_create_duplicate_shortlist(self): #add to doc
        employer = create_employer("Netflix", "netflixpass","netflix@mail.com")
        position = create_position(employer.id, "Content Intern", 2)
        staff = create_staff("trudy", "trudypass","trudy@mail.com")
        shortlist1 = create_shortlist(position.id, staff.id)
        shortlist2 = create_shortlist(position.id, staff.id)
        assert shortlist2 == f"Shortlist for Position ID {position.id} already exists."

    def test_add_application_to_shortlist(self):
        employer = create_employer("Uber", "uberpass","uber@mail.com")
        position = create_position(employer.id, "Logistics Intern", 3)
        staff = create_staff("trudy", "trudypass","trudy@mail.com")
        student = create_student("john", "johnpass","john@mail.com", ["HTML", "CSS"])
        application = create_application(student.id, position.id)
        shortlist = create_shortlist(position.id, staff.id)
        added_shortlist = add_application_to_shortlist(application.id, shortlist.id)
        assert added_shortlist != None

    def test_add_application_to_shortlist_twice(self): #add to doc
        employer = create_employer("Uber", "uberpass","uber@mail.com")
        position = create_position(employer.id, "Logistics Intern", 3)
        staff = create_staff("trudy", "trudypass","trudy@mail.com")
        student = create_student("john", "johnpass","john@mail.com", ["HTML", "CSS"])
        application = create_application(student.id, position.id)
        shortlist = create_shortlist(position.id, staff.id)
        add_application_to_shortlist(staff.id, application.id)
        result = add_application_to_shortlist(staff.id, application.id)
        assert result == f"Application with ID {application.id} is already in the shortlist for Position ID {position.id}."

    def test_get_shortlist_by_position_staff(self):
        employer = create_employer("Google", "googlepass","google@mail.com")
        position = create_position(employer.id, "Software Intern", 5)
        staff = create_staff("trudy", "trudypass","trudy@mail.com")
        shortlist = create_shortlist(position.id, staff.id)
        shortlist_data = get_shortlist_by_position_staff(position.id, staff.id)
        self.assertDictEqual(shortlist_data, {
        "shortlist_id": shortlist.id,
        "position_id": position.id,
        "position_title": position.title,
        "employer_username": employer.username,
        "applications": "No applications in this shortlist."
    })
        
        
    def test_get_shortlist_by_position_employer(self):
        employer = create_employer("Google", "googlepass","google@mail.com")
        position = create_position(employer.id, "Software Intern", 5)
        staff = create_staff("trudy", "trudypass","trudy@mail.com")
        shortlist = create_shortlist(position.id, staff.id)
        shortlist_data = get_shortlist_by_position_employer(position.id, employer.id)
        self.assertDictEqual(shortlist_data, {
        "shortlist_id": shortlist.id,
        "position_id": position.id,
        "position_title": position.title,
        "employer_username": employer.username,
        "applications": "No applications in this shortlist."
    })
                                    
    
    def test_get_all_shortlists_by_employer(self):
        employer = create_employer("Netflix", "netflixpass","netflix@mail.com")
        position = create_position(employer.id, "Content Intern", 2)
        position2 = create_position(employer.id, "Data Intern", 2)
        staff = create_staff("trudy", "trudypass","trudy@mail.com")
        shortlist = create_shortlist(position.id, staff.id)
        shortlist2 = create_shortlist(position2.id, staff.id)
        shortlists = get_all_shortlists_by_employer(employer.id)
        self.assertListEqual(shortlists, [{
            "shortlist_id": shortlist.id,
            "position_id": position.id,
            "position_title": position.title,
            "employer_username": employer.username,
            "applications": "No applications in this shortlist."
        }, {
            "shortlist_id": shortlist2.id,
            "position_id": position2.id,
            "position_title": position2.title,
            "employer_username": employer.username,
            "applications": "No applications in this shortlist."
        }])


    def test_view_all_shortlists(self):
        employer = create_employer("Spotify", "spotifypass","spotify@mail.com")
        position = create_position(employer.id, "Music Intern", 3)
        staff = create_staff("trudy", "trudypass","trudy@mail.com")
        shortlist = create_shortlist(position.id, staff.id)
        shortlists = get_all_shortlists(staff.id)
        self.assertListEqual(shortlists, [{
            "shortlist_id": shortlist.id,
            "position_id": position.id,
            "position_title": position.title,
            "employer_username": employer.username,
            "applications": "No applications in this shortlist."
        }])

    def test_view_all_shortlists_unauthorized(self): #add to doc 
        employer = create_employer("Spotify", "spotifypass","spotify@mail.com")
        position = create_position(employer.id, "Music Intern", 3)
        staff = create_staff("trudy", "trudypass","trudy@mail.com")
        shortlist = create_shortlist(position.id, staff.id)
        student = create_student("harry", "harrypass","harry@mail.com", ["C#", "HTML"])
        shortlists = get_all_shortlists(student.id)
        assert shortlists == f"Only staff members can access shortlists. Staff with ID {student.id} does not exist."

    def test_view_my_shortlisted_applications(self):
        employer = create_employer("Adobe", "adobepass","adobe@mail.com")
        position = create_position(employer.id, "Design Intern", 2)
        staff = create_staff("trudy", "trudypass","trudy@mail.com")
        student = create_student("eva", "evapass","eva@mail.com", ["Design", "Photoshop"])
        application = create_application(student.id, position.id)
        create_shortlist(position.id, staff.id)
        add_application_to_shortlist(staff.id, application.id)
        shortlisted_applications = view_my_shortlisted_applications(student.id)
        expected_application = {
            "employer_name": employer.username,
            "position_title": position.title,
            "application_status": "Shortlisted",
            "student_id": student.id,
            "student_name": student.username,
            "student_email": student.email,
            "student_skills": student.skills
        }
        self.assertIn(expected_application, shortlisted_applications)

    def test_accept_student(self):
        employer = create_employer("Airbnb", "airbnbpass","airbnb@mail.com")
        position = create_position(employer.id, "Hospitality Intern", 4)
        staff = create_staff("trudy", "trudypass","trudy@mail.com")
        student = create_student("alice", "alicepass","alice@mail.com", ["Java", "React"])
        application = create_application(student.id, position.id)
        shortlist = create_shortlist(position.id, staff.id)
        add_application_to_shortlist(staff.id, application.id)
        accept_student(employer.id, position.id, student.id)
        self.assertEqual(application.state_value, "Accepted")

    def test_accept_unshortlisted_application(self): #add to doc
        employer = create_employer("Airbnb", "airbnbpass", "airbnb@mail.com")
        position = create_position(employer.id, "Hospitality Intern", 4)
        staff = create_staff("trudy", "trudypass", "trudy@mail.com")
        student = create_student("alice", "alicepass", "alice@mail.com", ["Java", "React"])
        application = create_application(student.id, position.id)
        shortlist = create_shortlist(position.id, staff.id)
        result = accept_student(employer.id, position.id, student.id)
        assert result == "Only shortlisted applications can be accepted."
    

    def test_reject_student(self):
        employer = create_employer("Airbnb", "airbnbpass","airbnb@mail.com")
        position = create_position(employer.id, "Hospitality Intern", 4)
        staff = create_staff("trudy", "trudypass","trudy@mail.com")
        student = create_student("alice", "alicepass","alice@mail.com", ["Java", "React"])
        application = create_application(student.id, position.id)
        shortlist = create_shortlist(position.id, staff.id)
        add_application_to_shortlist(staff.id, application.id)
        reject_student(employer.id, position.id, student.id)
        self.assertEqual(application.state_value, "Rejected")

    def test_reject_unauthoried_employer(self): #add to doc
        employer1 = create_employer("Airbnb", "airbnbpass","airbnb@mail.com")
        employer2 = create_employer("VRBO", "vrbopass","vrbo@mail.com")
        position = create_position(employer1.id, "AI Intern", 4)
        staff = create_staff("trudy", "trudypass","trudy@mail.com")
        student = create_student("alice", "alicepass","alice@mail.com", ["Java", "React"])
        application = create_application(student.id, position.id)
        shortlist = create_shortlist(position.id, staff.id)
        add_application_to_shortlist(staff.id, application.id)
        result = reject_student(employer2.id, position.id, student.id)
        assert result == f"Employer with ID {employer2.id} is not authorized to reject students for this position."

