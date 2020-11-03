from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from case import views


urlpatterns = [
    path('', views.CaseList.as_view(), name='case-list'),
    path('<str:pk>', views.CaseDetail.as_view(), name='case-detail'),
    path('<str:pk>/locations', views.CaseLocationHistory.as_view(), name='case-locations'),
]

urlpatterns = format_suffix_patterns(urlpatterns)