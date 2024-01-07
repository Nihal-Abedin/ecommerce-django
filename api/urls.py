from django.urls import path
from user_auths import views as userAuths_views
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    path('user/token/', userAuths_views.MyTokenObtainPairView.as_view()),
    path('user/token/refresh', TokenRefreshView.as_view()),
    path('user/register/', userAuths_views.RegisterView.as_view())
]
