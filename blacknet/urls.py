"""blacknet URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import main.views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.home,name="home"),
    path("api/twitter",views.twitter,name="twitterPage"),
    path("api/twitter/suspects",views.suspect,name="suspect"),

    path("api/twitter/add-suspect/<username>",views.addSuspect,name="addSuspect"),
    path("api/twitter/delete-suspect/<username>",views.deleteSuspect,name="deleteSuspect"),
    path("api/twitter/suspect-list", views.SuspectListView.as_view()),

    path("api/twitter-profile/username=<username>",views.get_profile,name="getTwitterProfile"),
    path("api/twitter/username=<userName>",views.twitterApi,name="twitter"),
    path("api/twitter/hashtag=<hashtag>",views.twitterHashTagApi,name="twitterHashTag"),
]