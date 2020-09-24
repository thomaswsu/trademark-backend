import json

from django.shortcuts import render

from django.core.validators import validate_email

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.password_validation import validate_password, password_changed, get_password_validators

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from trademark_backend.serializers import UserSerializer

User = get_user_model()

# Create your views here.

class ExampleView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        content = {'message': 'Authenticated users can see this.'}
        return Response(content)

class UserView(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self, request):
        content = {
            'id': request.user.id,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }                                                                                                                                                                                                                                                                                                                                                   
        return Response(content, status=status.HTTP_200_OK)
    def patch(self, request):
        body = json.loads(request.body)
        user = User.objects.get(id=request.user.id)
        if 'password' in body and request.user.check_password(body['password']):
            # should consider validation
            if 'new_email' in body:
                try:
                    validate_email(body['new_email'])
                    user.email = body['new_email']
                    user.save()
                except Exception as e:
                    return Response({'new_email': e.messages[0]}, status=status.HTTP_400_BAD_REQUEST)
            if 'new_password' in body:
                try:
                    v = validate_password(password=body['new_password'], user=request.user)
                    user.set_password(str(body['new_password']))
                    user.save()
                    password_changed(password=body['new_password'], user=request.user)
                except Exception as e:
                    return Response({'new_password': e.messages[0]}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': 'User data updated successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'password': 'Incorrect password.'}, status=status.HTTP_401_UNAUTHORIZED)

class AnonymousUserView(APIView):
    def post(self, request):
        if not isinstance(request.user, AnonymousUser):
            content = {'message': 'Logged in users are unable to create other accounts.'}                                                                                                                                                                                                                                                                                                                                                   
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        serialized = UserSerializer(data=request.data)
        if serialized.is_valid():
            user = User.objects.create(
                email = serialized.validated_data.get('email'),
                first_name = serialized.validated_data.get('first_name'),
                last_name = serialized.validated_data.get('last_name'),
            )
            user.set_password(str(serialized.validated_data.get('password')))
            user.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
