


# =============================================================================
# User Validation Rules
# =============================================================================
USER_RULES = {
    "username": ["required", "unique", "min:3", "max:20", "no_html"],
    "phone": ["required", "unique", "min:10", "max:13", "no_html"],
    "email": ["required", "email", "unique", "max:100", "no_html"],

    "first_name": ["required", "min:2", "max:30", "no_html"],
    "last_name": ["required", "min:2", "max:30", "no_html"],

    "bio": ["max:500", "no_html"],
    "avatar": ["file", "size:2", "extensions:jpg,jpeg,png,gif"],
    
}
# =============================================================================