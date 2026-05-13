from django.urls import include, path 
from . import views 

urlpatterns=[
    path("",views.home,name="home"),
    path("rooms/",views.rooms,name="rooms"),
    path("signup/",views.signup,name="signup"),
    path("contact/",views.contact,name="contact"),
    path('accounts/', include('allauth.urls')),
    path('rooms/<slug:slug>/', views.room_detail, name='room_detail'),
    path('rooms/<slug:slug>/reservation/', views.reservation, name='reservation'),
    path('reservation/reservation_success/', views.reservation_success, name='reservation_success'),
    
]