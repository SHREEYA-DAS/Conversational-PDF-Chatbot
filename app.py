import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from htmlTemplates import css, bot_template, user_template

# Load environment variables
load_dotenv()

# Retrieve API key from .env file
api_key = os.getenv("GOOGLE_API_KEY")

# Validate if API key is found
if not api_key:
    st.error("API key not found. Please check your .env file.")
    st.stop()

# Configure Gemini API
genai.configure(api_key=api_key)

def get_pdf_text(pdf_docs):
    """Extract text from uploaded PDF files."""
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text() or ""  # Handle None case
    return text

def get_text_chunks(text):
    """Split extracted text into smaller chunks."""
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=2000,  # Increased chunk size
        chunk_overlap=200,
        length_function=len
    )
    return text_splitter.split_text(text)

def ask_gemini(question, context):
    """Send user question with context to Gemini API and get a response."""
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"Use the following context to answer the question. If the answer is not in the context, say 'I don't know'. However, you can reply normally to conversational questions.\n\nContext:\n{context}\n\nQuestion: {question}"
    
    response = model.generate_content(prompt)
    
    return response.text.strip() if response and response.text else "I don't know."

def handle_userinput(user_question):
    """Handle user input and display responses."""
    if "text_chunks" not in st.session_state or not st.session_state.text_chunks:
        st.warning("Please upload and process a PDF first.")
        return

    # Combine chunks into context
    context = "\n".join(st.session_state.text_chunks)
    
    # Get response from Gemini
    response = ask_gemini(user_question, context)

    # Display user question
    st.write(user_template.replace("{{MSG}}", user_question), unsafe_allow_html=True)
    
    # Display bot response
    st.write(bot_template.replace("{{MSG}}", response), unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="Chat with your PDFs", layout="wide")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    
    st.title("Chat with your PDFs 📄💬")

    if "text_chunks" not in st.session_state:
        st.session_state.text_chunks = None

    with st.sidebar:
        st.subheader("Upload PDFs")
        pdf_docs = st.file_uploader("Choose PDF files", accept_multiple_files=True, type="pdf")

        if st.button("Process"):
            if not pdf_docs:
                st.warning("Please upload at least one PDF.")
            else:
                with st.spinner("Processing PDFs..."):
                    raw_text = get_pdf_text(pdf_docs)
                    text_chunks = get_text_chunks(raw_text)
                    st.session_state.text_chunks = text_chunks  # Store chunks
                    st.success("PDFs processed successfully!")

    user_question = st.text_input("Ask a question about your documents:")
    
    if user_question:
        handle_userinput(user_question)

if __name__ == '__main__':
    main()
