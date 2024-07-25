from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('contents', views.getContents, name='get_contents'),
    path('contents/<int:pk>', views.getContent, name='get_content'),
    path('contents/add', views.addContent, name='add_content'),
    path('contents/update/<int:pk>', views.updateContent, name='update_content'),
    path('contents/delete/<int:pk>', views.deleteContent, name='delete_content'),
    path('register', views.RegisterView.as_view(), name='auth_register'),
    path('token', views.MyTokenObtainPairView.as_view(), name='auth_login'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('', views.getRoutes, name='get_routes'),
]