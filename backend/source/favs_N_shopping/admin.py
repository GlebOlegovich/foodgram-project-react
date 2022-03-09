from django.contrib import admin

from .models import Purchase, Favorites


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Favorites, FavoriteAdmin)
