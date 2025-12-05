
import uuid
from django.db import models


# ============================================================================================
# A form representing visitors accessing the platform.
# Used to store basic information for each visitor.
# This form is essential for monitoring platform traffic and analyzing statistics.
# It can be used to generate accurate reports on platform usage and visitor behavior.
# ============================================================================================
class Visitor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key             = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    ip_address      = models.GenericIPAddressField(protocol="both", unpack_ipv4=True)
    device_type     = models.CharField(max_length=500, null=True, blank=True)
    browser_agent   = models.CharField(max_length=500, null=True, blank=True)
    browser         = models.CharField(max_length=100, null=True, blank=True)
    country         = models.CharField(max_length=100, null=True, blank=True)
    first_visit     = models.DateTimeField(auto_now_add=True)
    last_visit      = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return f"Visitor: {self.ip_address} ({self.key})"
# ============================================================================================
# 
# 
# 
# 
# ============================================================================================
# A form representing visitor visits to the platform.
# It stores each visitor's visit, specifying that each visitor can make only one visit every 24 hours.
# This form is used to track daily visitor activity and analyze interaction patterns with the platform.
# ============================================================================================
class Visit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE,  related_name="visits")
    page_url = models.URLField(max_length=500)
    page_title = models.CharField(max_length=255, null=True, blank=True)
    referrer = models.URLField(max_length=500, null=True, blank=True)
    visit_time = models.DateTimeField(auto_now_add=True)  
    visit_date = models.DateField(auto_now_add=True)    

    def __str__(self):
        return f"Visit by {self.visitor.browser} on {self.visit_date}"
# ============================================================================================


