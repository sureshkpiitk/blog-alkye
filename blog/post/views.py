from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework import mixins, generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.pagination import CursorPagination, LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from post.models import Post, Comment
from post.serializer import PostSerializer, CommentSerializer


# Create your views here.

class APIView(mixins.ListModelMixin,
              mixins.CreateModelMixin,
              mixins.RetrieveModelMixin,
              mixins.UpdateModelMixin,
              mixins.DestroyModelMixin,
              generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        if "pk" in kwargs:
            return self.retrieve(request, *args, **kwargs)

        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class PostPublicAPIView(APIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    page_size = 10
    max_page_size = 20
    http_method_names = ["get"]

    def get_queryset(self):
        query = {}
        if "auther" in self.request.GET:
            query["auther"] = int(self.request.GET.get("auther"))
        elif "created" in self.request.GET:
            query["created"] = self.request.GET.get("created")
        return self.queryset.filter(**query)


class PostView(PostPublicAPIView):
    authentication_classes = [BasicAuthentication, OAuth2Authentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "patch", 'delete']


class CommentPublicAPIView(APIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    page_size = 10
    max_page_size = 20
    http_method_names = ["get"]

    def get_queryset(self):
        query = {}
        if "auther" in self.request.GET:
            query["auther"] = int(self.request.GET.get("auther"))
        elif "created" in self.request.GET:
            query["created"] = self.request.GET.get("created")
        return self.queryset.filter(**query)


class CommentView(CommentPublicAPIView):
    authentication_classes = [BasicAuthentication, OAuth2Authentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "patch", 'delete']
