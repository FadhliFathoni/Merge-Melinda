from Account.models import Account
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["email","password"]