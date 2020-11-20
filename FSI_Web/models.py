
from djongo import models


# Create your models here.



class Project(models.Model):
    # _id = models.ObjectIdField()
    id = models.CharField(max_length=100, primary_key=True)
    project_name = models.CharField(max_length=255)
    description = models.TextField()
    user_id = models.CharField(max_length=255,default='')
    start_time = models.CharField(max_length=255)
    end_time = models.CharField(max_length=255)
    company = models.CharField(max_length=255)


    def __str__(self):
        return (self.project_name)


class Post(models.Model):
    # _id = models.ObjectIdField()
    id = models.CharField(max_length=100, primary_key=True)
    project_id = models.CharField(max_length=255,default='')
    num_likes = models.IntegerField()
    num_comments = models.IntegerField()
    # num_shares = models.IntegerField()
    content = models.TextField()
    # time_create = models.CharField(max_length=255)

    def __str__(self):
        return self.content


class Comments(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    post_id = models.CharField(max_length=255, default='')
    # time_create = models.CharField(max_length=255)
    content = models.TextField()
    num_likes = models.IntegerField()
    # author = models.CharField(max_length=255)
    effect = models.CharField(max_length=40)

    def __str__(self):
        return self.content

class FSI_user(models.Model):
    id = models.CharField(max_length=22, primary_key=True)
    username = models.CharField(max_length=255)
    email = models.EmailField()
    token = models.CharField(max_length=255)
    pictureURL = models.CharField(max_length=255)


    def __str__(self):
        return self.username or ''



