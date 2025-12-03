import pytest
from click.testing import CliRunner
from wsgi import app
import re

@pytest.fixture
def runner():
    return CliRunner()

def extract_id(output, pattern=r'ID: (\d+)'):
    match = re.search(pattern, output)
    if match:
        return match.group(1)
    raise AssertionError(f"Could not extract ID with pattern '{pattern}' from output:\n{output}")

def test_full_cli_workflow(runner):
    # 1. Initialize database
    runner.invoke(app.cli, ['init'])

    # 2. Create staff
    result = runner.invoke(app.cli, ['user', 'create-staff'], input="staffuser\nstaffpass\nstaff@mail.com\n")
    print(result.output)
    assert 'created' in result.output or result.exit_code == 0
    staff_id = extract_id(result.output)
    
    # 3. Create employer
    result = runner.invoke(app.cli, ['user', 'create-employer'], input="employeruser\nemppass\nemployer@mail.com\n")
    print(result.output)
    assert 'created' in result.output or result.exit_code == 0
    employer_id = extract_id(result.output)
    
    # 4. Create student
    result = runner.invoke(app.cli, ['user', 'create-student'], input="stud1\nstudpass\nstud1@mail.com\nJava, C++\n")
    print(result.output)
    assert 'created' in result.output or result.exit_code == 0
    student_id = extract_id(result.output)
    
    # 5. Employer creates a position
    result = runner.invoke(app.cli, ['employer', 'position', str(employer_id or 3), 'Software Intern', '3', 'Python, C++'])
    print(result.output)
    assert 'created' in result.output or result.exit_code == 0
    position_id = extract_id(result.output)
    
    # 6. Staff views positions
    result = runner.invoke(app.cli, ['staff', 'positions', str(staff_id or 1)])
    print(result.output)
    assert 'title' in result.output or result.exit_code == 0
    
    # 7. Staff creates shortlist for the position
    result = runner.invoke(app.cli, ['staff', 'create-shortlist', str(position_id or 3), str(staff_id or 1)])
    print(result.output)
    assert 'Shortlist' in result.output or result.exit_code == 0
    shortlist_id = extract_id(result.output, r'Shortlist ID (\d+)') if 'ID' in result.output else "1"
    
    # 8. Staff lists students
    result = runner.invoke(app.cli, ['staff', 'students', str(staff_id or 1)])
    print(result.output)
    assert 'student' in result.output.lower() or result.exit_code == 0
    
    # 9. Student views open positions
    result = runner.invoke(app.cli, ['student', 'view-positions', str(student_id or 5)])
    print(result.output)
    assert result.exit_code == 0
    
    # 10. Student applies to position
    result = runner.invoke(app.cli, ['student', 'apply', str(student_id or 5), str(position_id or 2)])
    print(result.output)
    assert 'Application created' in result.output or result.exit_code == 0
    
    # 11. Staff views all applications
    result = runner.invoke(app.cli, ['staff', 'applications', str(staff_id or 1)])
    print(result.output)
    assert result.exit_code == 0
    
    # 12. Staff views applications by position
    result = runner.invoke(app.cli, ['staff', 'applications-by-position', str(staff_id or 1), str(position_id or 1)])
    print(result.output)
    assert result.exit_code == 0
    
    # 13. Staff adds application to shortlist (simulate application id 1)
    result = runner.invoke(app.cli, ['staff', 'shortlist-application', str(staff_id or 1), "1"])
    print(result.output)
    assert result.exit_code == 0
    
    # 14. Staff views all shortlists
    result = runner.invoke(app.cli, ['staff', 'shortlists', str(staff_id or 1)])
    print(result.output)
    assert result.exit_code == 0
    
    # 15. Staff views shortlists by position
    result = runner.invoke(app.cli, ['staff', 'shortlists-by-position', str(staff_id or 1), str(position_id or 1)])
    print(result.output)
    assert result.exit_code == 0
    
    # 16. Employer views shortlists
    result = runner.invoke(app.cli, ['employer', 'shortlists', str(employer_id or 3)])
    print(result.output)
    assert result.exit_code == 0
    
    # 17. Employer views shortlists by position
    result = runner.invoke(app.cli, ['employer', 'shortlists-by-position', str(employer_id or 3), str(position_id or 1)])
    print(result.output)
    assert result.exit_code == 0
    
    # 18. Employer accepts student
    result = runner.invoke(app.cli, ['employer', 'accept', str(employer_id or 3), str(position_id or 1), str(student_id or 5)])
    print(result.output)
    assert result.exit_code == 0
    
    # 19. Employer rejects student
    result = runner.invoke(app.cli, ['employer', 'reject', str(employer_id or 3), str(position_id or 1), str(student_id or 5)])
    print(result.output)
    assert result.exit_code == 0
    
    # 20. Student views all applications
    result = runner.invoke(app.cli, ['student', 'get-all-applications', str(student_id or 5)])
    print(result.output)
    assert result.exit_code == 0
    
    # 21. Student views application for a specific position
    result = runner.invoke(app.cli, ['student', 'get-position-application', str(student_id or 5), str(position_id or 2)])
    print(result.output)
    assert result.exit_code == 0
    
    # 22. Student views shortlists
    result = runner.invoke(app.cli, ['student', 'get-shortlists', str(student_id or 5)])
    print(result.output)
    assert result.exit_code == 0
    
    # 23. Student rejects position
    result = runner.invoke(app.cli, ['student', 'reject-position', str(student_id or 5), str(position_id or 1)])
    print(result.output)
    assert result.exit_code == 0
    
    # 24. Employer closes position
    result = runner.invoke(app.cli, ['employer', 'close-position', str(position_id or 1), str(employer_id or 3)])
    print(result.output)
    assert result.exit_code == 0
    
    # 25. Employer reopens position
    result = runner.invoke(app.cli, ['employer', 'reopen-position', str(position_id or 1), str(employer_id or 3)])
    print(result.output)
    assert result.exit_code == 0
    
    # 26. List positions by employer
    result = runner.invoke(app.cli, ['employer', 'list-positions', str(employer_id or 3)])
    print(result.output)
    assert result.exit_code == 0
    
    # 27. User list (all users)
    result = runner.invoke(app.cli, ['user', 'list'])
    print(result.output)
    assert result.exit_code == 0