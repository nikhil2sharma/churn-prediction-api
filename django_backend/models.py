# django_backend/models.py
from django.db import models

class ModelVersion(models.Model):
    """Every chef jar gets logged here"""
    
    version_tag = models.CharField(max_length=50)       # e.g. "v1.0.0"
    accuracy = models.FloatField()                       # 0.87
    trained_at = models.DateTimeField(auto_now_add=True)
    deployed = models.BooleanField(default=False)
    notes = models.TextField(blank=True)                 # "Retrained after data drift"

    def __str__(self):
        return f"{self.version_tag} - acc:{self.accuracy}"

class PredictionLog(models.Model):
    """Every order placed at the restaurant gets logged"""
    
    input_features = models.JSONField()
    prediction = models.IntegerField()
    probability = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)