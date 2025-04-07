import streamlit as st
import pandas as pd
import requests
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

# Initialize session state variables
if 'extracted_codes' not in st.session_state:
    st.session_state.extracted_codes = []

# Function to upload extracted data to Databricks
def upload_to_databricks(server=None, token=None, schema=None):
    try:
        # Convert data to DataFrame
        df = pd.DataFrame(st.session_state.extracted_codes)
        
        # Show a spinner during the upload process
        with st.spinner("Connecting to Databricks and uploading data..."):
            # In a real implementation, we would use the Databricks API with the provided credentials
            # For now, we'll just simulate the upload based on the provided parameters
            
            if server and token:
                # Create payload with connection details and data
                payload = {
                    "server_url": server,
                    "token": token,
                    "schema": schema or "default",
                    "data": st.session_state.extracted_codes
                }
                
                # In a real-world scenario, you would use the Databricks API here
                # For now, we'll use a placeholder API endpoint
                response = requests.post(f"{API_BASE_URL}/upload-to-databricks", json=payload)
                
                if response.status_code == 200:
                    st.success(f"Data successfully uploaded to Databricks schema '{schema or 'default'}'!")
                else:
                    st.error(f"Error uploading to Databricks: {response.text}")
            else:
                # This should not happen with our form validation, but just in case
                st.error("Missing Databricks connection details. Please provide server URL and token.")
    except Exception as e:
        st.error(f"Error connecting to Databricks: {str(e)}")

# Function to process individual file with metadata
def process_pdf(file, metadata):
    try:
        # Read the PDF content
        pdf_content = read_pdf(file)
        
        if not pdf_content:
            st.error(f"Could not read content from {file.name}")
            return False
        
        # Extract codes from the PDF content
        extracted_data = extract_all_codes(pdf_content)
        
        if extracted_data and len(extracted_data) > 0:
            # Add metadata to each extracted code
            for item in extracted_data:
                item.update(metadata)
                
                # Format the timestamp
                if "timestamp" not in item:
                    item["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Add to session state
            st.session_state.extracted_codes.extend(extracted_data)
            st.success(f"Successfully processed {file.name} - Found {len(extracted_data)} codes")
            return True
        else:
            st.warning(f"No codes extracted from {file.name}")
            return False
    except Exception as e:
        st.error(f"Error processing {file.name}: {str(e)}")
        return False

# UI
st.title("Prior Authorization Code Extractor")
st.write("Upload PDFs and assign metadata to each to extract CPT, HCPCS, and PLA codes.")

uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    st.subheader("Enter Metadata Per File")
    for i, file in enumerate(uploaded_files):
        with st.expander(f"📄 {file.name}", expanded=True):
            # Simplified metadata inputs without redundant filename mentions
            payer = st.text_input("Payer", key=f"payer_{i}")
            plan = st.text_input("Plan", key=f"plan_{i}")
            year = st.number_input("Year", min_value=2020, max_value=datetime.now().year,
                                   value=datetime.now().year, key=f"year_{i}")
            lob = st.selectbox("Line of Business",
                               ["Medicare", "Medicaid", "Commercial", "Marketplace", "Other"], key=f"lob_{i}")

            if st.button(f"Process {file.name}", key=f"process_{i}"):
                metadata = {
                    "file_name": file.name,
                    "payer": payer,
                    "plan": plan,
                    "year": int(year),
                    "line_of_business": lob,
                    "processed_date": datetime.now().strftime("%Y-%m-%d")
                }
                process_pdf(file, metadata)

# Display and Export
if st.session_state.extracted_codes:
    st.subheader("Extracted Codes")
    
    # Convert to DataFrame for display and export
    df = pd.DataFrame(st.session_state.extracted_codes)
    
    # Ensure all metadata columns are present (including the new separate description columns)
    required_columns = ["file_name", "payer", "plan", "year", "line_of_business", 
                       "code", "code_type", "category", "subcategory", "description"]
    for col in required_columns:
        if col not in df.columns:
            df[col] = ""
    
    # Reorganize columns for better display
    column_order = ["code", "code_type", "category", "subcategory", "description", 
                   "file_name", "payer", "plan", "year", "line_of_business", "timestamp"]
    display_df = df[[col for col in column_order if col in df.columns]]
    
    # Show the dataframe with all columns
    st.dataframe(display_df)
    
    # Add a clear button to reset the extracted codes
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.download_button(
            label="Download CSV",
            data=df.to_csv(index=False),
            file_name=f"extracted_codes_with_metadata_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    with col2:
        if st.button("Upload to Databricks"):
            # Create a popup form for Databricks credentials
            with st.popover("Enter Databricks Connection Details"):
                # Add input fields for Databricks connection
                databricks_server = st.text_input("Databricks Server URL", placeholder="https://your-databricks-instance.cloud.databricks.com")
                databricks_token = st.text_input("Databricks Token", type="password")
                databricks_schema = st.text_input("Schema Name", placeholder="default")
                
                # Add a submit button for the popup
                if st.button("Connect and Upload"):
                    if databricks_server and databricks_token:
                        # Call the upload function with parameters
                        upload_to_databricks(server=databricks_server, token=databricks_token, schema=databricks_schema)
                    else:
                        st.error("Please provide both Server URL and Token")
    
    with col3:
        if st.button("Clear All Data"):
            st.session_state.extracted_codes = []
            st.rerun()
