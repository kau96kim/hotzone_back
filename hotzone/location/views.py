from location.serializers import LocationSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from location.models import Location
from rest_framework import status
import requests
import json


class SearchList(APIView):

    def get(self, request):
        geoDataList = requests.get('https://geodata.gov.hk/gs/api/v1.0.0/locationSearch', params=request.GET)
        location_in_db = Location.objects.filter(location__icontains=request.GET['q'])
        location = LocationSerializer(location_in_db, many=True)
        location_list = [d['location'] for d in location.data]
        geo_list = geoDataList.json()
        geo_location = [i for i in geo_list if not (i['nameEN'] in location_list)] 

        def custom_to_dict(location):
            return {
                "location": location['nameEN'],
                "address": location['addressEN'],
                "x_coord": location['x'],
                "y_coord": location['y']
            }
        #custom_list is your list of customs
        geo_location = json.dumps([custom_to_dict(custom) for custom in geo_location])

        if geoDataList.status_code == 200:
            return Response({
                    'location_db': location.data,
                    'location_geo': json.loads(geo_location)
                })
        return Response(status=status.HTTP_400_BAD_REQUEST)