from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from staff import models
import uuid

# Create your views here.
class LoginView(APIView):

    def post(self,request,*args,**kwargs):
        user = request.data.get('username')
        pwd = request.data.get('password')

        user_object = models.Staff.objects.filter(username=user,password=pwd).first()
        if not user_object:
            return Response({'code':1000,'error':'wrong username or password'})

        random_string = str(uuid.uuid4())

        user_object.token = random_string
        user_object.save()

        return Response({'code':1001,'data':random_string})
