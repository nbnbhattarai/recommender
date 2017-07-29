from django.contrib import admin
from .models import Recommendation,Music,User,UserMusic


admin.site.register(Music)
admin.site.register(User)
admin.site.register(UserMusic)
admin.site.register(Recommendation)
