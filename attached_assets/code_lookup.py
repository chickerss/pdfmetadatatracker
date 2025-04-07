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
    "70010-79999": {
        "category": "Radiology",
        "subcategory": "Diagnostic Imaging",
        "description": "Radiologic exam and imaging"
    },
    "A0000-A0999": {
        "category": "HCPCS Level II",
        "subcategory": "Transportation Services",
        "description": "Ambulance and medical transport"
    },
    # Add more ranges as needed
}

import re

def get_code_info(code):
    code = code.upper()

    for code_range, info in CODE_LOOKUP.items():
        start, end = code_range.split("-")

        if re.match(r"[A-Z]", code):  # Alphanumeric HCPCS
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

# Example use
codes = ["00120", "99213", "A0428"]

for c in codes:
    info = get_code_info(c)
    print(f"Code: {c} => {info['category']} | {info['subcategory']} | {info['description']}")
