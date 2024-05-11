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
    path('cart-view/', store_views.CartAPIView.as_view()),
    path('cart-lists/<str:cart_id>/<int:user_id>', store_views.CartListView.as_view()),
    path('cart-lists/<str:cart_id>/', store_views.CartListView.as_view()),
    path('cart-detail/<str:cart_id>/', store_views.CartDetailView.as_view()),
    path('cart-detail/<str:cart_id>/<int:user_id>', store_views.CartDetailView.as_view()),
    path('cart-delete/<str:cart_id>/<str:item_id>/<int:user_id>', store_views.CartItemDeleteView.as_view()),

]

