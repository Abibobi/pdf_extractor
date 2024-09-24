import streamlit as st
import PyPDF2
import pdfplumber
import tabula

# Function to extract text from PDF using PyPDF2
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ''
    for page_num in range(len(reader.pages)):
        text += reader.pages[page_num].extract_text() or ""  # Handle None case
    return text

# Function to extract text using pdfplumber
def extract_text_with_pdfplumber(file):
    with pdfplumber.open(file) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text() or ""  # Handle None case
        return text

# Function to extract tables using tabula-py
def extract_tables_from_pdf(file):
    tables = tabula.read_pdf(file, pages='all', multiple_tables=True, stream=True)
    return tables

# Streamlit App
st.title('PDF Data Extractor')

# Upload the PDF file
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    st.success("File uploaded successfully!")
    
    # Show options for text or table extraction
    extract_option = st.selectbox("What do you want to extract?", ("Text", "Tables"))

    if extract_option == "Text":
        method = st.radio("Choose extraction method", ("PyPDF2", "pdfplumber"))

        if st.button("Extract Text"):
            if method == "PyPDF2":
                pdf_text = extract_text_from_pdf(uploaded_file)
                if pdf_text:
                    st.subheader("Extracted Text (PyPDF2)")
                    st.text_area("Extracted Text", pdf_text, height=300)
                else:
                    st.warning("No text found in the PDF.")
            else:
                pdf_text = extract_text_with_pdfplumber(uploaded_file)
                if pdf_text:
                    st.subheader("Extracted Text (pdfplumber)")
                    st.text_area("Extracted Text", pdf_text, height=300)
                else:
                    st.warning("No text found in the PDF.")

    elif extract_option == "Tables":
        if st.button("Extract Tables"):
            tables = extract_tables_from_pdf(uploaded_file)
            if tables:
                st.subheader("Extracted Tables")
                for i, table in enumerate(tables):
                    st.write(f"Table {i + 1}")
                    st.dataframe(table)  # Display as a dataframe
            else:
                st.warning("No tables found in the PDF.")

else:
    st.info("Please upload a PDF file to get started.")
