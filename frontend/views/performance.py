import streamlit as st

from frontend.api_client.performance import get_student_performance
from frontend.components.charts import show_gpa_history
from frontend.components.tables import show_course_table


def show_performance():
    st.title("📊 Student Performance")

    # ---------------------------------------------------------
    # Select Student
    # ---------------------------------------------------------

    st.subheader("View Student Performance")

    student_id = st.number_input(
        "Student ID",
        min_value=1,
        step=1,
    )

    if st.button("Load Performance"):

        try:
            performance = get_student_performance(student_id)

            # -------------------------------------------------
            # Student Information
            # -------------------------------------------------

            st.subheader("Student Information")

            col1, col2 = st.columns(2)

            with col1:
                st.write(
                    f"**Student ID:** "
                    f"{performance['student_id']}"
                )

            with col2:
                st.write(
                    f"**Student Name:** "
                    f"{performance['student_name']}"
                )

            # -------------------------------------------------
            # Overall Performance
            # -------------------------------------------------

            st.divider()
            st.subheader("Overall Performance")

            col1, col2, col3 = st.columns(3)

            with col1:
                if performance["cgpa"] is not None:
                    st.metric(
                        "CGPA",
                        f"{performance['cgpa']:.2f}",
                    )
                else:
                    st.metric(
                        "CGPA",
                        "Incomplete",
                    )

            with col2:
                if performance["percentile"] is not None:
                    st.metric(
                        "Percentile",
                        f"{performance['percentile']:.2f}",
                    )
                else:
                    st.metric(
                        "Percentile",
                        "Not enough data",
                    )

            with col3:
                if performance["projected_gpa"] is not None:
                    st.metric(
                        "Projected GPA",
                        f"{performance['projected_gpa']:.2f}",
                    )
                else:
                    st.metric(
                        "Projected GPA",
                        "Not available",
                    )

            # -------------------------------------------------
            # Semester Performance
            # -------------------------------------------------

            st.divider()
            st.subheader("Semester Performance")

            for semester in performance["semesters"]:

                st.markdown(
                    f"### {semester['semester_name']}"
                )

                if semester["gpa"] is not None:
                    st.write(
                        f"**GPA:** "
                        f"{semester['gpa']:.2f}"
                    )
                else:
                    st.write(
                        "**GPA:** Incomplete"
                    )

                # ---------------------------------------------
                # Course Performance
                # ---------------------------------------------

                show_course_table(
                    semester["courses"]
                )

            # -------------------------------------------------
            # GPA History
            # -------------------------------------------------

            st.divider()

            show_gpa_history(
                performance["gpa_history"]
            )

            # -------------------------------------------------
            # Projection Information
            # -------------------------------------------------

            st.divider()
            st.subheader("GPA Projection")

            if performance["projection_available"]:

                st.info(
                    "Projected GPA is an estimate based "
                    "on the student's completed semester "
                    "GPA trend."
                )

            else:

                st.info(
                    "Projection requires at least "
                    "3 completed semesters."
                )

        except Exception as exc:

            st.error(
                f"Unable to load student performance: {exc}"
            )