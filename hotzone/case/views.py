from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from case.serializers import CaseSerializer, CaseLocationSerializer, CaseLocationListSerializer
from case.models import Case, CaseLocation
from location.serializers import LocationSerializer
from location.models import Location
from staff.models import Staff
import requests


class CaseList(APIView):

    def get(self, request):
        cases = Case.objects.all()
        serializer = CaseSerializer(cases, many=True)

        token = request.query_params.get('token')
        if not token:
            return Response({'code':2000,'error':"please log in"})
        user_object = Staff.objects.filter(token=token).first()
        if not user_object:
            return Response({'code':3000,'error':"invalid token!"})

        return Response(serializer.data)


class CaseDetail(APIView):

    def get_object(self, pk):
        case = get_object_or_404(Case, case_number=pk)
        return case

    def get(self, request, pk):
        case = self.get_object(pk)
        serializer = CaseSerializer(case)
        return Response(serializer.data)


class CaseLocationHistory(APIView):

    def get(self, request, pk):
        locations = CaseLocation.objects.filter(case=pk)
        serializer = CaseLocationListSerializer(locations, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        # Add location Data
        location_data = {
            "location": request.data['location'],
            "address": request.data['address'],
            "x_coord": request.data['x_coord'],
            "y_coord": request.data['y_coord'],
        }
        location_serializer = LocationSerializer(data=location_data)
        location_in_db = Location.objects.filter(location=request.data['location'])

        if not location_in_db:
            if location_serializer.is_valid():
                location_serializer.save()
                location_id = location_serializer.data['id']
            else:
                return Response(location_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            location_id = location_in_db.get().id
            print(location_id)

        # Add Case location visit history Data
        case_locations_data = {
            'case': pk,
            'location': location_id,
            'date_from': request.data['date_from'],
            'date_to': request.data['date_to'],
            'category': request.data['category']
        }
        case_locations_serializer = CaseLocationSerializer(data=case_locations_data)

        if case_locations_serializer.is_valid():
            case_locations_serializer.save()
            return Response(case_locations_serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(case_locations_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
