from django.urls import path
from .views import home,Contact,MyFormView, download_file


urlpatterns = [
    # path('home/', HomePageView.as_view()),
    path('home/', home , name='home'),
    # path('contact/', Contact.as_view() , name='contact'),
    path('', MyFormView.as_view() , name='test'),
    path('download/<str:filename>/', download_file, name='download'),
    # path('download/<str:filename>//',download_file, name='downlaod'),

]
