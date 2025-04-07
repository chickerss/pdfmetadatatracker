import re

# Embedded CPT/HCPCS Lookup Dictionary
CODE_LOOKUP = {
    "00100-01999": {
        "category": "Anesthesia",
        "subcategory": "General",
        "description": "Anesthesia for surgical procedures"
    },
    "10000-19999": {
        "category": "Surgery",
        "subcategory": "Integumentary System",
        "description": "Procedures on the skin and subcutaneous tissue"
    },
    "20000-29999": {
        "category": "Surgery",
        "subcategory": "Musculoskeletal System",
        "description": "Procedures on bones, joints, and muscles"
    },
    "30000-39999": {
        "category": "Surgery",
        "subcategory": "Respiratory System",
        "description": "Procedures on nose, sinuses, larynx, trachea, bronchi, and lungs"
    },
    "40000-49999": {
        "category": "Surgery",
        "subcategory": "Digestive System",
        "description": "Procedures on digestive organs"
    },
    "50000-59999": {
        "category": "Surgery",
        "subcategory": "Urinary and Reproductive Systems",
        "description": "Procedures on kidney, ureter, bladder, and reproductive organs"
    },
    "60000-69999": {
        "category": "Surgery",
        "subcategory": "Endocrine System",
        "description": "Procedures on endocrine glands"
    },
    "70010-79999": {
        "category": "Radiology",
        "subcategory": "Diagnostic Imaging",
        "description": "Radiologic exam and imaging"
    },
    "80000-89999": {
        "category": "Pathology and Laboratory",
        "subcategory": "Lab Tests",
        "description": "Laboratory and pathology procedures"
    },
    "90000-99999": {
        "category": "Evaluation and Management",
        "subcategory": "Office Visits",
        "description": "Medical visit and consultation services"
    },
    "A0000-A0999": {
        "category": "HCPCS Level II",
        "subcategory": "Transportation Services",
        "description": "Ambulance and medical transport"
    },
    "B0000-B9999": {
        "category": "HCPCS Level II",
        "subcategory": "Enteral and Parenteral Therapy",
        "description": "Enteral and parenteral therapy"
    },
    "C0000-C9999": {
        "category": "HCPCS Level II",
        "subcategory": "Outpatient PPS",
        "description": "Outpatient prospective payment system"
    },
    "D0000-D9999": {
        "category": "HCPCS Level II",
        "subcategory": "Dental Procedures",
        "description": "Dental procedures"
    },
    "E0000-E9999": {
        "category": "HCPCS Level II",
        "subcategory": "Durable Medical Equipment",
        "description": "Durable medical equipment"
    },
    "G0000-G9999": {
        "category": "HCPCS Level II",
        "subcategory": "Procedures/Professional Services",
        "description": "Temporary procedures and professional services"
    },
    "H0000-H9999": {
        "category": "HCPCS Level II",
        "subcategory": "Behavioral Health",
        "description": "Alcohol and drug treatment services"
    },
    "J0000-J9999": {
        "category": "HCPCS Level II",
        "subcategory": "Drugs",
        "description": "Drugs administered other than oral method"
    },
    "K0000-K9999": {
        "category": "HCPCS Level II",
        "subcategory": "Temporary Codes",
        "description": "Temporary codes for DME and supplies"
    },
    "L0000-L9999": {
        "category": "HCPCS Level II",
        "subcategory": "Orthotic/Prosthetic",
        "description": "Orthotic and prosthetic procedures"
    },
    "M0000-M9999": {
        "category": "HCPCS Level II",
        "subcategory": "Medical Services",
        "description": "Medical services"
    },
    "P0000-P9999": {
        "category": "HCPCS Level II",
        "subcategory": "Pathology/Laboratory",
        "description": "Pathology and laboratory services"
    },
    "Q0000-Q9999": {
        "category": "HCPCS Level II",
        "subcategory": "Temporary Codes",
        "description": "Temporary codes"
    },
    "R0000-R9999": {
        "category": "HCPCS Level II",
        "subcategory": "Diagnostic Radiology",
        "description": "Diagnostic radiology services"
    },
    "S0000-S9999": {
        "category": "HCPCS Level II",
        "subcategory": "Private Payer",
        "description": "Temporary national codes (non-Medicare)"
    },
    "T0000-T9999": {
        "category": "HCPCS Level II",
        "subcategory": "State Medicaid",
        "description": "State Medicaid agency codes"
    },
    "V0000-V9999": {
        "category": "HCPCS Level II",
        "subcategory": "Vision Services",
        "description": "Vision and hearing services"
    },
    "0001U-9999U": {
        "category": "PLA Codes",
        "subcategory": "Proprietary Laboratory Analyses",
        "description": "Proprietary laboratory analyses"
    }
}

# Simple cache for code descriptions to avoid repeating lookups
code_description_cache = {}

def get_code_info(code):
    """
    Get detailed information about a medical code from the lookup dictionary.
    """
    code = str(code).upper()
    
    # First check for exact matches (future enhancement)
    # Then check for range matches
    for code_range, info in CODE_LOOKUP.items():
        start, end = code_range.split("-")
        
        if re.match(r"[A-Z]", code):  # Alphanumeric HCPCS or PLA
            if start <= code <= end:
                return info
        else:  # Numeric CPT
            try:
                if int(start) <= int(code) <= int(end):
                    return info
            except ValueError:
                continue
                
    return {
        "category": "Unknown",
        "subcategory": "Unknown",
        "description": "Not found in lookup"
    }

def get_code_description(code, code_type):
    """
    Get the description for a medical code using the lookup system.
    """
    # Check if we already have this code's description in our cache
    cache_key = f"{code_type}_{code}"
    if cache_key in code_description_cache:
        return code_description_cache[cache_key]
    
    # Get code info from lookup
    info = get_code_info(code)
    
    # Format the description using the code info
    description = f"{info['category']} | {info['subcategory']} | {info['description']}"
    
    # Cache the result
    code_description_cache[cache_key] = description
    
    return description

def format_code_with_description(code, code_type, description=None):
    """
    Format a code with its description for display or reporting.
    """
    if description is None:
        description = get_code_description(code, code_type)
    
    return f"{code} ({code_type}): {description}"