import streamlit as st
from utils import read_pdf, create_download_data
from medical_codes import extract_all_codes
from code_descriptions import format_code_with_description
from datetime import datetime

st.set_page_config(
    page_title="Prior Auth Manager",
    page_icon="📋",
    layout="wide"
)

API_BASE_URL = "http://localhost:5001/api"

if 'extracted_codes' not in st.session_state:
    st.session_state.extracted_codes = []

# Function to upload extracted data to Databricks
def upload_to_databricks():
    try:
        response = requests.post(f"{API_BASE_URL}/upload-to-databricks", json=st.session_state.extracted_codes)
        if response.status_code == 200:
            st.success("Data successfully uploaded to Databricks!")
        else:
            st.error(f"Error uploading to Databricks: {response.text}")
    except Exception as e:
        st.error(f"Error connecting to Databricks: {str(e)}")

# Function to process individual file with metadata
def process_pdf(file, metadata):
    extracted_data = extract_codes_from_pdf(file)
    if extracted_data:
        for item in extracted_data:
            item.update(metadata)
        st.session_state.extracted_codes.extend(extracted_data)
        st.success(f"Successfully processed {file.name}")
    else:
        st.error(f"No codes extracted from {file.name}")

# UI
st.title("Prior Authorization Code Extractor")
st.write("Upload PDFs and assign metadata to each to extract CPT, HCPCS, and PLA codes.")

uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    st.subheader("Enter Metadata Per File")
    for i, file in enumerate(uploaded_files):
        with st.expander(f"📄 {file.name}", expanded=True):
            payer = st.text_input(f"Payer for {file.name}", key=f"payer_{i}")
            plan = st.text_input(f"Plan for {file.name}", key=f"plan_{i}")
            year = st.number_input(f"Year for {file.name}", min_value=2020, max_value=datetime.now().year,
                                   value=datetime.now().year, key=f"year_{i}")
            lob = st.selectbox(f"Line of Business for {file.name}",
                               ["Medicare", "Medicaid", "Commercial", "Marketplace", "Other"], key=f"lob_{i}")

            if st.button(f"Process {file.name}", key=f"process_{i}"):
                metadata = {
                    "file_name": file.name,
                    "payer": payer,
                    "plan": plan,
                    "year": year,
                    "line_of_business": lob
                }
                process_pdf(file, metadata)

# Display and Export
if st.session_state.extracted_codes:
    st.subheader("Extracted Codes")
    df = pd.DataFrame(st.session_state.extracted_codes)
    st.dataframe(df)

    st.download_button(
        label="Download CSV",
        data=df.to_csv(index=False),
        file_name="extracted_codes_with_metadata.csv",
        mime="text/csv"
    )

    if st.button("Upload to Databricks"):
        upload_to_databricks()