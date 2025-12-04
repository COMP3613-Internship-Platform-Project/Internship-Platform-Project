# Intership Platform

### The following is built for an application that is meant to take student users applying to internship positions made by employers, the applications are reviewed by university staff members who will place the applications on a shortlist for the employers to review and accept accordingly.

## Requirements 
The aplication utilises a restful API through the Postman application to be run.  
The following can be used to run the Postman API through the CLI
```bash
npm install -g newman

newman run "postman/Deployed/Internship Platform Project Collection.postman_collection.json" -e "postman/Deployed/Internship Platform Project Environment.postman_environment.json"  

newman run "postman/Local/(Local) Internship Platform Project.postman_collection.json" -e "postman/Local/(Local) Internship Platform Project postman_environment.json"  
 ```
# Collaborators
- ### Franchesca James
- ### Marishel Lochan
- ### Jamal Mohammed
- ### Jason Downie


# Internship Platform - CLI Commands Guide

This document outlines all available Flask CLI commands for managing the Internship Platform application.

## Getting Started

To view all available commands:
```bash
flask help
```

To initialize the database:
```bash
flask init
```

---

## Common Usage Scenarios
This is a list of the general workflow for the application, for full command details scroll past until you reach the section of commands you wish to look at.

### Scenario 1: Employer creates position and student applies, is accepted but decides later he doesn't want that position

```bash
# 1. Create a position as employer, you will be prompted to enter skills
flask employer position 3 "Backend Developer Intern" 2
Java, React

# 2. Student applies
flask student apply 5 3

# 3. Staff reviews and shortlists
flask staff shortlist-application 1 3

# 4. Employer accepts application
flask employer accept 3 3

```

```bash
# 5. View all applications
flask student get-all-applications 5

# 6. View specific application
flask student get-position-application 5 3

# 7. Student decides that the position isn't for him
flask student reject-position 5 3

```

```bash
# 8. Staff views all applications
flask staff applications 1

# 9. Staff views applications for specific position
flask staff applications-by-position 1 3

```
### Scenario 2: Student applies but employer rejects student
```bash
# 1. Staff looks at pre-existing application
flask staff applications-by-position 1 2

# 2. Staff shortlists the application
flask staff shortlist-application 1 2

# 2. Employer checks the shortlist for the position
flask employer shortlists-by-position 2 4

# 3. View shortlists
flask student get-shortlists 6

# 4. Employer rejects the application
flask employer reject 2 4

# 5. Student checks their shortlisted application
flask student get-shortlists 6

# 6. Anxious they check positions to see the result
flask student get-position-application 6 2

# 7. Student cries about getting rejected
;-;
```
---

## User Commands

User management commands for creating and listing users.

### List All Users

View all users in the database.

```bash
flask user list [format]
```

**Arguments:**
- `format` (optional, default: "string") - Output format. Use "string" for text output or "json" for JSON format.

**Examples:**
```bash
# List users as text
flask user list string

# List users as JSON
flask user list json
```

### Create a Student

Create a new student user interactively.

```bash
flask user create-student
```

**Interactive Prompts:**
- Username
- Password
- Email
- Skills (comma-separated list)

**Example:**
```bash
flask user create-student
# Enter username: john_doe
# Enter password: password123
# Enter email: john@example.com
# Enter skills (comma separated): Python, JavaScript, React
```

### Create a Staff Member

Create a new staff user interactively.

```bash
flask user create-staff
```

**Interactive Prompts:**
- Username
- Password
- Email

**Example:**
```bash
flask user create-staff
# Enter username: staff_member
# Enter password: staffpass123
# Enter email: staff@example.com
```

### Create an Employer

Create a new employer user interactively.

```bash
flask user create-employer
```

**Interactive Prompts:**
- Username
- Password
- Email

**Example:**
```bash
flask user create-employer
# Enter username: acme_corp
# Enter password: employerpass123
# Enter email: hr@acme.com
```

---

## Student Commands

Student-related commands for viewing positions, applying, and managing applications.

### View Open Positions

List all open positions available for a student.

```bash
flask student view-positions [student_id]
```

**Arguments:**
- `student_id` (optional, default: 5) - The ID of the student

**Example:**
```bash
flask student view-positions 2
```

### Apply to a Position

Create an application for a student to a specific position.

```bash
flask student apply [student_id] [position_id]
```

**Arguments:**
- `student_id` (optional, default: 5) - The ID of the student
- `position_id` (optional, default: 2) - The ID of the position to apply to

**Example:**
```bash
flask student apply 2 3
```

**Returns:**
- Success message with application details, or error message if unable to apply

### Get All Applications

View all applications submitted by a student.

```bash
flask student get-all-applications [student_id]
```

**Arguments:**
- `student_id` (optional, default: 5) - The ID of the student

**Example:**
```bash
flask student get-all-applications 2
```

**Returns:**
- List of applications with employer name, position title, application status, and student details

### Get Application for Specific Position

View a student's application for a specific position.

```bash
flask student get-position-application [student_id] [position_id]
```

**Arguments:**
- `student_id` (optional, default: 5) - The ID of the student
- `position_id` (optional, default: 2) - The ID of the position

**Example:**
```bash
flask student get-position-application 2 3
```

**Returns:**
- Application details or error message if no application exists

### Get Shortlisted Applications

View all applications that have been shortlisted.

```bash
flask student get-shortlists [student_id]
```

**Arguments:**
- `student_id` (optional, default: 5) - The ID of the student

**Example:**
```bash
flask student get-shortlists 2
```

**Returns:**
- List of shortlisted applications with employer and position information

### Reject a Position

Reject an accepted position offer.

```bash
flask student reject-position [student_id] [position_id]
```

**Arguments:**
- `student_id` (optional, default: 5) - The ID of the student
- `position_id` (optional, default: 1) - The ID of the position to reject

**Example:**
```bash
flask student reject-position 2 3
```

**Note:** The application must be in "Accepted" state to reject it.

---

## Staff Commands

Staff-related commands for managing positions, students, applications, and shortlists.

### List All Positions

View all available positions.

```bash
flask staff positions [staff_id]
```

**Arguments:**
- `staff_id` (optional, default: 1) - The ID of the staff member

**Example:**
```bash
flask staff positions 1
```

**Returns:**
- List of positions with title, number of positions, status, and employer information

### Create a Shortlist for a Position

Create a shortlist for a specific position.

```bash
flask staff create-shortlist [position_id] [staff_id]
```

**Arguments:**
- `position_id` (optional, default: 3) - The ID of the position
- `staff_id` (optional, default: 1) - The ID of the staff member

**Example:**
```bash
flask staff create-shortlist 3 1
```

**Returns:**
- Success message with shortlist ID, or error message if shortlist already exists

### List All Students

View all students in the system.

```bash
flask staff students [staff_id]
```

**Arguments:**
- `staff_id` (optional, default: 1) - The ID of the staff member

**Example:**
```bash
flask staff students 1
```

**Returns:**
- List of all students with username, email, skills, and user type

### View All Applications

View all applications across all positions.

```bash
flask staff applications [staff_id]
```

**Arguments:**
- `staff_id` (optional, default: 1) - The ID of the staff member

**Example:**
```bash
flask staff applications 1
```

**Returns:**
- List of all applications with employer, position, student, and status information

### View Applications by Position

View applications for a specific position.

```bash
flask staff applications-by-position [staff_id] [position_id]
```

**Arguments:**
- `staff_id` (optional, default: 1) - The ID of the staff member
- `position_id` (optional, default: 1) - The ID of the position

**Example:**
```bash
flask staff applications-by-position 1 3
```

**Returns:**
- List of applications for the specified position

### View All Shortlists

View all shortlists in the system.

```bash
flask staff shortlists [staff_id]
```

**Arguments:**
- `staff_id` (optional, default: 1) - The ID of the staff member

**Example:**
```bash
flask staff shortlists 1
```

**Returns:**
- List of all shortlists with their associated applications and student information

### View Shortlists by Position

View shortlisted applications for a specific position.

```bash
flask staff shortlists-by-position [position_id] [staff_id]
```

**Arguments:**
- `position_id` (optional, default: 1) - The ID of the position
- `staff_id` (optional, default: 1) - The ID of the staff member

**Example:**
```bash
flask staff shortlists-by-position 3 1
```

**Returns:**
- Shortlist information with shortlisted applications for the position

### Add Application to Shortlist

Move an application from "Applied" status to a shortlist.

```bash
flask staff shortlist-application [staff_id] [application_id]
```

**Arguments:**
- `staff_id` (optional, default: 1) - The ID of the staff member
- `application_id` (optional, default: 1) - The ID of the application to shortlist

**Example:**
```bash
flask staff shortlist-application 1 5
```

**Returns:**
- Success message or error message if application cannot be shortlisted

---

## Employer Commands

Employer-related commands for managing positions, viewing applications, and making hiring decisions.

### Create a Position

Create a new internship position.

```bash
flask employer position [employer_id] [title] [number_of_positions] [skills]
```

**Arguments:**
- `employer_id` (optional, default: 3) - The ID of the employer
- `title` (optional, default: "Internship Position") - The position title
- `number_of_positions` (optional, default: 5) - Number of positions available
- `skills` (optional, default: ["Python", "C++"]) - Required skills (list format)

**Example:**
```bash
flask employer position 3 "Software Engineer Intern" 3 "['Python', 'JavaScript']"
```

**Returns:**
- Success message with position ID, or error message if position already exists

### Close a Position

Close an open position to stop accepting applications.

```bash
flask employer close-position [position_id] [employer_id]
```

**Arguments:**
- `position_id` (optional, default: 1) - The ID of the position
- `employer_id` (optional, default: 3) - The ID of the employer

**Example:**
```bash
flask employer close-position 3 3
```

**Returns:**
- Status message

### Reopen a Position

Reopen a previously closed position.

```bash
flask employer reopen-position [position_id] [employer_id]
```

**Arguments:**
- `position_id` (optional, default: 1) - The ID of the position
- `employer_id` (optional, default: 3) - The ID of the employer

**Example:**
```bash
flask employer reopen-position 3 3
```

**Returns:**
- Status message

### List Positions by Employer

View all positions created by an employer.

```bash
flask employer list-positions [employer_id]
```

**Arguments:**
- `employer_id` (optional, default: 3) - The ID of the employer

**Example:**
```bash
flask employer list-positions 3
```

**Returns:**
- List of positions with details, or error message if no positions exist

### View All Shortlists

View all shortlisted applications for an employer's positions.

```bash
flask employer shortlists [employer_id]
```

**Arguments:**
- `employer_id` (optional, default: 3) - The ID of the employer

**Example:**
```bash
flask employer shortlists 3
```

**Returns:**
- List of shortlisted applications with position and student information

### View Shortlists by Position

View shortlisted applications for a specific position.

```bash
flask employer shortlists-by-position [position_id] [employer_id]
```

**Arguments:**
- `position_id` (optional, default: 1) - The ID of the position
- `employer_id` (optional, default: 3) - The ID of the employer

**Example:**
```bash
flask employer shortlists-by-position 3 3
```

**Returns:**
- Shortlisted applications for the position

### Accept an Application

Accept a shortlisted application and offer the position to the student.

```bash
flask employer accept [application_id] [employer_id]
```

**Arguments:**
- `application_id` (optional, default: 1) - The ID of the application
- `employer_id` (optional, default: 3) - The ID of the employer

**Example:**
```bash
flask employer accept 5 3
```

**Returns:**
- Status message indicating acceptance or error

**Note:** Only shortlisted applications can be accepted.

### Reject an Application

Reject a shortlisted application.

```bash
flask employer reject [application_id] [employer_id]
```

**Arguments:**
- `application_id` (optional, default: 1) - The ID of the application
- `employer_id` (optional, default: 3) - The ID of the employer

**Example:**
```bash
flask employer reject 5 3
```

**Returns:**
- Status message indicating rejection or error

**Note:** Only shortlisted applications can be rejected.

---

## Test Commands

Commands for running unit and integration tests.

### Run User Tests

Execute tests related to user functionality.

```bash
flask test user [test_type]
```

**Arguments:**
- `test_type` (optional, default: "all") - Test type: "unit", "int" (integration), or "all"

**Examples:**
```bash
# Run all user tests
flask test user all

# Run unit tests only
flask test user unit

# Run integration tests only
flask test user int
```

---

## Application State Transitions

The following diagram shows how applications move through states:

```
Applied → Shortlisted → Accepted
   ↓          ↓            ↓
 (error)   Rejected      (final)
```

- **Applied**: Initial state when a student applies to a position
- **Shortlisted**: Staff moves the application to a shortlist
- **Accepted**: Employer accepts the shortlisted application
- **Rejected**: Employer rejects the shortlisted application

---



## Error Handling

Most commands return descriptive error messages if:
- Required entities (user, position, application) don't exist
- Invalid state transitions are attempted
- Authorization checks fail

Always check the returned message for operation status.

---

## Default Values Reference

| Command | Parameter | Default Value |
|---------|-----------|----------------|
| user list | format | "string" |
| student view-positions | student_id | 5 |
| student apply | student_id, position_id | 5, 2 |
| student get-all-applications | student_id | 5 |
| student get-position-application | student_id, position_id | 5, 2 |
| student get-shortlists | student_id | 5 |
| student reject-position | student_id, position_id | 5, 1 |
| staff positions | staff_id | 1 |
| staff create-shortlist | position_id, staff_id | 3, 1 |
| staff students | staff_id | 1 |
| staff applications | staff_id | 1 |
| staff applications-by-position | staff_id, position_id | 1, 1 |
| staff shortlists | staff_id | 1 |
| staff shortlists-by-position | position_id, staff_id | 1, 1 |
| staff shortlist-application | staff_id, application_id | 1, 1 |
| employer position | employer_id, title, number, skills | 3, "Internship Position", 5, ["Python", "C++"] |
| employer close-position | position_id, employer_id | 1, 3 |
| employer reopen-position | position_id, employer_id | 1, 3 |
| employer list-positions | employer_id | 3 |
| employer shortlists | employer_id | 3 |
| employer shortlists-by-position | position_id, employer_id | 1, 3 |
| employer accept | application_id, employer_id | 1, 3 |
| employer reject | application_id, employer_id | 1, 3 |
| test user | type | "all" |
