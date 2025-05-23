import streamlit as st

# Set the page config first
st.set_page_config(page_title="Resume Analyser")

# Hide Streamlit branding and GitHub link using custom CSS
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}  /* Hides the hamburger menu */
            footer {visibility: hidden;}  /* Hides the footer */
            header {visibility: hidden;}  /* Hides the header */
            .css-18e3th9 {visibility: hidden;}  /* Hides the footer items in the bottom right corner */
            .css-1e8jfi5 {visibility: hidden;}  /* Hides the footer items in the bottom right corner */
            .css-1yqjwxj {visibility: hidden;}  /* Hides the footer items in the bottom right corner */
            .css-1v3fvcr {visibility: hidden;}  /* Hides GitHub link */
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

from dotenv import load_dotenv
load_dotenv()
import base64
import os
import io
import fitz  # PyMuPDF
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define the function to send inputs to Gemini and get a response
def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

# Define the function for processing the uploaded PDF file
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert the PDF to image using PyMuPDF
        pdf_file = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        first_page = pdf_file.load_page(0)  # Get the first page of the PDF

        # Convert the page to a pixmap (image)
        pix = first_page.get_pixmap()

        # Convert the pixmap to byte array in PNG format
        img_byte_arr = io.BytesIO()
        img_bytes = pix.tobytes("png")  # Save the image to bytes in PNG format
        img_byte_arr.write(img_bytes)
        img_byte_arr.seek(0)  # Rewind to the start of the byte array

        # Encode the image into base64 for web use
        pdf_parts = [
            {
                "mime_type": "image/png",  # MIME type for PNG
                "data": base64.b64encode(img_byte_arr.getvalue()).decode()  # Encode image to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit app setup
st.header("Resume Scanner")

input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")
submit3 = st.button("Percentage match")

# Prompts for Gemini model
input_prompt1 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
Your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches
the job description. First, the output should come as percentage and then keywords missing and last final thoughts.
"""

# If the user clicks "Tell Me About the Resume"
if submit1:
    if not input_text.strip():
        st.write("Please enter the job description")
    elif uploaded_file is None:
        st.write("Please upload the resume")
    else:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)

# If the user clicks "Percentage Match"
elif submit3:
    if not input_text.strip():
        st.write("Please enter the job description")
    elif uploaded_file is None:
        st.write("Please upload the resume")
    else:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
