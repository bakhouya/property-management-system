


# ========================================================================================= 
# if the new value is a new uploaded file
# ========================================================================================= 
def is_new_file(new_file, old_file):
    if not new_file:
        return False
    from django.core.files.uploadedfile import UploadedFile
    return isinstance(new_file, UploadedFile)
# ========================================================================================= 

# ========================================================================================= 
# safely delete a file field
# ========================================================================================= 
def safe_delete_file(file_field):
    if file_field and hasattr(file_field, "delete"):
        try:
            file_field.delete(save=False)
        except:
            pass

# ========================================================================================= 

# ========================================================================================= 
# handle file update logic
# ========================================================================================= 
def handle_file_update(new_file, old_file):
    if is_new_file(new_file, old_file) and old_file:
        safe_delete_file(old_file)
# ========================================================================================= 





