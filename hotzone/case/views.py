from case.serializers import CaseSerializer, CaseLocationSerializer, CaseLocationListSerializer
from case.models import Case, CaseLocation
from location.serializers import LocationSerializer
from location.models import Location

from rest_framework.generics import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from sklearn.cluster import DBSCAN
import numpy as np
import datetime
import requests
import math


class ClusterList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def custom_metric(self, q, p, space_eps, time_eps):
        dist = 0
        for i in range(2):
            dist += (q[i] - p[i])**2
        spatial_dist = math.sqrt(dist)
        time_dist = abs(q[2]-p[2])

        if time_dist/time_eps <= 1 and spatial_dist/space_eps <= 1 and p[3] != q[3]:
            return 1
        else:
            return 2

    def cluster(self, vector_4d, distance, time, minimum_cluster):
        clusters = {}
        params = {"space_eps": distance, "time_eps": time}
        db = DBSCAN(eps=10, min_samples=minimum_cluster-1, metric=self.custom_metric, metric_params=params).fit_predict(vector_4d)

        unique_labels = set(db)
        total_clusters = len(unique_labels) if -1 not in unique_labels else len(unique_labels) -1
        total_noise = list(db).count(-1)

        clusters['total_clusters'] = total_clusters
        clusters['total_unclustered'] = total_noise
        clusters['clusters'] = []

        for k in unique_labels:
            if k != -1:
                cluster = {}
                labels_k = db == k
                cluster_k = vector_4d[labels_k]

                cluster['size'] = len(cluster_k)
                cluster['cluster'] = k
                cluster['cluster_list'] = []

                for pt in cluster_k:
                    cluster['cluster_list'].append({'x': pt[0], 'y': pt[1], 'day': pt[2], 'caseNo': pt[3]})

                clusters['clusters'].append(cluster)
        
        return clusters

    def get(self, request):
        locationForCases = CaseLocation.objects.all()
        clusterArray = []
        
        for locationForCase in locationForCases:
            days = (locationForCase.date_from - datetime.date(2020,1,1)).days
            clusterArray.append([locationForCase.location.x_coord, locationForCase.location.y_coord, days, locationForCase.case.case_number])
        
        npArray = np.array(clusterArray)
        D = int(request.GET['distance'] or 200)
        T = int(request.GET['time'] or 3)
        C = int(request.GET['size'] or 2)
                    
        cluster = self.cluster(npArray, D, T, C)

        return Response(cluster)


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

