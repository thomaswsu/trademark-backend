from django.shortcuts import render
from django.contrib.auth.models import User, AnonymousUser

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from trademark_backend.serializers import UserSerializer

# Create your views here.

class ExampleView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        content = {'message': 'Authenticated users can see this.'}
        return Response(content)

class AuthenticatedUserView(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self, request):
        content = {
            'id': request.user.id,
            'email': request.user.email,
            'username': request.user.username,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }                                                                                                                                                                                                                                                                                                                                                   
        return Response(content)

class AnonymousUserView(APIView):
    def post(self, request):
        if not isinstance(request.user, AnonymousUser):
            content = {'message': 'Logged in users are unable to create other accounts.'}                                                                                                                                                                                                                                                                                                                                                   
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        serialized = UserSerializer(data=request.data)
        if serialized.is_valid():
            user = User.objects.create(
                email = serialized.validated_data.get('email'),
                username = serialized.validated_data.get('username'),
                first_name = serialized.validated_data.get('first_name'),
                last_name = serialized.validated_data.get('last_name'),
            )
            user.set_password(str(serialized.validated_data.get('password')))
            user.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
