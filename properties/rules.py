


# =============================================================================
# Categories type Validation Rules
# =============================================================================
PROPERTY_RULES = {
    "title": ["required", "min:2", "max:200", "no_html"],
    "description": [ "min:3", "max:2000", "no_html"],
    "category_type": ["required", "no_html"],
    "main_category": ["required",  "no_html"],
    "sub_category": ["required", "no_html"],
    "city": ["required", "no_html"],
    "address": ["min:2", "max:255", "no_html"],
    "area": ["required", "no_html"],
    "price": ["required", "no_html"],
    "price_type": ["required", "no_html"],   
}
# =============================================================================

# =============================================================================
# Categories type Validation Rules
# =============================================================================
PRICETYPE_RULES = {
    "title": ["required", "min:2", "max:200", "no_html"],
    "description": ["required", "min:3", "max:2000", "no_html"],  
}
# =============================================================================

# =============================================================================
# Categories type Validation Rules
# =============================================================================
COMMENT_RULES = {
    "comment": ["required", "min:2", "no_html"],  
}
# =============================================================================