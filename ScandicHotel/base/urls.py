from django.urls import include, path 
from . import views 

urlpatterns=[
    path("",views.home,name="home"),
    path("rooms/",views.rooms,name="rooms"),
    path("signup/",views.signup,name="signup"),
    path("contact/",views.contact,name="contact"),
    path('accounts/', include('allauth.urls')),
]