from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from locations.models import Location

import os
import json
import requests
# Create your views here.

def search(request):
    
    if(request.method=='GET'):
        search= request.GET.get('searchfor')
        results = Location.objects.filter(name=search)
        url='https://geodata.gov.hk/gs/api/v1.0.0/locationSearch?q='+search
        response = requests.get(url=url,headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            Array=json.loads(response.text)
            return render(
                request,
                'results.html',
                {'Array': Array,
                 'results':results}
            )
        else:
            return render(
                request,
                'error.html',
            )

def AddLocation(request):
    data= request.GET.get('index')
    data = data.replace("\'", "\"")
    Array=json.loads(data)
    Location.objects.create(
        name=Array["nameEN"],
        address=Array["addressEN"],
        xcoord=Array["x"],
        ycoord=Array["y"],
    )

    return render(
                request,
                'confirm.html',
            )


class LocationViewAll(ListView):
    template_name = "location_list.html"
    model = Location

class SearchView(TemplateView):
    template_name = "search.html"



