# Grade Management System

A local Student Grade Management System built using **Python, FastAPI, MySQL, SQLAlchemy, Pydantic, and Streamlit**.

The system manages students, academic setup, assessments, grades, Excel grade uploads, and student performance calculations such as GPA, CGPA, percentile, GPA history, and projected GPA.

---

## 1. Tech Stack

### Backend

* Python
* FastAPI
* SQLAlchemy
* Pydantic
* MySQL
* Pandas
* OpenPyXL

### Frontend

* Streamlit
* Requests

---

## 2. Project Structure

```text
grade-management-system/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── validation/
│   │   ├── calculations/
│   │   ├── database/
│   │   ├── config/
│   │   └── utils/
│   │
│   ├── scripts/
│   │   └── seed_data.py
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── app.py
│   ├── views/
│   ├── components/
│   └── api_client/
│
├── data/
│   ├── templates/
│   └── examples/
│
├── tests/
│
├── .env
├── .env.example
├── .gitignore
├── README.md
└── AI_USAGE.md
```

---

## 3. Main Features

### Student Management

* Create students
* View students
* Edit students
* Search by student code or name
* Filter by batch
* Pagination
* Unique student codes

### Academic Setup

* Create semesters
* Edit semesters
* Create courses
* Edit courses
* Create assessments
* Edit assessments
* Filter assessments by course and semester

### Grade Management

* Enter grades
* Update grades
* Retrieve grades
* Filter grades by student, semester, and assessment
* Validate student enrollment
* Validate marks against maximum marks

### Excel Grade Upload

The system accepts `.xlsx` files containing:

```text
student_code
assessment_id
marks
```

The upload process:

1. Reads the Excel file.
2. Validates every row.
3. Checks for duplicate student-assessment combinations.
4. Validates students and assessments.
5. Validates enrollment.
6. Validates marks.
7. Saves changes only if the complete file is valid.
8. Creates missing grades.
9. Updates existing grades.
10. Reports created and updated counts.

If any row is invalid, no changes are saved.

### Student Performance

The system calculates:

* Course percentage
* Course grade point
* Semester GPA
* CGPA
* Percentile
* GPA history
* Projected GPA when sufficient history is available

---

## 4. Calculation Rules

### Course Result

For each assessment:

```text
assessment contribution =
(marks / maximum_marks) × weight
```

The course percentage is the sum of all assessment contributions.

A course result is considered complete only when:

```text
Total assessment weight = 100%
```

Missing marks are treated as incomplete, not as zero.

---

### Grade Points

| Percentage | Grade Point |
| ---------- | ----------: |
| 90–100     |          10 |
| 80–<90     |           9 |
| 70–<80     |           8 |
| 60–<70     |           7 |
| 50–<60     |           6 |
| 40–<50     |           5 |
| Below 40   |           0 |

---

### Semester GPA

```text
GPA =
Σ(grade point × course credits)
--------------------------------
        Σ(course credits)
```

A semester GPA is calculated only when all enrolled courses are complete.

Failed courses are still included.

---

### CGPA

CGPA is calculated using completed semesters and their total credits.

Incomplete semesters are excluded.

```text
CGPA =
Σ(semester GPA × semester credits)
-----------------------------------
        Σ(semester credits)
```

---

### Percentile

Percentile is calculated among eligible students in the same batch and semester.

```text
Percentile =
(number of students with lower GPA / eligible student count) × 100
```

Students with equal GPAs receive the same percentile.

At least two eligible GPAs are required.

---

### Projected GPA

A projected next-semester GPA is calculated only when at least three completed semester GPAs are available.

A straight-line trend is used and the result is constrained to the range:

```text
0 to 10
```

The result is displayed as an estimate.

---

## 5. Database

The system uses MySQL.

Main tables:

```text
students
courses
semesters
enrollments
assessments
grades
```

Relationships:

```text
Student
   │
   └── Enrollment ── Course
          │
          └── Semester

Course + Semester
        │
        └── Assessment
                │
                └── Grade ── Student
```

---

## 6. Environment Setup

### Create a virtual environment

From the project root:

```powershell
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

---

## 7. Install Dependencies

Install the backend dependencies:

```powershell
pip install -r backend\requirements.txt
```

If frontend dependencies are maintained separately, install those as well.

---

## 8. Database Configuration

Create a MySQL database.

Example:

```sql
CREATE DATABASE grade_management;
```

Create a `.env` file in the project root:

```text
DB_HOST=localhost
DB_PORT=3306
DB_NAME=grade_management
DB_USER=your_username
DB_PASSWORD=your_password
```

Do not commit `.env` to Git.

Use `.env.example` as the template for required environment variables.

---

## 9. Create Database Tables

From the project root:

```powershell
python backend\create_tables.py
```

Expected output:

```text
All tables created successfully!
```

---

## 10. Seed Data

The project contains a seed-data script for creating a small fictional academic dataset.

Run:

```powershell
python backend\scripts\seed_data.py
```

The seed data provides students, courses, semesters, enrollments, assessments, and grades for demonstrating the system.

---

## 11. Start the FastAPI Backend

From the project root:

```powershell
python -m uvicorn app.main:app --reload --app-dir backend
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 12. Start the Streamlit Frontend

Open another terminal and activate the virtual environment.

Run:

```powershell
streamlit run frontend\app.py
```

The Streamlit application will open in the browser.

---

## 13. Application Flow

The recommended flow is:

```text
Academic Setup
      │
      ├── Create Semester
      │
      ├── Create Course
      │
      └── Create Assessment
               │
               ▼
          Enroll Student
               │
               ▼
        Enter / Upload Grades
               │
               ▼
       Student Performance
               │
       ┌───────┼────────┐
       ▼       ▼        ▼
      GPA     CGPA   Percentile
               │
               ▼
          GPA History
               │
               ▼
        Projected GPA
```

---

## 14. API Overview

### Students

```text
POST   /students
GET    /students
GET    /students/{student_id}
PUT    /students/{student_id}
```

### Courses

```text
POST   /courses
GET    /courses
GET    /courses/{course_id}
PUT    /courses/{course_id}
```

### Semesters

```text
POST   /semesters
GET    /semesters
GET    /semesters/{semester_id}
PUT    /semesters/{semester_id}
```

### Assessments

```text
POST   /assessments
GET    /assessments
GET    /assessments/{assessment_id}
PUT    /assessments/{assessment_id}
```

### Enrollments

```text
POST   /enrollments
GET    /enrollments
```

### Grades

```text
POST   /grades
GET    /grades
GET    /grades/{grade_id}
GET    /grades/student/{student_id}/assessment/{assessment_id}
PUT    /grades/student/{student_id}/assessment/{assessment_id}
```

### Excel Upload

```text
POST   /uploads/grades
```

### Performance

```text
GET    /performance/students/{student_id}
```

---

## 15. Excel Upload Format

The Excel file must contain:

```text
student_code | assessment_id | marks
```

Example:

```text
STU001 | 1 | 85
STU002 | 1 | 72
STU003 | 2 | 91
```

The system validates the entire file before modifying the database.

---

## 16. Validation

The application validates:

* Duplicate student codes
* Unknown students
* Unknown assessments
* Student enrollment
* Negative marks
* Marks above maximum marks
* Duplicate Excel rows
* Assessment weight limits
* Maximum marks changes
* Positive course credits
* Positive maximum marks

Invalid operations should not partially modify existing data.

---

## 17. Testing

Run the test suite from the project root:

```powershell
python -m pytest -v
```

The tests cover database connectivity and core application functionality.

---

## 18. Git Setup

Initialize the repository:

```powershell
git init
```

Check files:

```powershell
git status
```

Add files:

```powershell
git add .
```

Create the first commit:

```powershell
git commit -m "Initial Grade Management System implementation"
```

Add the remote repository:

```powershell
git remote add origin <repository-url>
```

Push the branch:

```powershell
git branch -M main
git push -u origin main
```

---

## 19. Important Security Notes

Do not commit:

```text
.env
.venv/
__pycache__/
*.pyc
```

Database credentials should remain outside the source code.

Use `.env.example` to document required environment variables without exposing real credentials.

---

## 20. Project Architecture

The application follows a layered architecture:

```text
Streamlit
   │
   ▼
Frontend API Client
   │
   ▼
FastAPI Routes
   │
   ▼
Services
   │
   ├── Validation
   │
   └── Calculations
   │
   ▼
SQLAlchemy
   │
   ▼
MySQL
```

This separation keeps UI, API, business logic, calculations, validation, and database access independent.

---

## 21. AI Usage

AI assistance was used for explanations, debugging support, code review, and implementation guidance.

All generated code was reviewed, integrated, and tested as part of the project development process.

See `AI_USAGE.md` for details.
