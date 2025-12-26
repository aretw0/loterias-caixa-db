import re

def clean_currency(value) -> float:
    """
    Converts a currency string (e.g., 'R$ 1.234,56') or numeric value to a float.
    Handles 'R$', dots for thousands, and commas for decimals.
    Returns 0.0 if the value is empty, None, or cannot be converted.
    """
    if value is None or value == "":
        return 0.0
    
    if isinstance(value, (int, float)):
        return float(value)
        
    # Convert to string just in case
    s_value = str(value).strip()
    
    if not s_value:
        return 0.0

    # Remove 'R$' and whitespace
    s_value = s_value.replace("R$", "").strip()
    
    # Remove dots (thousands separators)
    s_value = s_value.replace(".", "")
    
    # Replace comma with dot (decimal separator)
    s_value = s_value.replace(",", ".")
    
    try:
        return float(s_value)
    except ValueError:
        return 0.0
