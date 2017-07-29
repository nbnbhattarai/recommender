from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Music(models.Model):
    artist = models.CharField(max_length=250)
    song = models.CharField(max_length=250)
    def __str__(self):
        return self.artist+"-"+self.song
        #return self.artist

class User(models.Model):
    fb_id = models.IntegerField()
    userName = models.CharField(max_length=250)
    op = models.IntegerField()
    cons = models.IntegerField()
    ex = models.IntegerField()
    ag = models.IntegerField()
    neu = models.IntegerField()
    def __str__(self):
        return self.userName

class UserMusic(models.Model):
    song = models.ForeignKey(Music, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators = [MaxValueValidator(5),MinValueValidator(0)])
    def __str__(self):
            return u'%s-%s-%s' %(self.songid,self.userid,self.rating)

class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    music = models.ManyToManyField(Music)
    def __str__(self):
        return self.user
