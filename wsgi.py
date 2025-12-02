import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app
from App.controllers.initialize import initialize
from App.controllers.user import get_all_users, get_all_users_json
from App.controllers.student import (
    create_student,
    view_open_positions_by_student,
    get_applications_by_student,
    get_application_by_student_and_position,
    view_my_shortlisted_applications,
    student_reject_position
)
from App.controllers.staff import (
    create_staff,
    view_positions,
    list_students,
    get_all_shortlists,
    get_shortlist_by_position_staff,
    get_all_applications,
    get_applications_by_position
)

from App.controllers.application import (
    create_application,
    add_application_to_shortlist,
)
from App.controllers.shortlist import create_shortlist
from App.controllers.employer import (
    create_employer,
    get_all_shortlists_by_employer,
    get_shortlist_by_position_employer,
    list_positions_by_employer,
    accept_student,
    reject_student,
)
from App.controllers.position import (
    create_position,
    close_position,
    reopen_position
)


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

@app.cli.command("help", help="Show CLI help for all commands")
def show_help():
    print("\nFlask CLI Command Reference\n" + "-"*32)
    print("flask init")
    print("    Initialize the database\n")
    print("User Commands:")
    print("  flask user list                                List all users")
    print("  flask user create-staff                        Create a new staff member (interactive)")
    print("  flask user create-employer                     Create a new employer (interactive)")
    print("  flask user create-student                      Create a new student (interactive)\n")
    print("Student Commands:")
    print("  flask student view-positions <student_id>       List all open positions for a student")
    print("  flask student apply <student_id> <position_id>  Apply to a position")
    print("  flask student get-all-applications <student_id> View all applications for a student")
    print("  flask student get-position-application <student_id> <position_id>  View application for a specific position")
    print("  flask student get-shortlists <student_id>       View all shortlists for a student")
    print("  flask student reject-position <student_id> <position_id>  Reject a position\n")
    print("Staff Commands:")
    print("  flask staff positions <staff_id>                List all positions")
    print("  flask staff create-shortlist <position_id> <staff_id>  Create a shortlist for a position")
    print("  flask staff students <staff_id>                 List all students")
    print("  flask staff applications <staff_id>             View all applications")
    print("  flask staff applications-by-position <staff_id> <position_id>  View applications by position")
    print("  flask staff shortlists <staff_id>               View all shortlists")
    print("  flask staff shortlists-by-position <position_id> <staff_id>  View shortlists by position")
    print("  flask staff shortlist-application <staff_id> <application_id>  Add application to shortlist\n")
    print("Employer Commands:")
    print("  flask employer position <employer_id> <title> <number_of_positions>  Create a position")
    print("  flask employer close-position <position_id> <employer_id>            Close a position")
    print("  flask employer reopen-position <position_id> <employer_id>           Reopen a position")
    print("  flask employer list-positions <employer_id>                          List all positions for an employer")
    print("  flask employer shortlists <employer_id>                              View all employer shortlists")
    print("  flask employer shortlists-by-position <position_id> <employer_id>    View shortlists by position")
    print("  flask employer accept <employer_id> <position_id> <student_id>       Accept a student application")
    print("  flask employer reject <employer_id> <position_id> <student_id>       Reject a student application\n")


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
    skills = click.prompt("Enter skills (comma separated)").split(", ")
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

#list all open positions
@student_cli.command("view-positions", help="Lists all open positions for a student")
@click.argument("student_id", default=5)
def list_open_positions_command(student_id):
    positions = view_open_positions_by_student(student_id)
    if isinstance(positions, list) and positions:
        for position in positions:
            print(position)
    elif isinstance(positions, str):
        print(positions)

@student_cli.command("apply", help="Creates an application for a student to a position")
@click.argument("student_id", default=5)
@click.argument("position_id", default=2)
def create_application_command(student_id, position_id):
    application = create_application(student_id, position_id)
    if isinstance(application, str):
        print(application)
    else:
        print(f'Application created for Student ID {student_id} to Position ID {position_id}')

@student_cli.command("get-all-applications", help="Gets all applications for a student")
@click.argument("student_id", default=5)
def get_applications_command(student_id):
    applications = get_applications_by_student(student_id)
    if isinstance(applications, list) and applications:
        for app in applications:
            print(app)
    elif isinstance(applications, str):
        print(applications)

@student_cli.command("get-position-application", help="Gets student's application for a specific position")
@click.argument("student_id", default=5)
@click.argument("position_id", default=2)
def get_position_application_command(student_id, position_id):
    application = get_application_by_student_and_position(student_id, position_id)
    if isinstance(application, dict):
        print(application)
    else:
        print(application)

#Lists a student's shortlisted applications
@student_cli.command("get-shortlists", help="Gets all shortlists for a student")
@click.argument("student_id", default=5)
def get_shortlist_command(student_id):
    shortlists = view_my_shortlisted_applications(student_id)
    if isinstance(shortlists, list) and shortlists:
        for app in shortlists:
            print(app)
    elif isinstance(shortlists, str):
        print(shortlists)

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
    if isinstance(positions, list) and positions:
        for position in positions:
            print(position)
    elif isinstance(positions, str):
        print(positions)

#Create shortlist for a position
@staff_cli.command("create-shortlist", help="Creates a shortlist for a position")
@click.argument("position_id", default=3)
@click.argument("staff_id", default=1)
def create_shortlist_command(position_id, staff_id):
    shortlist = create_shortlist(position_id, staff_id)
    if isinstance(shortlist, str):
        print(shortlist)
    else:
        print(f'Shortlist created for Position ID {position_id} with Shortlist ID {shortlist.id}')
    
#List all Students
@staff_cli.command("students", help="Lists all students")
@click.argument("staff_id", default=1)
def list_students_command(staff_id):
    students = list_students(staff_id)
    if isinstance(students, list) and students:
        for student in students:
            print(student)
    elif isinstance(students, str):
        print(students)

#List all applications
@staff_cli.command("applications", help="Views all applications")
@click.argument("staff_id", default=1)
def view_applications_command(staff_id):
    applications = get_all_applications(staff_id)
    if isinstance(applications, list) and applications:
        for application in applications:
            print(application)
    elif isinstance(applications, str):
        print(applications)

#List all applications for a position
@staff_cli.command("applications-by-position", help="Views all applications for a position")
@click.argument("staff_id", default=1)
@click.argument("position_id", default=1)
def view_applications_by_position_command(staff_id, position_id):
    application = get_applications_by_position(staff_id, position_id)
    if isinstance(application, list) and application:
        for app in application:
            print(app)
    elif isinstance(application, str):
        print(application)

#List all shortlists
@staff_cli.command("shortlists", help="Views all shortlists")
@click.argument("staff_id", default=1)
def view_shortlists_command(staff_id):
    shortlists = get_all_shortlists(staff_id)
    if isinstance(shortlists, list) and shortlists:
        for shortlist in shortlists:
            print(shortlist)
    elif isinstance(shortlists, str):
        print(shortlists)

#List all shortlists for a position
@staff_cli.command("shortlists-by-position", help="Views all applications for a position")
@click.argument("position_id", default=1)
@click.argument("staff_id", default=1)
def view_shortlists_by_position_command(position_id, staff_id):
    shortlists = get_shortlist_by_position_staff(position_id, staff_id)
    if isinstance(shortlists, list) and shortlists:
        for shortlist in shortlists:
            print(shortlist)
    elif isinstance(shortlists, dict):
        print(shortlists)
    elif isinstance(shortlists, str):
        print(shortlists)

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

@employer_cli.command("close-position", help="Closes a position")
@click.argument("position_id", default=1)
@click.argument("employer_id", default=3)
def close_position_command(position_id, employer_id):
    result = close_position(position_id, employer_id)
    print(result)

# Reopen a position
@employer_cli.command("reopen-position", help="Reopens a closed position")
@click.argument("position_id", default=1)
@click.argument("employer_id", default=3)
def reopen_position_command(position_id, employer_id):
    result = reopen_position(position_id, employer_id)
    print(result)

# List positions by employer
@employer_cli.command("list-positions", help="Lists all positions for an employer")
@click.argument("employer_id", default=3)
def list_positions_by_employer_command(employer_id):
    positions = list_positions_by_employer(employer_id)
    if isinstance(positions, list) and positions:
        for position in positions:
            print(position)
    elif isinstance(positions, str):
        print(positions)
    
#List all employer shortlists, probably should have one to look at shortlists by position too
@employer_cli.command("shortlists", help="Views all employer shortlists")
@click.argument("employer_id", default=3)
def view_employer_shortlists_command(employer_id):
    shortlists = get_all_shortlists_by_employer(employer_id)
    if isinstance(shortlists, list) and shortlists:
        for shortlist in shortlists:
            print(shortlist)
    elif isinstance(shortlists, str):
        print(shortlists)

#List shortlists by position for employer
@employer_cli.command("shortlists-by-position", help="Views all shortlists for an employer's position")
@click.argument("position_id", default=1)
@click.argument("employer_id", default=3)
def view_employer_shortlists_by_position_command(position_id, employer_id ):
    shortlists = get_shortlist_by_position_employer(position_id, employer_id)
    if isinstance(shortlists, list) and shortlists:
        for shortlist in shortlists:
            print(shortlist)
    elif isinstance(shortlists, dict):
        print(shortlists)
    elif isinstance(shortlists, str):
        print(shortlists)

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