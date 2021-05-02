from django.urls import path
from .views import MyFormView, download_file


urlpatterns = [
    path('', MyFormView.as_view() , name='test'),
    path('download/<str:filename>/', download_file, name='download'),
]
