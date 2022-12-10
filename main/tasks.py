from __future__ import absolute_import, unicode_literals
from .models import Account, Insight
from django.contrib.auth.models import User
from celery import shared_task
from utils.instagram_insights import InstagramInsights, MediaInsights, UserInsights

import time

#IMPLEMENT WRITE FUNC
@shared_task
def display_account():

    users = User.objects.all()

    for user in users:
        if len(user.account_set.all()) > 0:
            for account in user.account_set.all():
                ig = InstagramInsights(account, MediaInsights, UserInsights)

                date = ig.get_date()
                day = ig.get_day()
                month = ig.get_month()
                media_insights = ig.get_basic_insights('media')
                story_insights = ig.get_basic_insights('stories')
                carousel_insights = ig.get_basic_insights('children')
                story_count = ig.get_media_count(story_insights)
                media_count = ig.get_media_count(media_insights)
                carousel_count = ig.get_media_count(carousel_insights)
                media_likes, media_comments = ig.get_likes_comments(media_insights)
                media_reach_impressions = ig.get_media_reach_impressions()
                story_reach_impressions = ig.get_story_reach_impressions()
                carousel_reach_impressions = ig.get_carousel_reach_impressions()
                account_reach_impressions = ig.get_account_reach_impressions()

                insights = Insight.objects.create(
                account=account,
                date=date,
                day=day,
                month=month,
                story_count=story_count,
                media_count=media_count,
                carousel_count=carousel_count,
                media_likes=media_likes,
                media_comments=media_comments,
                media_reach_impressions=media_reach_impressions,
                story_reach_impressions=story_reach_impressions,
                carousel_reach_impressions=carousel_reach_impressions,
                account_reach_impressions=account_reach_impressions,
                )

                insights.save()
        else:
            continue
    
    return 'successfully written.'