from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Event


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=make_password(validated_data["password"]),
        )
        Token.objects.create(user=user)  # Create a token for the new user
        return user


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id",
            "user",
            "event_name",
            "date",
            "time",
            "location",
            "image",
            "is_liked",
        ]
        read_only_fields = ("user",)

    def create(self, validated_data):
        # Add the user from the request when creating an event
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
