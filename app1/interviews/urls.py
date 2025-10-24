from django.urls import path

from interviews.views import interviews_availability


app_name = "interviews"
urlpatterns = [
    path("<int:id>/availability", interviews_availability),
]
