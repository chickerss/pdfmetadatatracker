# Simple cache for code descriptions to avoid repeating lookups
code_description_cache = {}

def get_code_description(code, code_type):
    """
    Get the description for a medical code.
    In a full implementation, this would query a database or API.
    For now, we'll return a placeholder that indicates we need to connect to a real data source.
    """
    # Check if we already have this code's description in our cache
    cache_key = f"{code_type}_{code}"
    if cache_key in code_description_cache:
        return code_description_cache[cache_key]
    
    # In a real implementation, this would query a medical code API or database
    # For now, we'll return a standardized message
    description = f"Description for {code_type} code {code} (connect to code database for full descriptions)"
    
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