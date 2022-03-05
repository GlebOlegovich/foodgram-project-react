from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Ingredient, Tag

User = get_user_model()


class IngredientSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
