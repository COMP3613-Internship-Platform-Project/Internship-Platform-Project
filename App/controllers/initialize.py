from App.controllers.staff import create_staff, list_students, view_shortlists, view_positions
from App.controllers.employer import create_employer
from App.controllers.student import create_student
from App.controllers.application import create_application
from App.controllers.shortlist import create_shortlist
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

    shortlist = create_shortlist(int(position.id), int(staff.id))
    shortlist2 = create_shortlist(int(position2.id), int(staff2.id))

    application = create_application(int(student.id), int(position.id))
    application2 = create_application(int(student2.id), int(position2.id))

    print(staff.get_json())
    print(staff2.get_json())
    print(employer.get_json())
    print(employer2.get_json())
    print(student.get_json())
    print(student2.get_json())
    print(position.toJSON())
    print(position2.toJSON())
    print(shortlist.toJSON())
    print(shortlist2.toJSON())
    print(application.toJSON())
    print(application2.toJSON())

    # print(list_students(staff.id))
    # print(view_shortlists(staff.id))
    # print(view_positions(staff.id))
    
    # add_student_to_shortlist(student_id=1, position_id=1, staff_id=3)
