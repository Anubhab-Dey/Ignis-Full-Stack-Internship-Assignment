from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import Event
from .serializers import UserSerializer, EventSerializer


# User Registration View
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer


# User Login View
class LoginView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Invalid Credentials"},
                status=status.HTTP_400_BAD_REQUEST,
            )


# Event List/Create View
class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )  # Automatically assign the logged-in user as the creator of the event


# Event Detail View
class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        event = serializer.instance
        user = self.request.user
        # Handle 'like' functionality - Toggle like status
        if "like" in self.request.data:
            if self.request.data["like"]:
                event.is_liked = not event.is_liked  # Toggle the like status
                serializer.save()
        else:
            serializer.save()  # Normal update without touching the 'like' status

    def delete(self, request, *args, **kwargs):
        event = self.get_object()
        if event.user != request.user:
            return Response(
                {
                    "error": "You cannot delete an event that you did not create."
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().delete(request, *args, **kwargs)
