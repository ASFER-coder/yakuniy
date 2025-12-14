from django.urls import path
from .views import RegisterView, OrderCreateView, OrderListView, FoodListView, FoodCreateView, FoodUpdateView, FoodDeleteView, PromoCodeCreateView, PromoCodeDeleteView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('foods/', FoodListView.as_view(), name='food-list'),
    path('foods/create/', FoodCreateView.as_view(), name='food-create'),
    path('foods/<int:pk>/update/', FoodUpdateView.as_view(), name='food-update'),
    path('foods/<int:pk>/delete/', FoodDeleteView.as_view(), name='food-delete'),

    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/create/', OrderCreateView.as_view(), name='order-create'),

    path('promocodes/create/', PromoCodeCreateView.as_view(), name='promo-create'),
    path('promocodes/<int:pk>/delete/', PromoCodeDeleteView.as_view(), name='promocode-delete'),
]
