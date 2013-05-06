from django.db import models
from django.contrib.auth.models import User


# class User(models.Model):
#     def __unicode__(self):
#         return self.username
#     username = models.CharField(max_length=100)
#     password = models.CharField(max_length=100)
#     is_logged_in = models.BooleanField()


class Post(models.Model):

    author = models.ForeignKey(User)
    date = models.DateTimeField()
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __unicode__(self):
        return '"{}", by {}, published on {}'.format(self.title, self.author, self.date.date())
        


