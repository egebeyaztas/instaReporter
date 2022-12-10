from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('add-account/', views.add_account, name='add'),
    path('export-insights/', views.export_insights, name='export'),
    path('register/', views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name= "logout"),
]