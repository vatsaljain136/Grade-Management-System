import streamlit as st


# What this does

# The backend already returns GPA history in this format:
# [
#     {
#         "semester_name": "Semester 1",
#         "sequence": 1,
#         "gpa": 7.5,
#     },
#     {
#         "semester_name": "Semester 2",
#         "sequence": 2,
#         "gpa": 8.2,
#     },
# ]

# The function converts that into chart data:

# Semester 1 → 7.5
# Semester 2 → 8.2

def show_gpa_history(gpa_history):
    st.subheader("GPA History")

    if not gpa_history:
        st.info("No completed semester GPA history available.")
        return

    chart_data = {
        item["semester_name"]: item["gpa"]
        for item in gpa_history
    }

    st.line_chart(chart_data)