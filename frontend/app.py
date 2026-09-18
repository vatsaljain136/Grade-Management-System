import streamlit as st

from frontend.views.grades_uploads import show_grades_uploads
from frontend.views.performance import show_performance
from frontend.views.students import show_students


st.set_page_config(
    page_title="Grade Management System",
    page_icon="🎓",
    layout="wide",
)


st.title("🎓 Grade Management System")

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Students",
        "Grades & Uploads",
        "Student Performance",
    ],
)


if page == "Students":
    show_students()

elif page == "Grades & Uploads":
    show_grades_uploads()

elif page == "Student Performance":
    show_performance()