import streamlit as st

from frontend.api_client.courses import (
    create_course,
    get_courses,
    update_course,
)

from frontend.api_client.semesters import (
    create_semester,
    get_semesters,
    update_semester,
)

from frontend.api_client.assessments import (
    create_assessment,
    get_assessments,
    update_assessment,
)

from frontend.api_client.students import get_students
from frontend.api_client.enrollments import create_enrollment
from frontend.components.enrollment_form import enrollment_form


#  Academic Setup

# ┌────────────┬──────────┬──────────────┬──────────────────┐
# │ Semesters  │ Courses  │ Assessments  │ Enroll Students  │
# └────────────┴──────────┴──────────────┴──────────────────┘

# TLDR basically

# Add/edit semesters.
# Add/edit courses.
# Select a course + semester.
# Add assessments to that combination.
# Edit existing assessments.
# See assessment weight and maximum marks.
# Enroll students into courses and semesters.


def show_academic_setup():
    st.title("📚 Academic Setup")

    # ADDED: tab4
    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Semesters",
            "Courses",
            "Assessments",
            "Enroll Students",
        ]
    )

    # ---------------------------------------------------------
    # SEMESTERS
    # ---------------------------------------------------------

    with tab1:
        st.header("Semester Management")

        try:
            semesters = get_semesters()
        except Exception as exc:
            st.error(f"Unable to load semesters: {exc}")
            semesters = []

        if semesters:
            st.dataframe(
                [
                    {
                        "ID": semester["id"],
                        "Name": semester["name"],
                        "Sequence": semester["sequence"],
                    }
                    for semester in semesters
                ],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No semesters available.")

        st.divider()

        st.subheader("Add Semester")

        with st.form("create_semester_form"):
            semester_name = st.text_input(
                "Semester Name",
                placeholder="Example: Semester 1",
            )

            semester_sequence = st.number_input(
                "Sequence",
                min_value=1,
                step=1,
            )

            submitted = st.form_submit_button(
                "Add Semester"
            )

            if submitted:
                if not semester_name.strip():
                    st.warning("Semester name is required.")
                else:
                    try:
                        create_semester(
                            {
                                "name": semester_name.strip(),
                                "sequence": semester_sequence,
                            }
                        )

                        st.success(
                            "Semester created successfully."
                        )

                        st.rerun()

                    except Exception as exc:
                        st.error(
                            f"Unable to create semester: {exc}"
                        )

        st.divider()

        st.subheader("Edit Semester")

        if semesters:
            semester_options = {
                f"{semester['sequence']} - {semester['name']}":
                    semester["id"]
                for semester in semesters
            }

            selected_semester = st.selectbox(
                "Select Semester",
                options=list(semester_options.keys()),
            )

            selected_semester_id = semester_options[
                selected_semester
            ]

            selected_semester_data = next(
                semester
                for semester in semesters
                if semester["id"] == selected_semester_id
            )

            with st.form("edit_semester_form"):
                new_name = st.text_input(
                    "Semester Name",
                    value=selected_semester_data["name"],
                )

                new_sequence = st.number_input(
                    "Sequence",
                    min_value=1,
                    value=selected_semester_data["sequence"],
                    step=1,
                )

                update_submitted = st.form_submit_button(
                    "Update Semester"
                )

                if update_submitted:
                    if not new_name.strip():
                        st.warning(
                            "Semester name is required."
                        )
                    else:
                        try:
                            update_semester(
                                selected_semester_id,
                                {
                                    "name": new_name.strip(),
                                    "sequence": new_sequence,
                                },
                            )

                            st.success(
                                "Semester updated successfully."
                            )

                            st.rerun()

                        except Exception as exc:
                            st.error(
                                f"Unable to update semester: {exc}"
                            )

    # ---------------------------------------------------------
    # COURSES
    # ---------------------------------------------------------

    with tab2:
        st.header("Course Management")

        try:
            courses = get_courses()
        except Exception as exc:
            st.error(f"Unable to load courses: {exc}")
            courses = []

        if courses:
            st.dataframe(
                [
                    {
                        "ID": course["id"],
                        "Code": course["code"],
                        "Name": course["name"],
                        "Credits": course["credits"],
                    }
                    for course in courses
                ],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No courses available.")

        st.divider()

        st.subheader("Add Course")

        with st.form("create_course_form"):
            course_code = st.text_input(
                "Course Code",
                placeholder="Example: CS101",
            )

            course_name = st.text_input(
                "Course Name",
                placeholder="Example: Python Programming",
            )

            course_credits = st.number_input(
                "Credits",
                min_value=0.01,
                step=0.5,
            )

            submitted = st.form_submit_button(
                "Add Course"
            )

            if submitted:
                if not course_code.strip():
                    st.warning("Course code is required.")
                elif not course_name.strip():
                    st.warning("Course name is required.")
                else:
                    try:
                        create_course(
                            {
                                "code": course_code.strip(),
                                "name": course_name.strip(),
                                "credits": course_credits,
                            }
                        )

                        st.success(
                            "Course created successfully."
                        )

                        st.rerun()

                    except Exception as exc:
                        st.error(
                            f"Unable to create course: {exc}"
                        )

        st.divider()

        st.subheader("Edit Course")

        if courses:
            course_options = {
                f"{course['code']} - {course['name']}":
                    course["id"]
                for course in courses
            }

            selected_course = st.selectbox(
                "Select Course",
                options=list(course_options.keys()),
            )

            selected_course_id = course_options[
                selected_course
            ]

            selected_course_data = next(
                course
                for course in courses
                if course["id"] == selected_course_id
            )

            with st.form("edit_course_form"):
                new_code = st.text_input(
                    "Course Code",
                    value=selected_course_data["code"],
                )

                new_name = st.text_input(
                    "Course Name",
                    value=selected_course_data["name"],
                )

                new_credits = st.number_input(
                    "Credits",
                    min_value=0.01,
                    value=float(
                        selected_course_data["credits"]
                    ),
                    step=0.5,
                )

                update_submitted = st.form_submit_button(
                    "Update Course"
                )

                if update_submitted:
                    if not new_code.strip():
                        st.warning(
                            "Course code is required."
                        )
                    elif not new_name.strip():
                        st.warning(
                            "Course name is required."
                        )
                    else:
                        try:
                            update_course(
                                selected_course_id,
                                {
                                    "code": new_code.strip(),
                                    "name": new_name.strip(),
                                    "credits": new_credits,
                                },
                            )

                            st.success(
                                "Course updated successfully."
                            )

                            st.rerun()

                        except Exception as exc:
                            st.error(
                                f"Unable to update course: {exc}"
                            )

    # ---------------------------------------------------------
    # ASSESSMENTS
    # ---------------------------------------------------------

    with tab3:
        st.header("Assessment Management")

        try:
            courses = get_courses()
            semesters = get_semesters()
        except Exception as exc:
            st.error(
                f"Unable to load academic data: {exc}"
            )
            courses = []
            semesters = []

        if not courses or not semesters:
            st.info(
                "Please create at least one course and "
                "one semester before adding assessments."
            )
        else:
            course_options = {
                f"{course['code']} - {course['name']}":
                    course["id"]
                for course in courses
            }

            semester_options = {
                f"{semester['sequence']} - {semester['name']}":
                    semester["id"]
                for semester in semesters
            }

            selected_course = st.selectbox(
                "Course",
                options=list(course_options.keys()),
                key="assessment_course",
            )

            selected_semester = st.selectbox(
                "Semester",
                options=list(semester_options.keys()),
                key="assessment_semester",
            )

            course_id = course_options[selected_course]
            semester_id = semester_options[selected_semester]

            try:
                assessments = get_assessments(
                    course_id=course_id,
                    semester_id=semester_id,
                )
            except Exception as exc:
                st.error(
                    f"Unable to load assessments: {exc}"
                )
                assessments = []

            if assessments:
                st.subheader("Existing Assessments")

                st.dataframe(
                    [
                        {
                            "ID": assessment["id"],
                            "Title": assessment["title"],
                            "Type": assessment["type"],
                            "Maximum Marks": assessment[
                                "maximum_marks"
                            ],
                            "Weight": assessment["weight"],
                        }
                        for assessment in assessments
                    ],
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.info(
                    "No assessments available for "
                    "this course and semester."
                )

            st.divider()

            st.subheader("Add Assessment")

            with st.form("create_assessment_form"):
                title = st.text_input(
                    "Assessment Title",
                    placeholder="Example: Python Assignment 1",
                )

                assessment_type = st.selectbox(
                    "Assessment Type",
                    [
                        "assignment",
                        "project",
                        "quiz",
                        "exam",
                    ],
                )

                maximum_marks = st.number_input(
                    "Maximum Marks",
                    min_value=0.01,
                    step=1.0,
                )

                weight = st.number_input(
                    "Weight (%)",
                    min_value=0.0,
                    max_value=100.0,
                    step=1.0,
                )

                submitted = st.form_submit_button(
                    "Add Assessment"
                )

                if submitted:
                    if not title.strip():
                        st.warning(
                            "Assessment title is required."
                        )
                    else:
                        try:
                            create_assessment(
                                {
                                    "course_id": course_id,
                                    "semester_id": semester_id,
                                    "title": title.strip(),
                                    "type": assessment_type,
                                    "maximum_marks": maximum_marks,
                                    "weight": weight,
                                }
                            )

                            st.success(
                                "Assessment created successfully."
                            )

                            st.rerun()

                        except Exception as exc:
                            st.error(
                                f"Unable to create assessment: {exc}"
                            )

            st.divider()

            st.subheader("Edit Assessment")

            if assessments:
                assessment_options = {
                    f"{assessment['title']} "
                    f"({assessment['type']})":
                        assessment["id"]
                    for assessment in assessments
                }

                selected_assessment = st.selectbox(
                    "Select Assessment",
                    options=list(
                        assessment_options.keys()
                    ),
                )

                selected_assessment_id = (
                    assessment_options[
                        selected_assessment
                    ]
                )

                selected_assessment_data = next(
                    assessment
                    for assessment in assessments
                    if assessment["id"]
                    == selected_assessment_id
                )

                with st.form("edit_assessment_form"):
                    new_title = st.text_input(
                        "Assessment Title",
                        value=selected_assessment_data[
                            "title"
                        ],
                    )

                    new_type = st.selectbox(
                        "Assessment Type",
                        [
                            "assignment",
                            "project",
                            "quiz",
                            "exam",
                        ],
                        index=[
                            "assignment",
                            "project",
                            "quiz",
                            "exam",
                        ].index(
                            selected_assessment_data["type"]
                        ),
                    )

                    new_maximum_marks = st.number_input(
                        "Maximum Marks",
                        min_value=0.01,
                        value=float(
                            selected_assessment_data[
                                "maximum_marks"
                            ]
                        ),
                        step=1.0,
                    )

                    new_weight = st.number_input(
                        "Weight (%)",
                        min_value=0.0,
                        max_value=100.0,
                        value=float(
                            selected_assessment_data[
                                "weight"
                            ]
                        ),
                        step=1.0,
                    )

                    update_submitted = (
                        st.form_submit_button(
                            "Update Assessment"
                        )
                    )

                    if update_submitted:
                        if not new_title.strip():
                            st.warning(
                                "Assessment title is required."
                            )
                        else:
                            try:
                                update_assessment(
                                    selected_assessment_id,
                                    {
                                        "title": new_title.strip(),
                                        "type": new_type,
                                        "maximum_marks":
                                            new_maximum_marks,
                                        "weight": new_weight,
                                    },
                                )

                                st.success(
                                    "Assessment updated successfully."
                                )

                                st.rerun()

                            except Exception as exc:
                                st.error(
                                    "Unable to update assessment: "
                                    f"{exc}"
                                )

    # Enrollment 

    with tab4:
        st.header("Student Enrollment")

        # Load students, courses and semesters
        try:
            students = get_students()
            courses = get_courses()
            semesters = get_semesters()

        except Exception as exc:
            st.error(
                f"Unable to load enrollment data: {exc}"
            )

            students = []
            courses = []
            semesters = []

        # Show enrollment form only when all required
        # academic data is available.
        if not students:
            st.info(
                "Please create at least one student "
                "before enrolling."
            )

        elif not courses:
            st.info(
                "Please create at least one course "
                "before enrolling."
            )

        elif not semesters:
            st.info(
                "Please create at least one semester "
                "before enrolling."
            )

        else:
            enrollment_data = enrollment_form(
                students=students,
                courses=courses,
                semesters=semesters,
            )

            if enrollment_data:
                try:
                    create_enrollment(
                        student_id=enrollment_data[
                            "student_id"
                        ],
                        course_id=enrollment_data[
                            "course_id"
                        ],
                        semester_id=enrollment_data[
                            "semester_id"
                        ],
                    )

                    st.success(
                        "Student enrolled successfully."
                    )

                    st.rerun()

                except Exception as exc:
                    st.error(
                        f"Unable to enroll student: {exc}"
                    )