from django.shortcuts import render
from django.contrib.auth.models import AnonymousUser

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from trademark_backend.serializers import UserSerializer

from django.contrib.auth import get_user_model

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
            # TODO: Decide if this should be included in user data endpoint
            # 'alpaca_key_id': request.user.alpaca_key_id,
            # 'alpaca_secret_key': request.user.alpaca_secret_key
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
                first_name = serialized.validated_data.get('first_name'),
                last_name = serialized.validated_data.get('last_name'),
                alpaca_key_id = serialized.validated_data.get('alpaca_key_id'),
                alpaca_secret_key = serialized.validated_data.get('alpaca_secret_key'),
            )
            user.set_password(str(serialized.validated_data.get('password')))
            user.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
