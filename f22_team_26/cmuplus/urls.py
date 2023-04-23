from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('course_info/<str:course_number>', views.course_info, name='course_info'),
    path('post_experience', views.post_experience, name='post_experience'),
    path('discussion_board', views.discussion_board, name='discussion_board'),
    path('post_info/<str:post_id>', views.post_info, name='post_info'),
    path('barchart/<str:course_number>', views.create_barchart, name='barchart'),
    path('display_experience/<int:course_experience_id>', views.display_experience, name='display_experience'),
]