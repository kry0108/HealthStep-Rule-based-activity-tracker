from django.db import models

class Signup(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    age=models.CharField(max_length=100)
    gender = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class HealthProfile(models.Model):
    user = models.ForeignKey(Signup, on_delete=models.CASCADE)

    age = models.IntegerField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    bp = models.IntegerField(null=True, blank=True)
    sugar = models.FloatField(null=True, blank=True)
    bmi = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.user.name
    

    # models.py


class DailyEntry(models.Model):
    user = models.ForeignKey(Signup, on_delete=models.CASCADE)

    date = models.DateField()
    steps = models.IntegerField()
    water_intake = models.FloatField()
    calorie_intake = models.IntegerField()

    def __str__(self):
        return f"{self.user.name} - {self.date}"