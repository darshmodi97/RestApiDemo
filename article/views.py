from django.contrib.auth.models import User

from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from account.paginations import CustomPagination
from article.models import Article
from article.permissions import IsAllAccessible
from article.serializers import ShowArticleSerializer, ArticleSerializer


class ShowArticles(ListAPIView):
    """
    This API will return the list of an all Articles.
    """
    permission_classes = [IsAllAccessible]
    serializer_class = ShowArticleSerializer
    pagination_class = CustomPagination
    queryset = Article.objects.all()  # queryset attribute is compulsory or

    # override get_queryset(self) method.

    # def get_queryset(self):
    #     return Article.objects.all()


class ArticleDetail(RetrieveUpdateDestroyAPIView):
    """
    This API will return the detail of an particular article from the id and allows us to update and delete it.
    """
    permission_classes = [IsAllAccessible]
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()


class CreateArticleView(ListCreateAPIView):
    """
    This API will return the list of an articles and also allows us to create a new article.
    """
    # authentication_classes = []
    permission_classes = [IsAllAccessible]
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()  # we have to pass queryset attribute while using List API view generic class.

    def perform_create(self, serializer):
        """
        This is default method provided by the CreateApiView and ListCreateApiView generic classes.
        """
        serializer.save(author=User.objects.get(id=self.request.user.id))
        # we have to pass author explicitly like this as it is Article's model field.

        # OR

    # def post(self, request, *args, **kwargs):
    #     serializer = self.serializer_class(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save(author=User.objects.get(id=1))
    #     return Response(
    #         {
    #             "status":status.HTTP_201_CREATED,
    #             "data": serializer.data,
    #         }
    #     )


class UpdateArticleView(RetrieveUpdateAPIView):
    """
    This API will return the detail of an article from the particular id and allows us to update an article.
    """

    permission_classes = [IsAllAccessible]
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()


class DeleteArticleView(RetrieveDestroyAPIView):
    """
    This API will return the detail of an article from the particular id and allows us to delete the article.
    """
    permission_classes = [IsAllAccessible]
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
