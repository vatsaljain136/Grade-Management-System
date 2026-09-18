from frontend.api_client.client import post_request


def upload_grades(file):
    files = {
        "file": (
            file.name,
            file.getvalue(),    #This gets the actual contents of the uploaded file as bytes. st.file_uploader() gives us a Streamlit uploaded-file object.(see streamlit app.py for connected code)
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",  #This tells the server what kind of file you're sending. Microsoft Excel .xlsx file.
        )
    }

    return post_request(
        "/uploads/grades",
        files=files,
    )