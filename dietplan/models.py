from django.db import models
from django.contrib.auth.models import User

class DietPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    program = models.TextField()
    effects = models.TextField(blank=True, null=True)
    goal = models.TextField()

    def __str__(self):
        return f"Diet Plan for {self.user.username}"