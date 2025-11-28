import click, pytest, sys
from flask.cli import with_appcontext, AppGroup
from rich.console import Console
from rich.table import Table

from App.database import db, get_migrate
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize, open_position, get_positions_by_employer)
from App.controllers.position import get_shortlist_by_position
from App.controllers.student import  student_reject_position
from App.controllers.application import get_applications_by_student, create_application


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
    pass

#create staff
@user_cli.command("create-staff", help="Creates a staff user")
def create_staff_command():
    pass

#create employer
@user_cli.command("create-employer", help="Creates an employer user")
def create_employer_command():
    pass


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

#we don't have any applications shortlisted yet, nor do we have a get_shorlist_by_student as yet
@student_cli.command("get-shortlists", help="Gets all shortlists for a student")
@click.argument("student_id", default=5)
def get_shortlist_command(student_id):
    shortlists = get_shortlist_by_student(student_id)
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
def list_positions_command():
    pass

#List all Students
@staff_cli.command("students", help="Lists all students")
def list_students_command():
    pass

#List all applications
@staff_cli.command("applications", help="Views all applications")
def view_applications_command():
    pass

#List all applications for a position
@staff_cli.command("applications-by-position", help="Views all applications for a position")
@click.argument("position_id", default=1)
def view_applications_by_position_command(position_id):
    pass

#List all shortlists
@staff_cli.command("shortlists", help="Views all shortlists")
def view_shortlists_command():
    pass

#List all shortlists for a position
@staff_cli.command("shortlists-by-position", help="Views all applications for a position")
@click.argument("position_id", default=1)
def view_shortlists_by_position_command(position_id):
    pass

#Add an application to a shortlist
@staff_cli.command("add_to_shortlist", help="Adds a student to a shortlist")
@click.argument("student_id", default=1)
@click.argument("position_id", default=1)
def add_to_shortlist_command(student_id, position_id):
    pass

app.cli.add_command(staff_cli) # add the group to the cli


'''
Employer Commands
'''
employer_cli = AppGroup('employer', help='Employer object commands') 

#List all employer shortlists, probably should have one to look at shortlists by position too
@employer_cli.command("shortlists", help="Views all employer shortlists")
def view_employer_shortlists_command():
    pass

#Creates a new position
@employer_cli.command("position", help="Creates a position")
def create_position_command():
    pass

#Accept a student application from a shortlist
@employer_cli.command("accept", help="Accepts an application from a shortlist")
def accept_shortlist_command():
    pass

#Rejects a student application from a shortlist
@employer_cli.command("reject", help="Rejects an application from a shortlist")
def reject_shortlist_command():
    pass

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