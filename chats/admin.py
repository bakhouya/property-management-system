from django.contrib import admin
from .models import Conversation, Message, ImageMessage

# ========================================================
#  register Conversation, Message, ImageMessage Models
# ========================================================
admin.site.register(Conversation)
admin.site.register(Message)
admin.site.register(ImageMessage)
# ========================================================
