from rest_framework import serializers
from django.contrib.auth import get_user_model


from .models import Location, LoginHistorie

User = get_user_model()

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'phone_no', 'profile_picture']

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['user', 'latitude', 'longitude','timestamp','date']
        read_only_fields = ('timestamp', 'date',)

    def create(self, validated_data):

        loc = Location.objects.create(**validated_data)
        loc.save()
        return loc

class LoginHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginHistorie
        fields = ['user', 'session_type', 'date', 'timestamp']

        read_only_fields = ('date', 'timestamp',)

    def create(self, validated_data):
        hist = LoginHistorie.objects.create(
            user= validated_data['user'],
            session_type= validated_data['session_type']
        )

        hist.save()

        return hist


