from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, filters
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from .models import Food, Order, PromoCode
from .serializers import (
    RegisterSerializer,
    FoodSerializer,
    OrderSerializer,
    OrderCreateSerializer,
    PromoCodeSerializer
)

User = get_user_model()


class FoodPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


@extend_schema(
    summary="Foydalanuvchi royxatdan otadi",
    description="Yangi foydalanuvchi royxatdan otadi",
    request=RegisterSerializer,
    responses=RegisterSerializer
)
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


@extend_schema(
    summary="Mavjud ovqatlar royxati",
    description="Login bolgan foydalanuvchi barcha AVAILABLE ovqatlarni koradi",
    responses=FoodSerializer(many=True)
)
class FoodListView(generics.ListAPIView):
    queryset = Food.objects.filter(status='AVAILABLE')
    serializer_class = FoodSerializer
    pagination_class = FoodPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['category']
    permission_classes = [permissions.IsAuthenticated]


@extend_schema(
    summary="Yangi ovqat qoshish",
    description="Faqat ADMIN yangi ovqat qoshadi",
    request=FoodSerializer,
    responses=FoodSerializer
)
class FoodCreateView(generics.CreateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [permissions.IsAdminUser]


@extend_schema(
    summary="Ovqatni yangilash",
    description="Faqat ADMIN ovqat malumotlarini yangilaydi",
    request=FoodSerializer,
    responses=FoodSerializer
)
class FoodUpdateView(generics.UpdateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [permissions.IsAdminUser]


@extend_schema(
    summary="Ovqatni ochirish",
    description="Faqat ADMIN ovqatni tizimdan ochiradi"
)
class FoodDeleteView(generics.DestroyAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [permissions.IsAdminUser]


@extend_schema(
    summary="Yangi buyurtma yaratish",
    description="Login bolgan foydalanuvchi buyurtma yaratadi, promo kod ishlatishi mumkin",
    request=OrderCreateSerializer,
    responses=OrderSerializer
)
class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(OrderSerializer(order).data, status=201)


@extend_schema(
    summary="Buyurtmalar royxati",
    description="Login bolgan foydalanuvchi oz buyurtmalarini koradi",
    responses=OrderSerializer(many=True)
)
class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')


@extend_schema(
    summary="Yangi promo kod yaratish",
    description="Faqat ADMIN yangi promo kod yaratadi",
    request=PromoCodeSerializer,
    responses=PromoCodeSerializer
)
class PromoCodeCreateView(generics.CreateAPIView):
    queryset = PromoCode.objects.all()
    serializer_class = PromoCodeSerializer
    permission_classes = [permissions.IsAdminUser]


@extend_schema(
    summary="Promo kodni o'chirish",
    description="Faqat ADMIN promo kodni tizimdan o'chiradi",
    responses=None
)
class PromoCodeDeleteView(generics.DestroyAPIView):
    queryset = PromoCode.objects.all()
    serializer_class = PromoCodeSerializer
    permission_classes = [permissions.IsAdminUser]