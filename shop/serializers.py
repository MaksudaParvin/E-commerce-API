from rest_framework import serializers
from .models import Category, Product, Order


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    category_name = serializers.CharField(
        source='category.name',
        read_only=True
    )

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
            'stock',
            'category',
            'category_name',
            'created_date',
        ]


class OrderSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'product',
            'quantity',
            'total_price',
            'order_date',
        ]

        read_only_fields = [
            'user',
            'total_price',
            'order_date',
        ]

    def create(self, validated_data):

        product = validated_data['product']
        quantity = validated_data['quantity']

        if quantity > product.stock:
            raise serializers.ValidationError(
                "Not enough stock available."
            )

        total_price = product.price * quantity

        product.stock -= quantity
        product.save()

        order = Order.objects.create(
            user=self.context['request'].user,
            product=product,
            quantity=quantity,
            total_price=total_price
        )

        return order