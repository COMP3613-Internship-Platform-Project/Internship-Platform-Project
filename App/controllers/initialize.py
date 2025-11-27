from App.controllers.staff import create_staff
from App.controllers.employer import create_employer
from App.controllers.student import create_student
from .shortlist import add_student_to_shortlist
from .position import open_position
from App.database import db


def initialize():
    db.drop_all()
    db.create_all()

    staff = create_staff("sally", "sallypass", "sally@staff.com")
    staff2 = create_staff("pam", "pampass", "pam@staff.com")

    employer = create_employer("Unit Trust", "password", "unit.trust@unit.com")
    employer2 = create_employer("evee", "eveepass", "evee@evee.com")

    student = create_student("johndoe", "johndoepass", "john.doe@student.com", ["Java", "Python", "React"])
    student2 = create_student("acelaw", "acepass", "ace.law@student.com", ["R", "Python", "SQL"])

    position = open_position(
        int(employer.id), "Software Engineer", 2
    )

    position2 = open_position(
        int(employer2.id), "Data Analyst", 3
    )

    print(staff.get_json())
    print(staff2.get_json())
    print(employer.get_json())
    print(employer2.get_json())
    print(student.get_json())
    print(student2.get_json())
    print(position.toJSON())
    print(position2.toJSON())

    # open_position(user_id=2, title='Software Engineer', number_of_positions= 6)
    # open_position(user_id=2, title='Mechanical Engineer', number_of_positions= 6)
    # add_student_to_shortlist(student_id=1, position_id=1, staff_id=3)
