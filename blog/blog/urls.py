
from django.urls import path
from .views import (
    blog_post_detail_view,
    blog_post_list_view,
    blog_post_update_view,
    blog_post_delete_view,
    comment_create_view,
    comment_update_view,
    comment_delete_view,

)


urlpatterns = [
    path('', blog_post_list_view),
    path('<str:slug>/', blog_post_detail_view),
    path('<str:slug>/edit/', blog_post_update_view),
    path('<str:slug>/delete/', blog_post_delete_view),
    path('<str:slug>/comment/', comment_create_view),
    path('<str:slug>/<int:id>/editcomment/', comment_update_view),
    path('<str:slug>/<int:id>/deletecomment/', comment_delete_view),
]

