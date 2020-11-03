from rest_framework import serializers
from case.models import Case, CaseLocation


class CaseSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    patient_id_number = serializers.SerializerMethodField()
    patient_birth = serializers.SerializerMethodField()
    virus_name = serializers.SerializerMethodField()
    disease = serializers.SerializerMethodField()
    max_infectious_period = serializers.SerializerMethodField()

    class Meta:
        model = Case
        fields = ['case_number', 'date_confirmed', 'local_or_imported', 
        'patient_name', 'patient_id_number', 'patient_birth', 'virus_name', 'disease', 
        'max_infectious_period']
    
    def get_patient_name(self, obj):
        return obj.patient.name

    def get_patient_id_number(self, obj):
        return obj.patient.identity_document_number

    def get_patient_birth(self, obj):
        return obj.patient.date_of_birth

    def get_virus_name(self, obj):
        return obj.virus.virus_name

    def get_disease(self, obj):
        return obj.virus.disease

    def get_max_infectious_period(self, obj):
        return obj.virus.max_infectious_period


class CaseLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseLocation
        fields = ['id', 'case', 'location', 'date_from', 'date_to', 'category']

        
class CaseLocationListSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    x_coord = serializers.SerializerMethodField()
    y_coord = serializers.SerializerMethodField()

    class Meta:
        model = CaseLocation
        fields = ['id', 'location', 'address', 'x_coord', 'y_coord', 'date_from', 'date_to', 'category']
    
    def get_location(self, obj):
        return obj.location.location
    
    def get_address(self, obj):
        return obj.location.address
    
    def get_x_coord(self, obj):
        return obj.location.x_coord
    
    def get_y_coord(self, obj):
        return obj.location.y_coord

