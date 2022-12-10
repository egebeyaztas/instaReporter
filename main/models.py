from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Account(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=200, blank=False, null=False)
    client_id = models.CharField(max_length=200, blank=False, null=False)
    client_secret = models.CharField(max_length=200, blank=False, null=False)
    page_id = models.CharField(max_length=200, blank=False, null=False)
    instagram_id = models.CharField(max_length=200, blank=False, null=False)
    username = models.CharField(max_length=200, blank=False, null=False)
    graph_domain = models.CharField(max_length=200, default='https://graph.facebook.com', blank=False, null=False)
    graph_version = models.CharField(max_length=200,default='v14.0', blank=False, null=False)
    endpoint_base = models.CharField(max_length=200, default='https://graph.facebook.com/v14.0/', blank=False, null=False)

    def __str__(self):
        return self.username


class Insight(models.Model):
    account = models.ForeignKey(Account, related_name='insights', blank=False, null=False, on_delete=models.CASCADE)
    date = models.CharField(max_length=200, blank=False, null=False)
    day = models.CharField(max_length=200, blank=False, null=False)
    month = models.CharField(max_length=200, blank=False, null=False)
    story_count = models.CharField(max_length=200, blank=False, null=False)
    carousel_count = models.CharField(max_length=200, blank=False, null=False)
    media_count = models.CharField(max_length=200, blank=False, null=False)
    media_likes = models.CharField(max_length=200, blank=False, null=False)
    media_comments = models.CharField(max_length=200, blank=False, null=False)
    media_reach_impressions = models.CharField(max_length=200, blank=False, null=False)
    story_reach_impressions = models.CharField(max_length=200, blank=False, null=False)
    carousel_reach_impressions = models.CharField(max_length=200, blank=False, null=False)
    account_reach_impressions = models.CharField(max_length=200, blank=False, null=False)

    def __str__(self):
        return self.date
    

#SIGNALS