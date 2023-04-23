"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from socialnetwork import views

urlpatterns = [
    # path("admin/", admin.site.urls),
    path('', views.login_action, name='login'),
    path('register', views.register_action, name='register'),
    path('global_stream', views.global_stream_action, name='global_stream'),
    path('follower_stream', views.follower_stream_action, name='follower_stream'),
    path('my_profile', views.my_profile_action, name='my_profile'),
    path('other_profile/<int:user_id>', views.other_profile_action, name='other_profile'),
    path('logout', views.logout_action, name='logout'),
    path('photo/<int:id>', views.get_photo, name='photo'),
    path('follow/<int:user_id>', views.follow, name='follow'),
    path('unfollow/<int:user_id>', views.unfollow, name='unfollow'),
    path('socialnetwork/get-global', views.get_global_json_dumps_serializer),
    path('socialnetwork/get-follower', views.get_follower_json_dumps_serializer),
    path('socialnetwork/add-comment', views.add_comments, name='ajax-add-comment'),
]
