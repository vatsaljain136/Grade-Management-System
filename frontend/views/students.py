import streamlit as st

from frontend.api_client.students import (
    create_student,
    get_student,
    get_students,
    update_student,
)
from frontend.components.filters import student_filters
from frontend.components.forms import student_form
from frontend.components.tables import show_student_table



# students.py view
#       ↓
# frontend/api_client/students.py
#       ↓
# requests.get/post/put
#       ↓
# FastAPI
#       ↓
# Database


def show_students():
    st.title("👨‍🎓 Students")

    # ---------------------------------------------------------
    # Search and Filters
    # ---------------------------------------------------------

    st.subheader("Search Students")

    filters = student_filters()

    if "student_page" not in st.session_state:   #Streamlit reruns your Python script whenever the user interacts with the UI.
        st.session_state.student_page = 1

    page_size = 10

    if st.button("Search"):
        st.session_state.student_page = 1

    # ---------------------------------------------------------
    # Load Students
    # ---------------------------------------------------------

    try:
        students = get_students(
            search=filters["search"],
            batch=filters["batch"],
            page=st.session_state.student_page,
            page_size=page_size,
        )
    except Exception as exc:
        st.error(f"Unable to load students: {exc}")
        students = []

    # ---------------------------------------------------------
    # Student Table
    # ---------------------------------------------------------

    st.subheader("Student List")

    show_student_table(students)

    # ---------------------------------------------------------
    # Pagination
    # ---------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:
        if st.session_state.student_page > 1:
            if st.button("← Previous"):
                st.session_state.student_page -= 1
                st.rerun()

    with col2:
        if len(students) == page_size:
            if st.button("Next →"):
                st.session_state.student_page += 1
                st.rerun()

    # ---------------------------------------------------------
    # Edit Student Selection
    # ---------------------------------------------------------

    st.divider()
    st.subheader("Edit Student")

    if students:
        student_options = {
            f"{student['student_code']} - {student['name']}": student["id"]
            for student in students
        }

        selected_student = st.selectbox(
            "Select Student",
            options=list(student_options.keys()),
        )

        selected_student_id = student_options[selected_student]

        if st.button("Edit Selected Student"):
            st.session_state.edit_student_id = selected_student_id
            st.rerun()

    # ---------------------------------------------------------
    # Add Student
    # ---------------------------------------------------------

    st.divider()

    with st.form("create_student_form"):
        student_data = student_form(
            title="Add Student"
        )

    if student_data:
        try:
            response = create_student(student_data)

            st.success(
                f"Student {response['student_code']} "
                "created successfully."
            )

            st.rerun()

        except Exception as exc:
            st.error(
                f"Unable to create student: {exc}"
            )

    # ---------------------------------------------------------
    # Edit Student
    # ---------------------------------------------------------

    if "edit_student_id" in st.session_state:

        student_id = st.session_state.edit_student_id

        try:
            student = get_student(student_id)

            st.divider()

            with st.form("edit_student_form"):
                edited_data = student_form(
                    title="Edit Student",
                    student=student,
                )

                cancel = st.form_submit_button(
                    "Cancel"
                )

            if edited_data:
                try:
                    response = update_student(
                        student_id,
                        edited_data,
                    )

                    st.success(
                        f"Student {response['student_code']} "
                        "updated successfully."
                    )

                    del st.session_state.edit_student_id
                    st.rerun()

                except Exception as exc:
                    st.error(
                        f"Unable to update student: {exc}"
                    )

            if cancel:
                del st.session_state.edit_student_id
                st.rerun()

        except Exception as exc:
            st.error(
                f"Unable to load student: {exc}"
            )