from django.db import models

class Objective(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    created = models.DateField(auto_now_add=True)
    private = models.BooleanField(default=False)
    progress = models.DecimalField(default=0, max_digits=4, decimal_places=1)

class KeyResult(models.Model):
    objective = models.ForeignKey(Objective)
    name = models.CharField(max_length=255)
    description = models.TextField()
    progress = models.DecimalField(default=0, max_digits=4, decimal_places=1)