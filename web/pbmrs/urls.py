from django.conf.urls import url
from . import views
urlpatterns = [
        url(r'^$',views.home),
        url(r'^recommendation$',views.recommend),
        url(r'^personality$',views.personality),
]
