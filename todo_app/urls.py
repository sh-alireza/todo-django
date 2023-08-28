from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home_page"),
    path('home',views.home,name="home_page"),
    path('sign-up',views.sign_up,name="sign_up"),
    path('new-task/<int:user_id>',views.new_task,name="new_task"),
    path('edit-task/<str:edit_type>/<int:task_id>',views.edit_task,name="edit_task"),
    path('user-profile/<int:user_id>',views.user_profile,name="user_profile"),
    path('remove-profile/<int:user_id>',views.remove_profile,name="remove_profile"),
]
