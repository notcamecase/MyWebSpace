from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('post',views.show_all_post,name = 'post'),
    path('post/<int:post_id>/',views.single_post,name='single_post'),
    path('search/',views.search,name='search')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)