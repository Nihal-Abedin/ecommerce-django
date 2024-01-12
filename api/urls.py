from django.urls import path
from user_auths import views as userAuths_views
from store import views as store_views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('user/token/', userAuths_views.MyTokenObtainPairView.as_view()),
    path('user/token/refresh', TokenRefreshView.as_view()),
    path('user/register/', userAuths_views.RegisterView.as_view()),
    path('user/reset-password/<email>', userAuths_views.ResetUserPasswordEmail.as_view()),
    path('user/set-password/', userAuths_views.PasswordChangeView.as_view()),

    # STORE ENDPOINTS
    path('category/', store_views.CategoryListView.as_view()),
    path('products/', store_views.ProductsListView.as_view()),
    path('products/<slug>', store_views.ProductDetailView.as_view()),
]
