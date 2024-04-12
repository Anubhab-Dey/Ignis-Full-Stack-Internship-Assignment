from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Event


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        # Create the user and hash their password
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=make_password(validated_data["password"]),
        )
        user.save()
        Token.objects.create(user=user)  # Generate a token for the new user
        return user


class EventSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        source="user.username"
    )  # Display the username of the user who created the event

    class Meta:
        model = Event
        fields = (
            "id",
            "user",
            "event_name",
            "date",
            "time",
            "location",
            "image",
            "is_liked",
        )

    def create(self, validated_data):
        # Automatically set the user to the request user when creating an event
        event = Event.objects.create(**validated_data)
        return event
