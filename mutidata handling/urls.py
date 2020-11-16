from django.urls import path
from locations import views

urlpatterns = [
    path('locations',
        views.LocationViewAll.as_view(),
        name = 'locations'),
    path('',
        views.SearchView.as_view(),
        name = 'HotZone'),
    path('search/',views.search,name='search'),
    path(r'^addLocation/$', views.AddLocation, name="addLocation"),
    ]
