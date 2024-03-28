from django.urls import path
from myapp import views

urlpatterns = [
    path('upload/',views.upload_image),
]