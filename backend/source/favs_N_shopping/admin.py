from django.contrib import admin

from .models import Purchase, Favorite


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Favorite, FavoriteAdmin)
