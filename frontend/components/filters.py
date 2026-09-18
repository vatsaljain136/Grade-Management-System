import streamlit as st


def student_filters():
    col1, col2 = st.columns(2)

    with col1:
        search = st.text_input(
            "Search by student code or name",
            placeholder="Example: STU001 or Asha",
        )

    with col2:
        batch = st.text_input(
            "Batch",
            placeholder="Example: 2026",
        )

    return {
        "search": search or None,
        "batch": batch or None,
    }


def grade_filters():
    col1, col2, col3 = st.columns(3)

    with col1:
        student_id = st.number_input(
            "Student ID",
            min_value=0,
            value=0,
            step=1,
        )

    with col2:
        semester_id = st.number_input(
            "Semester ID",
            min_value=0,
            value=0,
            step=1,
        )

    with col3:
        assessment_id = st.number_input(
            "Assessment ID",
            min_value=0,
            value=0,
            step=1,
        )

    return {
        "student_id": student_id if student_id > 0 else None,
        "semester_id": semester_id if semester_id > 0 else None,
        "assessment_id": assessment_id if assessment_id > 0 else None,
    }