from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include
from .views import (home_page,about_page,contact_page,logout_request,login_request,register)
from game.views import game_list_view
from blog.views import blog_post_create_view
from searches.views import search_view                       

urlpatterns = [
    path('',home_page),

    path('admin/', admin.site.urls),

    path('blog-new/', blog_post_create_view),
    path('blog/', include('blog.urls')),

    path('search/', search_view),
    
    path('about/',about_page),
    path('contact/',contact_page),
    re_path(r'^con?/$',contact_page), # will turn con to contact

    path('logout/',logout_request),
    path('login/',login_request),
    path('register/',register),
    path('game/',game_list_view),
]

if settings.DEBUG:
	from django.conf.urls.static import static
	urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT )
	urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT )