from django.contrib import admin
from .models import RecommendationModel,MusicModel,UserModel,UserMusicModel, SessionModel


admin.site.register(MusicModel)
admin.site.register(UserModel)
admin.site.register(UserMusicModel)
admin.site.register(RecommendationModel)
admin.site.register(SessionModel)
