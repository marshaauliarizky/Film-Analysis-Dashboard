# Film Popularity & Rental Demand Prediction

A business intelligence system for DVD rental store analytics, 
built with Django and Machine Learning.

## Features
- **Film Popularity Analysis** — Top 10 most rented films based on historical data
- **Category Performance Analysis** — Most popular genres by rentals and revenue
- **Rental Demand Prediction** — Predict High/Low demand for new films using ML

## Tech Stack
- Python / Django
- PostgreSQL (DVD Rental Database)
- Scikit-learn (Random Forest Classifier)
- Chart.js
- Pandas / NumPy / Joblib

## ETL Pipeline
3 ETL commands to process raw data into OLAP tables:
```bash
python manage.py etl_film_popularity
python manage.py etl_category_performance
python manage.py etl_rental_demand
```

## 🗃️ OLAP Tables
| Table | Description |
|-------|-------------|
| FilmPopularity | Rental count per film |
| CategoryPerformance | Total rentals & revenue per genre |
| FilmModelInfo | ML model information |

## ML Model
- Algorithm: Random Forest Classifier
- Features: rental_rate, length, replacement_cost
- Label: High Demand (1) / Low Demand (0)
- Threshold: Median rental count

## How to Run
1. Clone the repository
2. Create and activate virtual environment
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
3. Setup PostgreSQL with DVD Rental database
4. Run migrations
```bash
python manage.py migrate
```
5. Run ETL commands
```bash
python manage.py etl_film_popularity
python manage.py etl_category_performance
python manage.py etl_rental_demand
```
6. Start the server
```bash
python manage.py runserver
```
7. Open `http://127.0.0.1:8000/film/`
