from django.urls import path
from library.api import api

urlpatterns = [
    path("api/", api.urls),
]
