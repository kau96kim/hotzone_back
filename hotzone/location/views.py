from rest_framework.response import Response
from rest_framework.views import APIView
from location.models import Location
from rest_framework import status
import requests


class SearchList(APIView):

    def get(self, request):
        geoDataList = requests.get('https://geodata.gov.hk/gs/api/v1.0.0/locationSearch', params=request.GET)
        if geoDataList.status_code == 200:
            return Response(geoDataList.json())
        return Response(status=status.HTTP_400_BAD_REQUEST)