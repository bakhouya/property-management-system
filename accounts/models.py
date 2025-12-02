
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from visitors.models import Visitor



# ============================================================================================
# A model representing users within the system.
# Allows storing basic information for each user and supports login using a phone number.
# Contains additional fields necessary for customizing the account according to user type 
# ============================================================================================
class User(AbstractUser):
    # Key:  Unique Field by UUID as primary key - better security
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Required unique fields for authentication
    email = models.EmailField(unique=True, blank=True)
    phone  = models.CharField(unique=True, max_length=20)
    # User type for role-based permissions
    ACCOUNT_TYPE_CHOICES  = [('personal', 'Personal'), ('admin', 'Administrator'),]
    account_type  = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES, default='personal')
    # Avatar User For profile
    avatar = models.ImageField(upload_to="accounts/avatars/", blank=True, null=True)
    # security field if this = True mean can logged
    is_blocked = models.BooleanField(default=False)
    visitor = models.ForeignKey(Visitor, on_delete=models.SET_NULL, null=True, blank=True, related_name="users")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["email", "username"]

    class Meta:
        verbose_name = "Users"
        verbose_name_plural = "Users"
        ordering = ['-created_at'] 
        permissions = [
            ("can_list_users", "Can view list users"),
            ("can_activate_user", "Can activate user"),
            ("can_block_user", "Can block user"),
            ("can_view_user_profile", "Can view user profile"),
            ("can_edit_user_profile", "Can edit user profile"),
        ]

    def __str__(self):
        return self.username
    
    def toggle_blocked(self):
        self.is_blocked = not self.is_blocked
        self.save()
        return self.is_blocked
# ============================================================================================




