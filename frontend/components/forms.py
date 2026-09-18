import streamlit as st


def student_form(title="Add Student", student=None):
    st.subheader(title)

    student_code = st.text_input(
        "Student Code",
        value=student["student_code"] if student else "",
    )

    name = st.text_input(
        "Name",
        value=student["name"] if student else "",
    )

    email = st.text_input(
        "Email",
        value=student["email"] if student else "",
    )

    batch = st.text_input(
        "Batch",
        value=student["batch"] if student else "",
    )

    submitted = st.form_submit_button(
        "Save Student"
    )

    if submitted:
        if not all([student_code, name, email, batch]):
            st.warning("Please fill in all fields.")
            return None

        return {
            "student_code": student_code,
            "name": name,
            "email": email,
            "batch": batch,
        }

    return None


def grade_form(title="Enter Grade"):
    st.subheader(title)

    student_id = st.number_input(
        "Student ID",
        min_value=1,
        step=1,
    )

    assessment_id = st.number_input(
        "Assessment ID",
        min_value=1,
        step=1,
    )

    marks = st.number_input(
        "Marks",
        min_value=0.0,
        step=0.01,
    )

    submitted = st.form_submit_button(
        "Save Grade"
    )

    if submitted:
        return {
            "student_id": student_id,
            "assessment_id": assessment_id,
            "marks": marks,
        }

    return None