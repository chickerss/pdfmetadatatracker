import io
import PyPDF2
import pandas as pd
from datetime import datetime

def read_pdf(uploaded_file):
    """
    Extract text content from an uploaded PDF file
    """
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()
        
        # Reset file pointer for future reads
        uploaded_file.seek(0)
        return text
    except Exception as e:
        print(f"Error reading PDF: {str(e)}")
        return None

def create_download_data(data):
    """
    Convert extracted data to CSV format for downloading
    """
    if not data:
        return ""
    
    # Create DataFrame from the data
    df = pd.DataFrame(data)
    
    # Ensure all metadata columns are present
    metadata_columns = ["file_name", "payer", "plan", "year", "line_of_business", 
                       "code", "code_type", "description", "timestamp"]
    
    for col in metadata_columns:
        if col not in df.columns:
            df[col] = ""
    
    # Generate the CSV
    return df.to_csv(index=False)