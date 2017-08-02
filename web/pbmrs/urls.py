from django.conf.urls import url
from . import views
urlpatterns = [
        url(r'^$',views.Home.as_view(), name='home'),
        url(r'^recommendation$',views.recommend),
        url(r'^about_personality$',views.about_personality),
        url(r'^classify_personality$',views.classifyPersonality),
        url(r'^logout$',views.LogOutView.as_view(), name='Logout'),
        url(r'^profile$',views.ProfileView.as_view(), name='profile'),
        url(r'^about$',views.AboutView.as_view(), name='about'),
]
