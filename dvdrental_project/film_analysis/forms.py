from django import forms

class FilmPredictionForm(forms.Form):
    rental_rate = forms.FloatField(label='Rental Rate', min_value=0)
    length = forms.IntegerField(label='Film Length (minutes)', min_value=1)
    replacement_cost = forms.FloatField(label='Replacement Cost', min_value=0)