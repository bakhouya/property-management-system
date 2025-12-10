


# =============================================================================
# Categories type Validation Rules
# =============================================================================
CATEGORY_TYPE_RULES = {
    "title": ["required", "unique", "min:2", "max:200", "no_html"],
    "description": [ "min:3", "max:500", "no_html"],
    "image": ["file", "size:2", "extensions:jpg,jpeg,png,gif"],    
}
# =============================================================================



# =============================================================================
# main categoriies Validation Rules
# =============================================================================
MAIN_CATEGORY_RULES = {
    "title": ["required", "unique", "min:2", "max:200", "no_html"],
    "description": [ "min:4", "max:500", "no_html"],
    "image": ["file", "size:2", "extensions:jpg,jpeg,png,gif"],    
}
# =============================================================================


# =============================================================================
# sub categories Validation Rules
# =============================================================================
SUB_CATEGORY_RULES = {
    "title": ["required", "unique", "min:2", "max:200", "no_html"],
    "description": [ "min:4", "max:500", "no_html"],
    "main_id": ["required", "no_html"],
    "image": ["file", "size:2", "extensions:jpg,jpeg,png,gif"],    
}
# =============================================================================