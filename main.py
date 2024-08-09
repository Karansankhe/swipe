import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
import PyPDF2

load_dotenv()  # Take environment variables from .env.

# Configure the Gemini API with your key
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini model and get responses
def get_gemini_response(input_text, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')  # Updated model name
    response = model.generate_content([input_text, prompt])
    return response.text

# Function to extract text from a PDF file
def extract_text_from_pdf(uploaded_file):
    if uploaded_file is not None:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page].extract_text()
        return text
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize our Streamlit app
st.set_page_config(page_title="Gemini PDF Demo")

st.header("Gemini Application")
uploaded_file = st.file_uploader("Choose a PDF...", type=["pdf"])

submit = st.button("Extract and Analyze")

# Input prompt to instruct the model to extract specific details
input_prompt = """
You are tasked with processing the text extracted from a PDF document. 
Your goal is to analyze the content and extract only the following information:
- Customer details (such as name, address, contact information)
- Product details (such as product names, quantities, descriptions, and prices)
- Total Amount (the final amount billed, including any taxes or discounts)

Return only the extracted details, omitting all other content.
"""

# If the submit button is clicked
if submit and uploaded_file is not None:
    try:
        extracted_text = extract_text_from_pdf(uploaded_file)
        
        # Use the extracted text as input for the model
        response = get_gemini_response(extracted_text, input_prompt)
        st.subheader("The Response is")
        st.write(response)
    except Exception as e:
        st.error(f"Error processing the PDF: {str(e)}")
