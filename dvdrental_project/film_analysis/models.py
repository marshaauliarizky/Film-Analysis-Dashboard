from django.db import models

# Create your models here.
# OLAP Table 1: Film Popularity
class FilmPopularity(models.Model):
    film_id = models.IntegerField()
    title = models.CharField(max_length=255)
    rental_count = models.IntegerField(default=0)
    rating = models.CharField(max_length=10)
    rental_rate = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = 'film_popularity'

    def __str__(self):
        return f"{self.title} - {self.rental_count} rentals"


# OLAP Table 2: Category Performance
class CategoryPerformance(models.Model):
    category_id = models.IntegerField()
    category_name = models.CharField(max_length=50)
    total_rentals = models.IntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'category_performance'

    def __str__(self):
        return f"{self.category_name} - {self.total_rentals} rentals"


# OLAP Table 3: Film Model Info
class FilmModelInfo(models.Model):
    model_name = models.CharField(max_length=100)
    model_file = models.CharField(max_length=255)
    training_data = models.CharField(max_length=255)
    training_date = models.DateTimeField()
    model_summary = models.TextField(blank=True)

    def __str__(self):
        return f"{self.model_name} - {self.training_date.strftime('%Y-%m-%d')}"