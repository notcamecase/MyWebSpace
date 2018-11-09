from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post',views.show_all_post,name = 'post'),
    path('post/<int:post_id>/',views.single_post,name='single_post'),
    path('search/',views.search,name='search')
]