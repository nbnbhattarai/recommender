from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class MusicModel(models.Model):
    artist = models.CharField(max_length=250)
    song = models.CharField(max_length=250)
    def __str__(self):
        return self.artist+"-"+self.song
        #return self.artist

class UserModel(models.Model):
    fb_id = models.IntegerField()
    name = models.CharField(max_length=250)
    op = models.FloatField()
    cons = models.FloatField()
    ex = models.FloatField()
    ag = models.FloatField()
    neu = models.FloatField()
    def __str__(self):
        return self.name #+ ' : '+  str(self.op) + str(self.cons) + str(self.ex) + str(self.ag) + str(self.neu)

class UserMusicModel(models.Model):
    music = models.ForeignKey(MusicModel, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    rating = models.IntegerField(validators = [MaxValueValidator(10),MinValueValidator(0)])
    def __str__(self):
            return u'%s-%s-%s' %(self.music,self.user,self.rating)

class RecommendationModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    music = models.ManyToManyField(MusicModel)
    def __str__(self):
        return self.user

class SessionModel(models.Model):
	user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
	sessionid = models.CharField(max_length=30, unique=True)

	def __str__(self):
		return self.user.name + ':' + self.sessionid
