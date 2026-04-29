from django.core.management.base import BaseCommand
from django.db import connection
from film_analysis.models import FilmPopularity
import pandas as pd

class Command(BaseCommand):
    help = 'ETL: Extract film popularity data from rental history'

    def handle(self, *args, **kwargs):
        # Clear existing data
        FilmPopularity.objects.all().delete()

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT f.film_id, f.title, COUNT(r.rental_id) as rental_count,
                       f.rating, f.rental_rate
                FROM film f
                JOIN inventory i ON f.film_id = i.film_id
                JOIN rental r ON i.inventory_id = r.inventory_id
                GROUP BY f.film_id, f.title, f.rating, f.rental_rate
                ORDER BY rental_count DESC
            """)
            rows = cursor.fetchall()

        for row in rows:
            FilmPopularity.objects.create(
                film_id=row[0],
                title=row[1],
                rental_count=row[2],
                rating=row[3],
                rental_rate=row[4]
            )

        # Autosave to CSV
        df = pd.DataFrame(rows, columns=['film_id', 'title', 'rental_count', 'rating', 'rental_rate'])
        df.to_csv('film_popularity_dataset.csv', index=False)
        self.stdout.write(self.style.SUCCESS('CSV saved: film_popularity_dataset.csv'))

        self.stdout.write(self.style.SUCCESS(
            f'Film popularity ETL done! {len(rows)} films processed.'
        ))