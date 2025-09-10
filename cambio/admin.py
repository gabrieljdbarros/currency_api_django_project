from django.contrib import admin
from .models import Rate, FxConfig
from .models import RateHistory
@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    list_display = ('code', 'rate_per_base')
    search_fields = ('code',)

@admin.register(FxConfig)
class FxConfigAdmin(admin.ModelAdmin):
    list_display = ('base_code',)

@admin.register(RateHistory)
class RateHistoryAdmin(admin.ModelAdmin):
    list_display = ('rate', 'value_per_base', 'changed_at')
    list_filter = ('rate',)