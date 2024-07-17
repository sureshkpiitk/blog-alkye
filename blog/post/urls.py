from django.urls import path

from post.views import PostView, CommentView, CommentPublicAPIView, PostPublicAPIView

urlpatterns = [
    path("", PostView.as_view(), name="post"),
    path("pub/", PostPublicAPIView.as_view(), name="post-public"),
    path("pub/<int:pk>/", PostPublicAPIView.as_view(), name="get-post-public"),
    path("<int:pk>/", PostView.as_view(), name="get-post"),
    path("comment/", CommentView.as_view(), name="comment"),
    path("pub/comment/", CommentPublicAPIView.as_view(), name="comment-public"),
    path("comment/<int:pk>/", CommentView.as_view(), name="get-comment"),
    path("pub/comment/<int:pk>/", CommentPublicAPIView.as_view(), name="get-comment-public"),
]
