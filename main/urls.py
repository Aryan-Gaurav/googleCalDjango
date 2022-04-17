from xml.etree.ElementInclude import include
from django.urls import path
from .views import GoogleCalendarInitView,GoogleCalendarRedirectView
urlpatterns = [
   
    path('init',GoogleCalendarInitView.as_view()),
    path('redirect',GoogleCalendarRedirectView.as_view()),

]
