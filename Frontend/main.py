import streamlit as st
import requests

# Initialize our Streamlit app
st.set_page_config(page_title="Gemini PDF Demo")

st.header("Details Extract App")
uploaded_file = st.file_uploader("Choose a PDF...", type=["pdf"])

submit = st.button("Extract and Analyze")

# If the submit button is clicked
if submit and uploaded_file is not None:
    try:
        # Save the uploaded file temporarily
        with open(uploaded_file.name, "wb") as file:
            file.write(uploaded_file.getbuffer())

        # Send the file to the Flask API for processing
        files = {'file': open(uploaded_file.name, 'rb')}
        response = requests.post("http://localhost:5000/process-pdf", files=files)
        
        if response.status_code == 200:
            st.subheader("The Response is")
            st.write(response.json().get("response"))
        else:
            st.error(f"Error from server: {response.json().get('error')}")

    except Exception as e:
        st.error(f"Error processing the PDF: {str(e)}")