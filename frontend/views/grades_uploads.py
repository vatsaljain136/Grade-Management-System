import streamlit as st

from frontend.api_client.grades import (
    create_grade,
    get_grades,
    update_grade,
)
from frontend.api_client.uploads import upload_grades
from frontend.components.filters import grade_filters
from frontend.components.forms import grade_form
from frontend.components.tables import show_grade_table


def show_grades_uploads():
    st.title("📝 Grades & Uploads")

    # ---------------------------------------------------------
    # Grade Filters
    # ---------------------------------------------------------

    st.subheader("Filter Grades")

    filters = grade_filters()

    if st.button("Search Grades"):
        try:
            grades = get_grades(
                student_id=filters["student_id"],
                semester_id=filters["semester_id"],
                assessment_id=filters["assessment_id"],
            )

            st.subheader("Grade Results")

            show_grade_table(grades)

        except Exception as exc:
            st.error(f"Unable to load grades: {exc}")

    # ---------------------------------------------------------
    # Enter Grade
    # ---------------------------------------------------------

    st.divider()

    with st.form("create_grade_form"):
        grade_data = grade_form(
            title="Enter Grade"
        )

    if grade_data:
        try:
            response = create_grade(grade_data)

            st.success(
                f"Grade saved successfully. "
                f"Grade ID: {response['id']}"
            )

        except Exception as exc:
            st.error(
                f"Unable to save grade: {exc}"
            )

    # ---------------------------------------------------------
    # Update Grade
    # ---------------------------------------------------------

    st.divider()

    st.subheader("Update Grade")

    with st.form("update_grade_form"):

        student_id = st.number_input(
            "Student ID",
            min_value=1,
            step=1,
            key="update_student_id",
        )

        assessment_id = st.number_input(
            "Assessment ID",
            min_value=1,
            step=1,
            key="update_assessment_id",
        )

        marks = st.number_input(
            "New Marks",
            min_value=0.0,
            step=0.01,
            key="update_marks",
        )

        submitted = st.form_submit_button(
            "Update Grade"
        )

    if submitted:
        try:
            response = update_grade(
                student_id,
                assessment_id,
                {"marks": marks},
            )

            st.success(
                f"Grade updated successfully. "
                f"New marks: {response['marks']}"
            )

        except Exception as exc:
            st.error(
                f"Unable to update grade: {exc}"
            )

    # ---------------------------------------------------------
    # Excel Upload
    # ---------------------------------------------------------

    st.divider()

    st.subheader("Upload Grades from Excel")

    st.write(
        "Upload an `.xlsx` file containing "
        "`student_code`, `assessment_id`, and `marks`."
    )

    uploaded_file = st.file_uploader(
        "Choose Excel file",
        type=["xlsx"],
    )

    if uploaded_file is not None:

        if st.button("Upload Grades"):

            try:
                response = upload_grades(
                    uploaded_file
                )

                if response["success"]:

                    st.success(
                        "Grades uploaded successfully."
                    )

                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric(
                            "Created",
                            response["created_count"],
                        )

                    with col2:
                        st.metric(
                            "Updated",
                            response["updated_count"],
                        )

                else:

                    st.error(
                        "Upload failed. "
                        "No changes were saved."
                    )

                    if response["errors"]:

                        st.subheader(
                            "Validation Errors"
                        )

                        for error in response["errors"]:

                            st.write(
                                f"Row {error['row']}: "
                                f"{error['reason']}"
                            )

            except Exception as exc:
                st.error(
                    f"Unable to upload grades: {exc}"
                )