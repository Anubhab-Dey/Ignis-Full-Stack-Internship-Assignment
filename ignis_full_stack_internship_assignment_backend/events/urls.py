from django.urls import path
from .views import (
    CreateUserView,
    LoginView,
    EventListCreateView,
    EventDetailView,
)

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("", EventListCreateView.as_view(), name="events-list"),
    path("<int:pk>/", EventDetailView.as_view(), name="event-detail"),
]
