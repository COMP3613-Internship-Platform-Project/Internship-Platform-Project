import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app
from App.controllers.__init__ import *
# from App.controllers.initialize import  initialize
# from App.controllers.position import get_shortlist_by_position, create_position
# from App.controllers.student import  create_student, student_reject_position
# from App.controllers.employer import create_employer, get_shortlisted_applications_for_employer, accept_student, reject_student
# from App.controllers.staff import create_staff, view_positions, list_students, view_shortlists, view_shortlist_by_position, view_applications, view_applications_by_position
# from App.controllers.application import get_applications_by_student, create_application,add_application_to_shortlist


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''
user_cli = AppGroup('user', help='User object commands') 

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

#create student
@user_cli.command("create-student", help="Creates a student user")
def create_student_command():
    username = click.prompt("Enter username")
    password = click.prompt("Enter password")
    email = click.prompt("Enter email")
    skills = click.prompt("Enter skills (comma separated)").split(",")
    student = create_student(username, password, email, skills)
    print(f'Student {student.username} created with ID: {student.id}')

#create staff
@user_cli.command("create-staff", help="Creates a staff user")
def create_staff_command():
    username = click.prompt("Enter username")
    password = click.prompt("Enter password")
    email = click.prompt("Enter email")
    staff = create_staff(username, password, email)
    print(f'Staff {staff.username} created with ID: {staff.id}')

#create employer
@user_cli.command("create-employer", help="Creates an employer user")
def create_employer_command():
    username = click.prompt("Enter username")
    password = click.prompt("Enter password")
    email = click.prompt("Enter email")
    employer = create_employer(username, password, email)
    print(f'Employer {employer.username} created with ID: {employer.id}')


app.cli.add_command(user_cli) # add the group to the cli


'''
Student Commands
'''
student_cli = AppGroup('student', help='Student object commands') 

#Commands go here

@student_cli.command("create-application", help="Creates an application for a student to a position")
@click.argument("student_id", default=5)
@click.argument("position_id", default=2)
def create_application_command(student_id, position_id):
    application = create_application(student_id, position_id)
    if isinstance(application, str):
        print(application)
    else:
        print(f'Application created for Student ID {student_id} to Position ID {position_id}')

@student_cli.command("get-applications", help="Gets all applications for a student")
@click.argument("student_id", default=5)
def get_applications_command(student_id):
    applications = get_applications_by_student(student_id)
    if applications:
        for app in applications:
            print(app)

#Lists a student's shortlisted applications
@student_cli.command("get-shortlists", help="Gets all shortlists for a student")
@click.argument("student_id", default=5)
def get_shortlist_command(student_id):
    shortlists = view_my_shortlisted_applications(student_id)
    if shortlists:
        for app in shortlists:
            print(app)

@student_cli.command("reject-position", help="Student rejects a position they have accepted")
@click.argument("student_id", default=5)
@click.argument("position_id", default=1)
def reject_position_command(student_id, position_id):
    result = student_reject_position(student_id, position_id)
    print(result)

app.cli.add_command(student_cli) # add the group to the cli


'''
Staff Commands
'''
staff_cli = AppGroup('staff', help='Staff object commands') 

#List all positions
@staff_cli.command("positions", help="Lists all positions")
@click.argument("staff_id",default=1)
def list_positions_command(staff_id):
    positions = view_positions(staff_id)
    if positions:
        for position in positions:
            print(position)

#Create shortlist for a position
@staff_cli.command("create-shortlist", help="Creates a shortlist for a position")
@click.argument("position_id", default=1)
def create_shortlist_command(position_id):
    shortlist = create_shortlist(position_id)
    if isinstance(shortlist, str):
        print(shortlist)
    else:
        print(f'Shortlist created for Position ID {position_id} with Shortlist ID {shortlist.id}')

    

#List all Students
@staff_cli.command("students", help="Lists all students")
@click.argument("staff_id", default=1)
def list_students_command(staff_id):
    students = list_students(staff_id)
    if students:
        for student in students:
            print(student)


#List all applications
@staff_cli.command("applications", help="Views all applications")
@click.argument("staff_id", default=1)
def view_applications_command(staff_id):
    applications = view_applications(staff_id)
    if applications:
        for application in applications:
            print(application)

#List all applications for a position
@staff_cli.command("applications-by-position", help="Views all applications for a position")
@click.argument("staff_id", default=1)
@click.argument("position_id", default=1)
def view_applications_by_position_command(staff_id, position_id):
    application = view_applications_by_position(staff_id, position_id)
    if application:
        for app in application:
            print(app)

#List all shortlists
@staff_cli.command("shortlists", help="Views all shortlists")
@click.argument("staff_id", default=1)
def view_shortlists_command(staff_id):
    shortlists = view_shortlists(staff_id)
    if shortlists:
        for shortlist in shortlists:
            print(shortlist)

#List all shortlists for a position
@staff_cli.command("shortlists-by-position", help="Views all applications for a position")
@click.argument("staff_id", default=1)
@click.argument("position_id", default=1)
def view_shortlists_by_position_command(staff_id, position_id):
    shortlists = view_shortlist_by_position(staff_id, position_id)
    if shortlists:
        for shortlist in shortlists:
            print(shortlist)

#Add an application to a shortlist
@staff_cli.command("shortlist-application", help="Adds a student to a shortlist")
@click.argument("staff_id", default=1)
@click.argument("application_id", default=1)
def add_to_shortlist_command(staff_id, application_id):
    application = add_application_to_shortlist(staff_id, application_id)
    if isinstance(application, str):
        print(application)
    else:
        print(f'Application ID {application_id} added to shortlist by Staff ID {staff_id}')
    

app.cli.add_command(staff_cli) # add the group to the cli


'''
Employer Commands
'''
employer_cli = AppGroup('employer', help='Employer object commands') 

#List all employer shortlists, probably should have one to look at shortlists by position too
@employer_cli.command("shortlists", help="Views all employer shortlists")
@click.argument("employer_id", default=3)
def view_employer_shortlists_command(employer_id):
    shortlists = get_shortlisted_applications_for_employer(employer_id)
    if shortlists:
        for shortlist in shortlists:
            print(shortlist)

#Creates a new position
@employer_cli.command("position", help="Creates a position")
@click.argument("employer_id", default=3)
@click.argument("title", default="Internship Position")
@click.argument("number_of_positions", default=5)
def create_position_command(employer_id, title, number_of_positions):
    position = create_position(employer_id, title, number_of_positions)
    if isinstance(position, str):
        print(position)
    else:
        print(f'Position {position.title} created with ID: {position.id}')
    

#Accept a student application from a shortlist
@employer_cli.command("accept", help="Accepts an application from a shortlist")
@click.argument("employer_id", default=3)
@click.argument("position_id", default=1)
@click.argument("student_id", default=5)
def accept_shortlist_command(employer_id, position_id, student_id):
    application = accept_student(employer_id, position_id, student_id)
    if isinstance(application, str):
        print(application)

#Rejects a student application from a shortlist
@employer_cli.command("reject", help="Rejects an application from a shortlist")
@click.argument("employer_id", default=3)
@click.argument("position_id", default=1)
@click.argument("student_id", default=5)
def reject_shortlist_command(employer_id, position_id, student_id):
    application = reject_student(employer_id, position_id, student_id)
    if isinstance(application, str):
        print(application)

app.cli.add_command(employer_cli) # add the group to the cli        


'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)