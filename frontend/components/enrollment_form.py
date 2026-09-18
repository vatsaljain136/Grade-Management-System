import streamlit as st


def enrollment_form(students, courses, semesters):
    st.subheader("Enroll Student")

    if not students:
        st.warning("No students available.")
        return None

    if not courses:
        st.warning("No courses available.")
        return None

    if not semesters:
        st.warning("No semesters available.")
        return None

    student_options = {
        f"{student['student_code']} - {student['name']}": student["id"]
        for student in students
    }

    course_options = {
        course["name"]: course["id"]
        for course in courses
    }

    semester_options = {
        semester["name"]: semester["id"]
        for semester in semesters
    }

    with st.form("enrollment_form"):

        student_name = st.selectbox(
            "Student",
            options=list(student_options.keys()),
        )

        course_name = st.selectbox(
            "Course",
            options=list(course_options.keys()),
        )

        semester_name = st.selectbox(
            "Semester",
            options=list(semester_options.keys()),
        )

        submitted = st.form_submit_button(
            "Enroll Student"
        )

    if submitted:
        return {
            "student_id": student_options[student_name],
            "course_id": course_options[course_name],
            "semester_id": semester_options[semester_name],
        }

    return None