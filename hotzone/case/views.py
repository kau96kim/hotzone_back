from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from case.serializers import CaseSerializer, CaseLocationSerializer, CaseLocationListSerializer
from case.models import Case, CaseLocation
from location.serializers import LocationSerializer
from location.models import Location
import requests


import numpy as np
from sklearn.cluster import DBSCAN
import math
import datetime


class CaseCluster(APIView):

    def get(self, request):
        locations = CaseLocation.objects.all()
        locationArray = []

        # not sure about getting D, T, C from user
        D = request.data['d']
        T = request.data['t']
        C = request.data['c']
        
        for location in locations:
            # not sure whether the day is calculated correctly
            day = location.date_from - datetime.date(2020,1,1)
            # not sure whether i access the data correctly            
            locationArray.append([location.location.x_coord, location.location.y_coord, day, location.case.case_number])
            
        npArray = np.array(locationArray)

        # clustering functions
        def custom_metric(q, p, space_eps, time_eps):
            dist = 0
            for i in range(2):
                dist += (q[i] - p[i])**2
            spatial_dist = math.sqrt(dist)

            time_dist = math.sqrt((q[2]-p[2])**2)

            if time_dist/time_eps <= 1 and spatial_dist/space_eps <= 1 and p[3] != q[3]:
                return 1
            else:
                return 2


        def cluster(vector_4d, distance, time, minimum_cluster):
            params = {"space_eps": distance, "time_eps": time}
            db = DBSCAN(eps=1, min_samples=minimum_cluster-1, metric=custom_metric, metric_params=params).fit_predict(vector_4d)

            unique_labels = set(db)
            total_clusters = len(unique_labels) if -1 not in unique_labels else len(unique_labels) -1
            total_noise = list(db).count(-1)

            # not sure what should I return here
            """
            for k in unique_labels:
                if k != -1:

                    labels_k = db == k
                    cluster_k = vector_4d[labels_k]

                    print("Cluster", k, " size:", len(cluster_k))

                    for pt in cluster_k:
                        print("(x:{}, y:{}, day:{}, caseNo:{})".format(pt[0], pt[1], pt[2], pt[3]))

                    print()
            """

        cluster(npArray, D, T, C)

      

class CaseList(APIView):

    def get(self, request):
        cases = Case.objects.all()
        serializer = CaseSerializer(cases, many=True)  
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

