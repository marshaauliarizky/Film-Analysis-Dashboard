from django.core.management.base import BaseCommand
from django.db import connection
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
from film_analysis.models import FilmModelInfo
from django.utils.timezone import now

class Command(BaseCommand):
    help = 'ETL: Build rental demand prediction model'

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT f.film_id, f.rental_rate, f.length, f.replacement_cost,
                       COUNT(r.rental_id) as rental_count
                FROM film f
                JOIN inventory i ON f.film_id = i.film_id
                JOIN rental r ON i.inventory_id = r.inventory_id
                GROUP BY f.film_id, f.rental_rate, f.length, f.replacement_cost
            """)
            rows = cursor.fetchall()

        df = pd.DataFrame(rows, columns=[
            'film_id', 'rental_rate', 'length',
            'replacement_cost', 'rental_count'
        ])

        # Save to CSV
        df.to_csv('film_rental_dataset.csv', index=False)
        self.stdout.write(self.style.SUCCESS('CSV saved: film_rental_dataset.csv'))

        # Create label: high demand if rental_count > median
        median = df['rental_count'].median()
        df['demand_label'] = (df['rental_count'] > median).astype(int)

        # Features & label
        features = ['rental_rate', 'length', 'replacement_cost']
        X = df[features]
        y = df['demand_label']

        # Train/test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Train model
        model = RandomForestClassifier()
        model.fit(X_train, y_train)

        # Evaluate
        predictions = model.predict(X_test)
        report = classification_report(y_test, predictions)
        self.stdout.write(self.style.SUCCESS("Classification Report:\n" + report))

        # Feature Importance
        self.stdout.write("Feature Importance:")
        for name, score in zip(features, model.feature_importances_):
            self.stdout.write(f"  {name}: {score:.4f}")

        # Save model
        model_filename = 'film_demand_model.pkl'
        joblib.dump(model, model_filename)
        self.stdout.write(self.style.SUCCESS(f'Model saved: {model_filename}'))

        # Save to DB
        FilmModelInfo.objects.create(
            model_name='FilmRentalDemandModel',
            model_file=model_filename,
            training_data='film_rental_dataset.csv',
            training_date=now(),
            model_summary=report
        )
        self.stdout.write(self.style.SUCCESS('Model info saved to DB!'))