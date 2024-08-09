from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import google.generativeai as genai
import PyPDF2

load_dotenv()  # Take environment variables from .env.

app = Flask(__name__)

# Configure the Gemini API with your key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini model and get responses
def get_gemini_response(input_text, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')  # Updated model name
    response = model.generate_content([input_text, prompt])
    return response.text

# Function to extract text from a PDF file
def extract_text_from_pdf(file_path):
    with open(file_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page].extract_text()
    return text

# API endpoint to handle PDF upload and processing
@app.route('/process-pdf', methods=['POST'])
def process_pdf():
    try:
        # Get the file from the request
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files['file']
        
        # Save the file temporarily
        file_path = os.path.join("temp", file.filename)
        file.save(file_path)

        # Extract text from the PDF
        extracted_text = extract_text_from_pdf(file_path)

        # Input prompt to instruct the model to extract specific details
        input_prompt = """
        You are tasked with processing the text extracted from a PDF document. 
        Your goal is to analyze the content and extract only the following information:
        - Customer details (such as name, address, contact information)
        - Product details (such as product names, quantities, descriptions, and prices)
        - Total Amount (the final amount billed, including any taxes or discounts)

        Return only the extracted details, omitting all other content.
        """

        # Use the extracted text as input for the model
        response = get_gemini_response(extracted_text, input_prompt)

        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Note: We will use Gunicorn to run the application on Render
