from django.urls import path, include
from django.views.generic.base import TemplateView
from api import views

urlpatterns = [
    path('', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),
    path('api/login', views.userLogin.as_view()),
    path('api/sign-up', views.userSignUp.as_view()),
    path('api/admin/authors', views.authorManagement.as_view()),
    path('api/admin/articles', views.articleManagement.as_view()),
    path('api/articles/', views.listArticles.as_view()),
    path('api/articles/<int:id>', views.articleDetails.as_view()),
]