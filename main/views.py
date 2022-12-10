from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Account, Insight
from utils.instagram_insights import InstagramInsights, MediaInsights, UserInsights
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required


def home(request):
    
    accounts = Account.objects.all()
    account = Account.objects.first()
    ig = InstagramInsights(account, MediaInsights, UserInsights)
    print(ig.get_day())

    return render(request, 'index.html', {'accounts': accounts})

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("home")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="register.html", context={"register_form":form})


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("home")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect('home')

@login_required
def add_account(request):

    if request.method == 'POST':

        access_token = request.POST.get('accesstoken')
        client_id = request.POST.get('clientid')
        client_secret = request.POST.get('clientsecret')
        fb_id = request.POST.get('fbid')
        ig_id = request.POST.get('igid')
        username = request.POST.get('username')
        user = request.user

        account = Account.objects.create(
                user=user,
                access_token=access_token,
                client_id=client_id,
                client_secret=client_secret,
                page_id=fb_id,
                instagram_id=ig_id,
                username=username
                )
        account.save()

        return redirect('home')

    return render(request, 'add_account.html', {})

@login_required
def export_insights(request):

    if request.method == 'POST' and request.is_ajax():
        account = Account.objects.get(username=request.POST.get('value'))

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
    
    return JsonResponse({'success': 'İstatistikler Kaydedildi.'})
