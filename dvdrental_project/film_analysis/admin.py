from django.contrib import admin
from django.utils.html import format_html
from .models import FilmPopularity, CategoryPerformance, FilmModelInfo

# Register your models here.
@admin.register(FilmPopularity)
class FilmPopularityAdmin(admin.ModelAdmin):
    list_display = ('title', 'rental_count', 'rating', 'rental_rate')
    search_fields = ('title', 'rating')
    ordering = ('-rental_count',)

@admin.register(CategoryPerformance)
class CategoryPerformanceAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'total_rentals', 'total_revenue')
    ordering = ('-total_rentals',)

@admin.register(FilmModelInfo)
class FilmModelInfoAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'training_date', 'training_data', 'short_summary')
    search_fields = ('model_name',)

    def short_summary(self, obj):
        return (obj.model_summary[:75] + '...') if obj.model_summary else "-"
    short_summary.short_description = "Summary"