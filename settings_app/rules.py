


# =============================================================================
# Platform settings Validation Rules
# =============================================================================
PLATFORM_RULES = {
    "title": ["required", "min:3", "max:255", "no_html"],
    "description": ["required", "min:10", "max:2000", "no_html"],

    "timezone": ["required", "min:2", "max:25", "no_html"],
    "currency": ["required", "min:2", "max:10", "no_html"],
    "currency_symbol": ["required", "min:1", "max:10", "no_html"],

    "dark_logo": ["file", 'max:2MB', "size:1048576", "extensions:jpg,jpeg,png,gif"],
    "light_logo": ["file", 'max:2MB', "size:1048576", "extensions:jpg,jpeg,png,gif"],    
}
# =============================================================================
# 
# 
# 
# =============================================================================
# socail media Validation Rules
# =============================================================================
MEDIA_RULES = {
    "facebook": ["url", "min:3", "max:255", "no_html"],
    "facebook": ["url", "min:3", "max:255", "no_html"],
    "facebook": ["url", "min:3", "max:255", "no_html"],
    "facebook": ["url", "min:3", "max:255", "no_html"],
    "facebook": ["url", "min:3", "max:255", "no_html"],
    "facebook": ["url", "min:3", "max:255", "no_html"],
    "facebook": ["url", "min:3", "max:255", "no_html"],
    "facebook": ["url", "min:3", "max:255", "no_html"],
    "facebook": ["url", "min:3", "max:255", "no_html"],  
}
# =============================================================================
# 
# 
# 
# =============================================================================
# seo settings Validation Rules
# =============================================================================
SEO_RULES = {
    "title": ["min:3", "max:255", "no_html"],
    "description": ["min:3", "max:2000", "no_html"],
    "keywords": ["min:3", "max:255", "no_html"],
    "google_analytics_id": ["min:3", "max:255", "no_html"], 
    "facebook_pixel_id": ["min:3", "max:255", "no_html"], 
    "tiktok_pixel_id": ["min:3", "max:255", "no_html"], 
}
# =============================================================================
# 
# 
# 
# =============================================================================
# security settings Validation Rules
# =============================================================================
SECURITY_RULES = {
    "allowed_cors": ["min:100", "url", "no_html"],
}
# =============================================================================
# 
# 
# 
# =============================================================================
# city Validation Rules
# =============================================================================
CITY_RULES = {
    "name": ["unique", "max:100", "min:2", "no_html"],
}
# =============================================================================
# 
# 
# 
# =============================================================================
# User settings Validation Rules
# =============================================================================
USER_SETTINGS_RULES = {
    "number_whatsapp": ["min:8", "max:13", "no_html"],
    "number_vocal": ["min:8", "max:13", "no_html"],
}
# =============================================================================