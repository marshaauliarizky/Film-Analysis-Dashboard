from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import joblib
import numpy as np
import json
import os
from .models import FilmPopularity, CategoryPerformance, FilmModelInfo
from .forms import FilmPredictionForm

def film_dashboard(request):
    form = FilmPredictionForm()
    top_films = FilmPopularity.objects.order_by('-rental_count')[:10]
    categories = CategoryPerformance.objects.order_by('-total_rentals')
    model_info = FilmModelInfo.objects.last()
    return render(request, 'film_analysis/dashboard.html', {
        'form': form,
        'top_films': top_films,
        'categories': categories,
        'model_info': model_info,
    })

model_path = os.path.join(settings.BASE_DIR, 'film_demand_model.pkl')
model = joblib.load(model_path)

@csrf_exempt
def predict_film(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        features = np.array([
            data['rental_rate'],
            data['length'],
            data['replacement_cost']
        ]).reshape(1, -1)
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0].tolist()
        return JsonResponse({
            'prediction': int(prediction),
            'probability': probability,
            'label': 'High Demand' if prediction == 1 else 'Low Demand'
        })