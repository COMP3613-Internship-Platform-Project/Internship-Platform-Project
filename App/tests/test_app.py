import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User, Employer, Position, Shortlist, Staff, Student
from App.controllers import (
    create_user,
    get_all_users_json,
    login,
    get_user,
    get_user_by_username,
    update_user,
    open_position
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

# # This fixture creates an empty database for the test and deletes it after the test
# # scope="class" would execute the fixture once and resued for all methods in the class
# @pytest.fixture(autouse=True, scope="function")
# def empty_db():
#     app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    
#     with app.app_context():
#         create_db()
#         yield app.test_client()
#         db.drop_all()


# class UserIntegrationTests(unittest.TestCase):

#     def test_create_user(self):
        
#         staff = create_user("rick", "bobpass", "staff")
#         assert staff.username == "rick" 

#         employer = create_user("sam", "sampass", "employer")
#         assert employer.username == "sam"

#         student = create_user("hannah", "hannahpass", "student")
#         assert student.username == "hannah"

#    # def test_get_all_users_json(self):
#      #   users_json = get_all_users_json()
#       #  self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

#     # Tests data changes in the database
#     #def test_update_user(self):
#       #  update_user(1, "ronnie")
#       #  user = get_user(1)
#        # assert user.username == "ronnie"
        
#     def test_open_position(self):
#         position_count = 2
#         employer = create_user("sally", "sallypass", "employer")
#         assert employer is not None
#         position = open_position("IT Support", employer.id, position_count)
#         positions = get_positions_by_employer(employer.id)
#         assert position is not None
#         assert position.number_of_positions == position_count
#         assert len(positions) > 0
#         assert any(p.id == position.id for p in positions)
        
#         invalid_position = open_position("Developer",-1,1)
#         assert invalid_position is False


#     def test_add_to_shortlist(self):
#         position_count = 3
#         staff = create_user("linda", "lindapass", "staff")
#         assert staff is not None
#         student = create_user("hank", "hankpass", "student")
#         assert student is not None
#         employer =  create_user("ken", "kenpass", "employer")
#         assert employer is not None
#         position = open_position("Database Manager", employer.id, position_count)
#         invalid_position = open_position("Developer",-1,1)
#         assert invalid_position is False
#         added_shortlist = add_student_to_shortlist(student.id, position.id ,staff.id)
#         assert position is not None
#         assert (added_shortlist)
#         shortlists = get_shortlist_by_student(student.id)
#         assert any(s.id == added_shortlist.id for s in shortlists)


#     def test_decide_shortlist(self):
#         position_count = 3
#         student = create_user("jack", "jackpass", "student")
#         assert student is not None
#         staff = create_user ("pat", "patpass", "staff")
#         assert staff is not None
#         employer =  create_user("frank", "pass", "employer")
#         assert employer is not None
#         position = open_position("Intern", employer.id, position_count)
#         assert position is not None
#         stud_shortlist = add_student_to_shortlist(student.id, position.id ,staff.id)
#         assert (stud_shortlist)
#         decided_shortlist = decide_shortlist(student.id, position.id, "accepted")
#         assert (decided_shortlist)
#         shortlists = get_shortlist_by_student(student.id)
#         assert any(s.status == PositionStatus.accepted for s in shortlists)
#         assert position.number_of_positions == (position_count-1)
#         assert len(shortlists) > 0
#         invalid_decision = decide_shortlist(-1, -1, "accepted")
#         assert invalid_decision is False


#     def test_student_view_shortlist(self):

#         student = create_user("john", "johnpass", "student")
#         assert student is not None
#         staff = create_user ("tim", "timpass", "staff")
#         assert staff is not None
#         employer =  create_user("joe", "joepass", "employer")
#         assert employer is not None
#         position = open_position("Software Intern", employer.id, 4)
#         assert position is not None
#         shortlist = add_student_to_shortlist(student.id, position.id ,staff.id)
#         shortlists = get_shortlist_by_student(student.id)
#         assert any(shortlist.id == s.id for s in shortlists)
#         assert len(shortlists) > 0

#     # Tests data changes in the database
#     #def test_update_user(self):
#     #    update_user(1, "ronnie")
#     #   user = get_user(1)
#     #   assert user.username == "ronnie"

