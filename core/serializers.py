from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Food, Order, OrderItem, PromoCode

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'phone_number', 'address')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            phone_number=validated_data.get('phone_number', ''),
            address=validated_data.get('address', '')
        )
        return user


class FoodSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = Food
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    food_name = serializers.ReadOnlyField(source='food.name')

    class Meta:
        model = OrderItem
        fields = ['id', 'food', 'food_name', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'total_price', 'delivery_address', 'promo_code', 'created_at', 'items']


class OrderItemCreateSerializer(serializers.Serializer):
    food_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class OrderCreateSerializer(serializers.Serializer):
    items = OrderItemCreateSerializer(many=True)
    promo_code = serializers.CharField(required=False, allow_blank=True)
    delivery_address = serializers.CharField()

    def create(self, validated_data):
        user = self.context['request'].user
        items = validated_data['items']
        promo_code_value = validated_data.get('promo_code')
        delivery_address = validated_data.get('delivery_address', user.address)

        total_price = 0
        order = Order.objects.create(user=user, total_price=0, delivery_address=delivery_address)

        for item in items:
            food = Food.objects.get(id=item['food_id'])
            quantity = item['quantity']
            price = food.price * quantity
            OrderItem.objects.create(order=order, food=food, quantity=quantity, price=price)
            total_price += price

        if promo_code_value:
            promo = PromoCode.objects.filter(code=promo_code_value, is_active=True).first()
            if promo and total_price >= promo.min_amount:
                total_price -= promo.discount_amount
                order.promo_code = promo

        order.total_price = total_price
        order.save()
        return order


class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields = ['id', 'code', 'min_amount', 'discount_amount', 'is_active', 'expires_at']