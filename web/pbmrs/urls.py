from django.conf.urls import url
from . import views
urlpatterns = [
        url(r'^$',views.Home.as_view(), name='home'),
        url(r'^recommendation$',views.recommend),
        url(r'^about_personality$',views.about_personality),
        url(r'^classify_personality$',views.classifyPersonality),
        url(r'^logout$',views.logout_view),
]
