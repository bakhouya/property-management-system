# ==========================================================================================
#  imports
# ==========================================================================================
import re
import os
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, URLValidator
import bleach
# ==========================================================================================

# ==========================================================================================
# validator class
# ==========================================================================================
class DynamicValidator:
    def __init__(self, model, instance=None):
        self.model = model
        self.instance = instance

    # ==========================================================================================
    # method handle clean data : delete tags HTML , script, attr
    # ==========================================================================================
    def _clean_no_html(self, value):
        if not value:
            return value
        
        if hasattr(value, 'size'):
            return value
               
        original_value = str(value)
        cleaned = bleach.clean(original_value, tags=[], attributes={}, strip=True, strip_comments=True)
        cleaned = re.sub(r'javascript:', '', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'on\w+\s*=', '', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'data-', '', cleaned, flags=re.IGNORECASE)
        
        return cleaned.strip()
    # ==========================================================================================
    # 
    # 
    # 
    # 
    # ==========================================================================================
    # handle all method validations
    # ==========================================================================================
    def validate(self, data, rules_config, is_update=False):
        errors = {}
        cleaned_data = data.copy()
        
        # Clean all data (HTML sanitization)
        for field_name, rules in rules_config.items():
            value = data.get(field_name)

            if value and "no_html" in rules:
                cleaned_value = self._clean_no_html(value)
                cleaned_data[field_name] = cleaned_value

                if cleaned_value == "" and "required" in rules and not is_update:
                    errors.setdefault(field_name, []).append("This field is required and cannot contain only HTML code.")
        

        # Validation with cleaned data
        for field_name, rules in rules_config.items():
            value = cleaned_data.get(field_name)

            # Required check Validator & call method handle required 
            required_error = self._check_required(field_name, value, rules, data, is_update)
            if required_error:
                errors.setdefault(field_name, []).append(required_error)
                continue  

            # Skip empty values
            if value in [None, "", []]:
                continue
                
            field_errors = []

            for rule in rules:
                if rule in ["no_html", "required"]: 
                    continue
                    
                try:
                    if rule.startswith("max:"):
                        self._validate_max(value, rule)
                    elif rule.startswith("min:"):
                        self._validate_min(value, rule)
                    elif rule == "email":
                        self._validate_email(value)
                    elif rule == "url":
                        self._validate_url(value)
                    elif rule == "file":
                        self._validate_file(value)
                    elif rule.startswith("size:"):
                        self._validate_file_size(value, rule)
                    elif rule.startswith("extensions:"):
                        self._validate_file_extensions(value, rule)
                    elif rule == "unique":
                        self._validate_unique(field_name, value)
                        
                except ValidationError as e:
                    field_errors.extend(e.messages)
            
            if field_errors:
                errors[field_name] = field_errors
        
        if errors:
            raise ValidationError(errors)
        
        return cleaned_data
    # ==========================================================================================





    # ==========================================================================================
    # handle check required fields
    # ==========================================================================================
    def _check_required(self, field_name, value, rules, data, is_update):
        if "required" in rules:
            if is_update:
                if field_name in data and value in [None, "", []]:
                    return "This field is required."
            else:
                if value in [None, "", []]:
                    return "This field is required"
        return None
    # ==========================================================================================
    # 
    # 
    # 
    # 
    # ==========================================================================================
    # handle max lenght and max size file 
    # ==========================================================================================
    def _validate_max(self, value, rule):
        max_val = int(rule.split(":")[1])
        if hasattr(value, 'size'): 
            if value.size > max_val * 1024:  
                raise ValidationError(f"File size must not exceed {max_val} KB.")
        elif len(str(value)) > max_val: 
            raise ValidationError(f"Value must not exceed {max_val} characters.")
    # ==========================================================================================
    # 
    # 
    # 
    # 
    # ==========================================================================================
    # handle min lenght fields
    # ==========================================================================================
    def _validate_min(self, value, rule):
        min_val = int(rule.split(":")[1])
        if len(str(value)) < min_val:
            raise ValidationError(f"Value must be at least {min_val} characters.")
    # ==========================================================================================
    # 
    # 
    # 
    # 
    # ==========================================================================================
    # ==========================================================================================
    def _validate_email(self, value):
        validator = EmailValidator(message="Enter a valid email address.")
        validator(value)
    # ==========================================================================================
    # 
    # 
    # 
    # 
    # ==========================================================================================
    # handle URL field check
    # ==========================================================================================
    def _validate_url(self, value):
        validator = URLValidator(message="Enter a valid URL.")
        validator(value)
    # ==========================================================================================
    # 
    # 
    # 
    # 
    # ==========================================================================================
    #  handle valid file
    # ==========================================================================================
    def _validate_file(self, value):
        if not hasattr(value, 'size'):
            raise ValidationError("Must upload a valid file.")
    # ==========================================================================================
    # 
    # 
    # 
    # 
    # ==========================================================================================
    # ==========================================================================================
    def _validate_file_size(self, value, rule):
        max_size_mb = int(rule.split(":")[1])
        max_size = max_size_mb * 1024 * 1024
        if value.size > max_size:
            raise ValidationError(f"File size must not exceed {max_size_mb} MB.")
    # ==========================================================================================
    # 
    # 
    # 
    # 
    # ==========================================================================================
    # handle file extensions
    # ==========================================================================================
    def _validate_file_extensions(self, value, rule):
        allowed_exts = rule.split(":")[1].split(",")
        ext = os.path.splitext(value.name)[1][1:].lower()
        if ext not in allowed_exts:
            raise ValidationError(f"File type not allowed. Allowed types: {', '.join(allowed_exts)}")
    # ==========================================================================================
    # 
    # 
    # 
    # 
    # ==========================================================================================
    # handle unique fields
    # ==========================================================================================
    def _validate_unique(self, field_name, value):
        if self.instance:
            qs = self.model.objects.filter(**{field_name: value}).exclude(pk=self.instance.pk)
        else:
            qs = self.model.objects.filter(**{field_name: value})
            
        if qs.exists():
            raise ValidationError(f"This {field_name} already exists.")
    # ==========================================================================================
    


