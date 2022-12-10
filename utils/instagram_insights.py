import datetime
import calendar
from re import X
import pandas as pd
import requests
import json

class MediaInsights:


    def __init__(self, params):
        self.params = params
        self.IMAGE = 'IMAGE'
        self.STORIES = 'STORIES'
        self.CAROUSEL = 'CAROUSEL_ALBUM'


    def makeAPICall(self, url: str, endpointParams: dict):
        
        data = requests.get(url, endpointParams)
        json_data = json.loads(data.content)
        formatted_data = json.dumps(json_data, indent=4)
        return json_data


    def get_insights(self, m_type: str, since, until):

        """

        type: /media, /stories, '/children'

        """
        """
        API Endpoint:
        https://graph.facebook.com/{graph-api-version}/{ig-user-id}/media?fields={fields}

        """
        acc_id = self.params.instagram_id
        url = self.params.endpoint_base + acc_id + '/' + m_type
        endpointParams = dict()
        endpointParams['fields'] = 'id,caption,media_type,media_url,permalink,thumbnail_url,timestamp,username,like_count,comments_count'
        endpointParams['since'] = since
        endpointParams['until'] = until
        endpointParams['access_token'] = self.params.access_token

        basic_insights = self.makeAPICall(url, endpointParams)
        return basic_insights



    def get_advanced_insights(self, basic_insights: dict):

        """
        API Endpoint:
        https://graph.facebook.com/{graph-api-version}/{ig-media-id}/insights?metric={metric}

        """

        adv_insights = []
        temp_params = dict()
        for data in basic_insights['data']:
            temp_params['latest_media_id'] = data['id']

            url = self.params.endpoint_base + temp_params['latest_media_id'] + '/insights'
            
            endpointParams = dict()
            if data['media_type'] == self.IMAGE:
                endpointParams['metric'] = 'engagement,impressions,reach,saved'
            elif data['media_type'] == self.STORIES:
                endpointParams['metric'] = 'reach,impressions,replies'
            elif data['media_type'] == self.CAROUSEL:
                endpointParams['metric'] = 'carousel_album_engagement,carousel_album_impressions,carousel_album_reach,carousel_album_saved'
            endpointParams['access_token'] = self.params.access_token

            advanced_insights = self.makeAPICall(url, endpointParams)
            adv_insights.append(advanced_insights)

        return adv_insights


class UserInsights(object):

    def __init__(self, params):
        self.params = params

    def makeAPICall(self, url, endpointParams):

        data = requests.get(url, endpointParams)
        json_data = json.loads(data.content)
        formatted_json = json.dumps(json_data, indent=4)

        return json_data

    def get_user_metrics(self, metrics: list = ['impressions', 'reach', 'profile_views','follower_count'],period='day' ,since='', until='',):

        """
        API Endpoint:
        https://graph.facebook.com/{ig-user-id}/insights?metric={metric}

        """

        url = self.params.endpoint_base + self.params.instagram_id + '/insights'

        endpointParams = dict()
        endpointParams['metric'] = ','.join(metrics)
        endpointParams['access_token'] = self.params.access_token
        endpointParams['period'] = period
        endpointParams['since'] = since
        endpointParams['until'] = until

        data = self.makeAPICall(url, endpointParams)

        return data

    def get_adv_user_metrics(self):
        url = self.params.endpoint_base + self.params.instagram_id + '/insights'

        endpointParams = dict()
        endpointParams['metric'] = 'audience_city,audience_country,audience_gender_age,online_followers'
        endpointParams['period'] = 'lifetime'
        endpointParams['access_token'] = self.params.access_token
        data = self.makeAPICall(url, endpointParams)

        return data



class InstagramInsights:

    def __init__(self, params, MediaInsights, UserInsights):
        self.params = params
        self.media_insights = MediaInsights(params)
        self.user_insights = UserInsights(params)
        

    def convert_date(self, date: str):
        date = date.replace(' ', '')
        dates = date.split('/')
        date_time = datetime.datetime(int(dates[2]), int(dates[1]), int(dates[0]), 5, 0)
        unix_date = calendar.timegm(date_time.utctimetuple())

        return unix_date


    def get_date(self, time_delta=None):
        today = datetime.date.today()
        current_date = today.strftime('%d/%m/%Y')
        if time_delta:
            date = today - datetime.timedelta(time_delta)
            current_date = date.strftime('%d/%m/%Y')
            return current_date
        return current_date

    def get_day(self):
        today = datetime.datetime.today().strftime('%A')

        days = {'Monday': 'Pazartesi', 'Tuesday':'Salı', 'Wednesday':'Çarşamba', 'Thursday':'Perşembe', 'Friday':'Cuma', 'Saturday':'Cumartesi', 'Sunday':'Pazar'}
        
        for day,x in days.items():
            if today == day:
                today = x

        return today

    def get_month(self):

        this_month = datetime.datetime.today().strftime('%B')

        months = {
            'January': 'Ocak',
            'February': 'Şubat',
            'March': 'Mart',
            'April': 'Nisan',
            'May': 'Mayıs',
            'June': 'Haziran',
            'July': 'Temmuz',
            'August': 'Ağustos',
            'September': 'Eylül',
            'October': 'Ekim',
            'November': 'Kasım',
            'December': 'Aralık',
        }
        
        for month,x in months.items():
            if this_month == month:
                this_month = x

        return this_month

    def get_basic_insights(self, m_type):
        data = self.media_insights.get_insights(m_type=m_type, since=str(self.convert_date(self.get_date(1))), until=str(self.convert_date(self.get_date())))

        return data

    def get_media_count(self, data):

        try:
            counter = 0
            if len(data['data']) >= 1:
                for i in data['data']:
                    if i['id']:
                        counter += 1
        except:
            counter = 0
        
        return counter
    

    def get_likes_comments(self, data):

        likes_count = []
        comments_count = []
        likes = {}
        comments = {}
        like_str = []
        comment_str = []
        try:

            if len(data['data']) >= 1:
                for i in data['data']:
                    if i['like_count']:
                        likes[i['id']] = i['like_count']
                        z = f'{i["timestamp"]} zamanında atılan post için: {i["like_count"]}'
                    else:
                        likes[i['id']] = 0
                        z = f'{i["timestamp"]} zamanında atılan post için: 0'
                    if i['comments_count']:
                        comments[i['id']] = i['comments_count']
                        y = f'{i["timestamp"]} zamanında atılan post için: {i["comments_count"]}'
                    else:
                        comments[i['id']] = 0
                        y = f'{i["timestamp"]} zamanında atılan post için: 0'
                    
                    like_str.append(z)
                    comment_str.append(y)

                l = ', '.join(like_str)
                c = ', '.join(comment_str)

            else:
                l = 'Yeni gönderi bulunamadı'
                c = 'Yeni gönderi bulunamadı'
            
        except Exception as e:
            likes_count.append('None')
            comments_count.append('None')
            l = 'Gönderi bulunamadı'
            c = 'Gönderi bulunamadı'
            return l,c

        return l,c

    def get_media_reach_impressions(self):
        data = self.media_insights.get_insights(m_type='media', since=str(self.convert_date(self.get_date(1))), until=str(self.convert_date(self.get_date())))
        adv_data = self.media_insights.get_advanced_insights(data)
        insight_list = []
        media_reach_impressions = {}
        string_list = []
        if len(adv_data) >= 1:
            for data in adv_data:
                try:
                    media_reach_impressions['Gösterim'] = data['data'][1]['values'][0]['value']
                    media_reach_impressions['Erişim'] = data['data'][2]['values'][0]['value']
                    media_reach_impressions['Kaydetme'] = data['data'][3]['values'][0]['value']

                    insight_list.append(media_reach_impressions)
                except:
                    continue

            for i in insight_list:
                z = f'Gösterim: {i["Gösterim"]} - Erişim: {i["Erişim"]} - Kaydetme: {i["Kaydetme"]}'
                string_list.append(z)

            x = ', '.join(string_list)

            return x
        
        else:
            z = 'Yeni gönderi bulunamadı'
            return z
    
    def get_story_reach_impressions(self):
        data = self.media_insights.get_insights(m_type='stories', since=str(self.convert_date(self.get_date(1))), until=str(self.convert_date(self.get_date())))
        try:
            adv_data = self.media_insights.get_advanced_insights(data)
        except:
            return 'No Story'
        insight_list = []
        media_reach_impressions = {}
        string_list = []
        if len(adv_data) >= 1:
            for data in adv_data:
                try:
                    media_reach_impressions['Gösterim'] = data['data'][1]['values'][0]['value']
                    media_reach_impressions['Erişim'] = data['data'][2]['values'][0]['value']
                    media_reach_impressions['Yanıt'] = data['data'][3]['values'][0]['value']

                    insight_list.append(media_reach_impressions)
                except:
                    continue

            for i in insight_list:
                z = f'Gösterim: {i["Gösterim"]} - Erişim: {i["Erişim"]} - Kaydetme: {i["Kaydetme"]}'
                string_list.append(z)

            x = ', '.join(string_list)

            return x
        
        else:
            z = 'Yeni gönderi bulunamadı'
            return z
    
    def get_carousel_reach_impressions(self):
        data = self.media_insights.get_insights(m_type='children', since=str(self.convert_date(self.get_date(1))), until=str(self.convert_date(self.get_date())))
        try:
            adv_data = self.media_insights.get_advanced_insights(data)
        except:
            return 'No Carousel'

        insight_list = []
        media_reach_impressions = {}
        string_list = []

        if len(adv_data) >= 1:
            for data in adv_data:
                try:
                    media_reach_impressions['Gösterim'] = data['data'][1]['values'][0]['value']
                    media_reach_impressions['Erişim'] = data['data'][2]['values'][0]['value']
                    media_reach_impressions['Kaydetme'] = data['data'][3]['values'][0]['value']
                    insight_list.append(media_reach_impressions)
                except:
                    continue

            for i in insight_list:
                z = f'Gösterim: {i["Gösterim"]} - Erişim: {i["Erişim"]} - Kaydetme: {i["Kaydetme"]}'
                string_list.append(z)

            x = ', '.join(string_list)

            return x
        
        else:
            z = 'Yeni gönderi bulunamadı'
            return z

    def get_account_reach_impressions(self):

        acc_insights = self.user_insights.get_user_metrics(since=str(self.convert_date(self.get_date(1))), until=str(self.convert_date(self.get_date())))
        
        acc_insights_dict = {
            'impressions': acc_insights['data'][0]['values'][0]['value'],
            'reach': acc_insights['data'][1]['values'][0]['value'],
            'profile_views': acc_insights['data'][2]['values'][0]['value'],
            #'follower_count': acc_insights['data'][3]['values'][0]['value'],
        }
        x = f'Gösterim: {acc_insights_dict["impressions"]} - Erişim: {acc_insights_dict["reach"]} - Profil Ziyaretleri: {acc_insights_dict["profile_views"]}'
        return x

    def get_other_metrics(self):

        metrics = self.user_insights.get_adv_user_metrics()
        if len(metrics['data']) == 0:
            return 'Metrics not available'
        return metrics

    def export_insights(self):

        date = self.get_date()
        day = self.get_day()
        story_count = self.get_media_count(self.get_basic_insights('stories'))
        carousel_count = self.get_media_count(self.get_basic_insights('children'))
        media_count = self.get_media_count(self.get_basic_insights('media'))
        media_likes, media_comments = self.get_likes_comments(self.get_basic_insights('media'))

        media_reach_impressions = self.get_media_reach_impressions()
        story_reach_impressions = self.get_story_reach_impressions()
        carousel_reach_impressions = self.get_carousel_reach_impressions()
        account_reach_impressions = self.get_account_reach_impressions()
        #other_metrics = self.get_other_metrics()

        x = {
            'date': [date],
            'day': [day],
            'story_count': [story_count],
            'carousel_count': [carousel_count],
            'media_count': [media_count],
            'media_likes': [media_likes],
            'media_comments': [media_comments],
            'media_reach_impressions': [media_reach_impressions],
            'story_reach_impressions': [story_reach_impressions],
            'carousel_reach_impressions': [carousel_reach_impressions],
            'account_reach_impressions': [account_reach_impressions],
        }

        df = pd.DataFrame(x)
        df.to_excel('igx.xlsx', sheet_name='ig')

        return df

    def append_df_to_excel(self, df, excel_path):
        df_excel = pd.read_excel(excel_path)
        result = pd.concat([df_excel, df], ignore_index=True)
        result.to_excel(excel_path, index=False)

    def convert_access_token(self):
        url = self.params.endpoint_base + 'oauth/access_token'

        endpointParams = dict()
        endpointParams['grant_type'] = 'fb_exchange_token'
        endpointParams['client_id'] = self.params.client_id
        endpointParams['client_secret'] = self.params.client_secret
        endpointParams['fb_exchange_token'] = self.params.access_token

        data = requests.get(url, endpointParams)
        long_lived_token = json.loads(data.content)

        return long_lived_token

#ig = InstagramInsights(params, MediaInsights, UserInsights)
#likes, comments = ig.get_likes_comments('media')
#cnt = ig.get_media_count('stories')
#adv_data = ig.get_carousel_reach_impressions()
#acc_insights = ig.get_account_reach_impressions()
#metrics = ig.get_other_metrics()
#date = ig.get_date(time_delta=1)
#x = ig.export_insights()
#ig.append_df_to_excel(x, 'igx.xlsx')
#print(metrics)
#print(x)
#print(adv_data)
#print(cnt)
#print(comments)