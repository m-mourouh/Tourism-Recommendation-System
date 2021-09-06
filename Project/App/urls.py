from django.urls import path 
from . import views
from django.conf import settings
from django.conf.urls.static import  static

urlpatterns = [
    path('',views.home,name = "home-page") ,
    path('login/',views.login,name = "login-page") ,
    path('logout/',views.logout,name = "logout-page") ,
    path('signup/',views.signup,name = "signup-page") ,
    path('profile/',views.profile,name = "profile-page") ,
    path('details/<int:id>/',views.details,name = "details-page") ,
    path('recommendation/',views.recommend,name="recommendation-page")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
