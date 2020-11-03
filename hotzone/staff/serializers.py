from rest_framework import serializers
from staff.models import Staff


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['id', 'username', 'password', 'CHP_staff_number', 'first_name', 'last_name', 'email_address']