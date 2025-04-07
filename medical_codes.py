import re
from datetime import datetime
from code_descriptions import get_code_description

# Regular expressions for different code types
CPT_PATTERN = r'\b\d{5}\b'  # Basic 5-digit CPT codes
HCPCS_PATTERN = r'\b[A-Z]\d{4}\b'  # HCPCS codes (e.g., G0101)
PLA_PATTERN = r'\b\d{4}[A-Z]\b'  # PLA codes (e.g., 0001U)

def extract_cpt_codes(text):
    """Extract CPT codes from text"""
    if not text:
        return []
    
    # Find all 5-digit numbers that could be CPT codes
    cpt_codes = re.findall(CPT_PATTERN, text)
    
    # Create dictionary for each extracted code
    results = []
    for code in set(cpt_codes):  # Using set to remove duplicates
        results.append({
            "code": code,
            "code_type": "CPT",
            "description": get_code_description(code, "CPT"),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    return results

def extract_hcpcs_codes(text):
    """Extract HCPCS codes from text"""
    if not text:
        return []
    
    # Find all HCPCS codes (letter followed by 4 digits)
    hcpcs_codes = re.findall(HCPCS_PATTERN, text)
    
    # Create dictionary for each extracted code
    results = []
    for code in set(hcpcs_codes):  # Using set to remove duplicates
        results.append({
            "code": code,
            "code_type": "HCPCS",
            "description": get_code_description(code, "HCPCS"),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    return results

def extract_pla_codes(text):
    """Extract PLA codes from text"""
    if not text:
        return []
    
    # Find all PLA codes (4 digits followed by a letter)
    pla_codes = re.findall(PLA_PATTERN, text)
    
    # Create dictionary for each extracted code
    results = []
    for code in set(pla_codes):  # Using set to remove duplicates
        results.append({
            "code": code,
            "code_type": "PLA",
            "description": get_code_description(code, "PLA"),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    return results

def extract_all_codes(text):
    """Extract all types of medical codes from text"""
    if not text:
        return []
    
    # Extract all code types
    cpt_results = extract_cpt_codes(text)
    hcpcs_results = extract_hcpcs_codes(text)
    pla_results = extract_pla_codes(text)
    
    # Combine all results
    all_results = cpt_results + hcpcs_results + pla_results
    
    return all_results