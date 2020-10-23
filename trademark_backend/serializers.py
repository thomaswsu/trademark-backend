from rest_framework import serializers
from django.contrib.auth import get_user_model

from trademark_api.models import Order

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'password']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['ticker', 'action_type', 'order_type', 'execution_price', 'quantity', 'time_in_force']
