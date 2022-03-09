from django.contrib import admin

from favs_N_shopping.models import Favorites
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

    inlines = [
        RecipeIngredientAdmin,
    ]

    def favorited(self, obj):
        favorited_count = Favorites.objects.filter(recipe=obj).count()
        return favorited_count

    favorited.short_description = 'В избранном'


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientInRecipe, RecipeIngredientAdmin)
