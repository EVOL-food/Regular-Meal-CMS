from rest_framework import serializers
from menu.models import Menu, Dish, Category, DailyMeal, Photo


class PhotoImageSerializer(serializers.HyperlinkedModelSerializer):
    image = serializers.ImageField(allow_empty_file=True, use_url=True)
    image_large = serializers.ImageField(allow_empty_file=True, use_url=True)
    image_medium = serializers.ImageField(allow_empty_file=True, use_url=True)
    image_small = serializers.ImageField(allow_empty_file=True, use_url=True)

    class Meta:
        model = Photo
        fields = ('image', 'image_large', 'image_medium', 'image_small')


class DishSerializer(serializers.ModelSerializer):
    ingredients = serializers.StringRelatedField(many=True)

    class Meta:
        model = Dish
        fields = ['title', 'slug', 'calories', 'meal_of_the_day', 'ingredients']


class CategorySerializer(serializers.ModelSerializer):
    photo = PhotoImageSerializer(many=False, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'title', 'description', 'slug', 'photo')


class CategorySerializerShort(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', 'slug')


class DailyMealSerializer(serializers.ModelSerializer):
    dish_1 = DishSerializer(read_only=True, many=False)
    dish_2 = DishSerializer(read_only=True, many=False)
    dish_3 = DishSerializer(read_only=True, many=False)
    dish_4 = DishSerializer(read_only=True, many=False)
    dish_5 = DishSerializer(read_only=True, many=False)

    class Meta:
        model = DailyMeal
        fields = ('title', 'calories', 'dish_1', 'dish_2',
                  'dish_3', 'dish_4', 'dish_5')


class MenuSerializerList(serializers.ModelSerializer):
    category = CategorySerializerShort(read_only=True, many=False)
    photo = PhotoImageSerializer(many=False, read_only=True)

    class Meta:
        model = Menu
        fields = ['id', 'title', 'description', 'slug', 'photo', 'category']


class MenuSerializerDetail(serializers.ModelSerializer):
    category = CategorySerializerShort(read_only=True, many=False)
    day_1 = DailyMealSerializer(read_only=True, many=False)
    day_2 = DailyMealSerializer(read_only=True, many=False)
    day_3 = DailyMealSerializer(read_only=True, many=False)
    day_4 = DailyMealSerializer(read_only=True, many=False)
    day_5 = DailyMealSerializer(read_only=True, many=False)
    day_6 = DailyMealSerializer(read_only=True, many=False)
    day_7 = DailyMealSerializer(read_only=True, many=False)
    photo = PhotoImageSerializer(many=False, read_only=True)

    class Meta:
        model = Menu
        fields = ['id', 'title', 'description', 'slug', 'category', 'photo',
                  'day_1', 'day_2', 'day_3', 'day_4', 'day_5', 'day_6', 'day_7']
