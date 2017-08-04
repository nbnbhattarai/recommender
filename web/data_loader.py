from pbmrs.models import UserModel, MusicModel, UserMusicModel
import random
import csv


def load_usermusicmodel():
    for user in UserModel.objects.all():
        for music in MusicModel.objects.all():
            rand_test = random.random()
            if rand_test > 0.2:
                rating = random.randrange(0, 10)
                UserMusicModel.objects.create(user=user, music=music,
                                              rating=rating)


def load_usermodel():
    with open('user_list.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            UserModel.objects.create(fb_id=row[0], name=row[1],
                                     op=float(row[2]), cons=float(row[3]),
                                     ex=float(row[4]),
                                     ag=float(row[5]), neu=float(row[6]))


def load_musicmodel():
    with open('song_list.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            MusicModel.objects.create(song=row[0], artist=row[1],
                                      youtube_id=row[2])


# if __name__ == '__main__':
def main():
    load_usermodel()
    load_musicmodel()
    load_usermusicmodel
