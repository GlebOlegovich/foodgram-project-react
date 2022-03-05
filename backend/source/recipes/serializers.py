from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Ingredient

User = get_user_model()


class IngredientSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
