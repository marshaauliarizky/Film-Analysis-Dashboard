from django.core.management.base import BaseCommand
from django.db import connection
from film_analysis.models import CategoryPerformance
import pandas as pd

class Command(BaseCommand):
    help = 'ETL: Extract category performance data'

    def handle(self, *args, **kwargs):
        CategoryPerformance.objects.all().delete()

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT c.category_id, c.name,
                       COUNT(r.rental_id) as total_rentals,
                       COALESCE(SUM(p.amount), 0) as total_revenue
                FROM category c
                JOIN film_category fc ON c.category_id = fc.category_id
                JOIN film f ON fc.film_id = f.film_id
                JOIN inventory i ON f.film_id = i.film_id
                JOIN rental r ON i.inventory_id = r.inventory_id
                LEFT JOIN payment p ON r.rental_id = p.rental_id
                GROUP BY c.category_id, c.name
                ORDER BY total_rentals DESC
            """)
            rows = cursor.fetchall()

        for row in rows:
            CategoryPerformance.objects.create(
                category_id=row[0],
                category_name=row[1],
                total_rentals=row[2],
                total_revenue=row[3]
            )

        # Autosave to CSV
        df = pd.DataFrame(rows, columns=['category_id', 'category_name', 'total_rentals', 'total_revenue'])
        df.to_csv('category_performance_dataset.csv', index=False)
        self.stdout.write(self.style.SUCCESS('CSV saved: category_performance_dataset.csv'))

        self.stdout.write(self.style.SUCCESS(
            f'Category performance ETL done! {len(rows)} categories processed.'
        ))