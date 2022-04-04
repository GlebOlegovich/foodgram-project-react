from django.contrib import admin

from favs_n_shopping.models import Favorite
from .models import Ingredient, IngredientInRecipe, Recipe, Tag


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('^name',)


class RecipeIngredientAdmin(admin.TabularInline):
    model = IngredientInRecipe
    fk_name = 'recipe'


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'favorited')
    list_filter = ('author', 'name', 'tags')
    exclude = ('ingredients',)
    search_fields = ('^name',)

    inlines = [
        RecipeIngredientAdmin,
    ]

    @admin.display(empty_value='Никто')
    def favorited(self, obj):
        favorited_count = Favorite.objects.filter(recipe=obj).count()
        return favorited_count

    favorited.short_description = 'Кол-во людей добавивших в избранное'


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientInRecipe, RecipeIngredientAdmin)
