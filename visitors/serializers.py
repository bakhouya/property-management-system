
from rest_framework import serializers
from .models import Visitor, Visit



# ========================================================================

# ========================================================================
class VisitorSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Visitor 
        fields = '__all__'
# ========================================================================
# 
# 
# 
# 
# ========================================================================
# VisitSerializer
# This serializer is responsible for converting the Visit form data to JSON format.
# It is used when you need to display details of each visit made by the visitor.
# Fields: All fields in the Visit form.
# ========================================================================
class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = '__all__'
# ========================================================================
# 
# 
# 
# 
# ========================================================================
# VisitorDetailSerializer
# This serializer is designed to display visitor details, including all their visits.
# Fields:
    # - Visitor's basic data: id, ip_address, browser_agent, browser, device_type, country, first_visit, last_visit
    # - visits: A list of all the visitor's visits (structured using VisitSerializer)
    # - total_visits: The total number of visits for the visitor
# Method get_total_visits: Calculates the number of visits associated with this visitor.
# ========================================================================
class VisitorDetailSerializer(serializers.ModelSerializer):
    visits = VisitSerializer(many=True, read_only=True)  
    total_visits = serializers.SerializerMethodField()

    class Meta:
        model = Visitor
        fields = [
            'id', 'ip_address', 'browser_agent', 'browser',  'device_type',
            'country', 'first_visit', 'last_visit', 
            'visits', 'total_visits'
        ]

    def get_total_visits(self, obj):
        return obj.visits.count()
# ========================================================================
