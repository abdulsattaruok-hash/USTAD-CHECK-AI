import streamlit as st
from google import genai
from PIL import Image

st.set_page_config(page_title="UstadCheck AI", page_icon="📝")
st.title("📝 UstadCheck AI: Automated Test Copy Checker")
st.caption("Sindh STEAM / STREAM Project | Track 2: AI & Digital Solutions")

with st.sidebar:
    st.header("Teacher Setup")
    api_key = st.text_input("Enter Google Gemini API Key", type="password")
    subject = st.selectbox("Subject", ["General Science", "Biology", "Chemistry", "Physics", "Mathematics", "English"])
    grade = st.selectbox("Class / Grade", ["Class 6", "Class 7", "Class 8", "Class 9 (Matric)", "Class 10 (Matric)"])

answer_key = st.text_area(
    "1. Paste Correct Answer Key & Marks Distribution",
    placeholder="Example:\nQ1: Define photosynthesis. (2 marks)\nQ2: Write the chemical formula of water. (1 mark)"
)

uploaded_file = st.file_uploader("2. Upload Photo of Student's Handwritten Copy", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Student Copy", use_container_width=True)

if st.button("Check Copy Now", type="primary"):
    if not api_key or not answer_key or not uploaded_file:
        st.error("Please enter your API key, answer key, and upload a copy photo.")
    else:
        with st.spinner("Reading handwriting and evaluating answers..."):
            try:
                client = genai.Client(api_key=api_key)
                prompt = f"""
                You are an experienced {grade} {subject} teacher in Sindh, Pakistan.
                Grade the attached handwritten student test copy strictly based on this Answer Key:
                {answer_key}

                Instructions:
                1. Read the student's handwriting carefully. Ignore crossed-out rough work.
                2. Award partial marks if the concept or formula is partially correct.
                3. Identify specific spelling, factual, or calculation mistakes.
                4. Provide encouraging feedback for the student.

                Return the result in clean Markdown with:
                - Student Name / Roll No (if visible on page)
                - A Question-by-Question Marks Table (Question | Student's Answer Summary | Marks Obtained | Max Marks | Remarks)
                - Total Score & Percentage
                - Key Areas for Improvement
                """
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[image, prompt]
                )
                st.success("Evaluation Complete!")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error: {e}")
