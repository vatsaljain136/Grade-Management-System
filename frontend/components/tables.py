import streamlit as st


def show_student_table(students):
    if not students:
        st.info("No students found.")
        return

    st.dataframe(
        [
            {
                "ID": student["id"],
                "Student Code": student["student_code"],
                "Name": student["name"],
                "Email": student["email"],
                "Batch": student["batch"],
            }
            for student in students
        ],
        use_container_width=True,
        hide_index=True,
    )


def show_grade_table(grades):
    if not grades:
        st.info("No grades found.")
        return

    st.dataframe(
        [
            {
                "Grade ID": grade["id"],
                "Student ID": grade["student_id"],
                "Assessment ID": grade["assessment_id"],
                "Marks": grade["marks"],
            }
            for grade in grades
        ],
        use_container_width=True,
        hide_index=True,
    )


def show_course_table(courses):
    if not courses:
        st.info("No course data available.")
        return

    st.dataframe(
        [
            {
                "Course": course["course_name"],
                "Credits": course["credits"],
                "Percentage": (
                    f"{course['percentage']:.2f}%"
                    if course["percentage"] is not None
                    else "Incomplete"
                ),
                "Grade Point": (
                    f"{course['grade_point']:.2f}"
                    if course["grade_point"] is not None
                    else "Incomplete"
                ),
                "Status": (
                    "Complete"
                    if course["complete"]
                    else "Incomplete"
                ),
            }
            for course in courses
        ],
        use_container_width=True,
        hide_index=True,
    )