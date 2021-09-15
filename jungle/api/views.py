from api.serializers import ArticleSerializer, AuthorSerializer, ArticleDetailsSerializer
from api.models import Author, Article
from django.contrib.auth import authenticate, get_user_model
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken


class JWTAuthenticationSafe(JWTAuthentication):
    def authenticate(self, request):
        try:
            return super().authenticate(request=request)
        except InvalidToken:
            return None


# Create your views here.
class userSignUp(APIView):
    """
    Registers new users.
    """
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthenticationSafe]

    def post(self, request):
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        if not username or not password:
            return Response({'message': 'Request must provide username and password'}, status=status.HTTP_400_BAD_REQUEST)

        user = get_user_model().objects.create_user(username=username,
                                                    password=password)
        token = AccessToken.for_user(user)
        content = {
            'username': username,
            'token': str(token),
        }
        return Response(content)


class userLogin(APIView):
    """
    Authenticates registered users.
    """

    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthenticationSafe]

    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        if not username or not password:
            return Response({'message': 'Request must provide username and password'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            token = AccessToken.for_user(user)
            content = {
                'token': str(token),
            }
            return Response(content)
        else:
            return Response({'message': 'Failed to authenticate user. Check login information and try again'}, status=status.HTTP_401_UNAUTHORIZED)


class authorManagement(APIView):
    """
    Restricted endpoint for author CRUD.
    """
    permission_classes = [IsAuthenticated]

    queryset = Author.objects.all()

    def get(self, request):
        serializer = AuthorSerializer(self.queryset.all(), many=True)
        return Response(serializer.data)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = AuthorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        author_id = request.data.get('id', None)
        if not author_id:
            return Response({'message': 'You must inform an author id.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            author = self.queryset.get(pk=author_id)
            serializer = AuthorSerializer(author, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Author.DoesNotExist:
            return Response({'message': 'No author was found for the provided id'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        author_id = request.data.get('id', None)
        if not author_id:
            return Response({'message': 'You must inform an author id.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            author = self.queryset.get(pk=author_id)
            author.delete()
            return Response({'message': 'Deleted {}'.format(author_id)})
        except Author.DoesNotExist:
            return Response({'message': 'No author was found for the provided id'}, status=status.HTTP_404_NOT_FOUND)


class articleManagement(APIView):
    """
    Restricted endpoint for article CRUD.
    """
    permission_classes = [IsAuthenticated]
    
    queryset = Article.objects.all()

    def get(self, request):
        serializer = ArticleDetailsSerializer(self.queryset.all(), many=True)
        return Response(serializer.data)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = ArticleDetailsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        article_id = request.data.get('id', None)
        if not article_id:
            return Response({'message': 'You must inform an article id.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            article = self.queryset.get(pk=article_id)
            serializer = AuthorSerializer(article, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Article.DoesNotExist:
            return Response({'message': 'No article was found for the provided id'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        article_id = request.data.get('id', None)
        if not article_id:
            return Response({'message': 'You must inform an article id.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            author = self.queryset.get(pk=article_id)
            author.delete()
            return Response({'message': 'Deleted {}'.format(article_id)})
        except Article.DoesNotExist:
            return Response({'message': 'No article was found for the provided id'}, status=status.HTTP_404_NOT_FOUND)


class listArticles(generics.ListAPIView):
    """
    Lists articles with category filter.
    """
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthenticationSafe]

    serializer_class = ArticleSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned articles to a given category,
        by filtering against a `category` query parameter in the URL.
        """
        queryset = Article.objects.all()
        category = self.request.query_params.get('category')
        if category is not None:
            queryset = queryset.filter(category=category)
        return queryset


class articleDetails(APIView):
    """
    Retrieve basic article details for anonymous users and full article details for logged in users.
    """
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthenticationSafe]

    queryset = Article.objects.all()

    def get(self, request, id):
        try:
            article = self.queryset.get(id=id)
            serializer = ArticleDetailsSerializer(article, context={'anonymous_user':request.user.is_anonymous})
            return Response(serializer.data)
        except Article.DoesNotExist:
            return Response({'message': 'No article was found for the provided id.'}, status=status.HTTP_404_NOT_FOUND)
