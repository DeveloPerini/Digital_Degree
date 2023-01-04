from django.db import models


class Student(models.Model):
    
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    birth_date = models.DateField()
    graduation_date = models.DateField()
    grade = models.FloatField()
    
    
    DEGREE_CHOICES = [
        ('BA', 'Bachelor'),
        ('MA', 'Master'),
        ('PHD', 'Doctorate'),
    ]
    degree = models.CharField(max_length=3, choices=DEGREE_CHOICES)
    
    
    identifier = models.CharField(max_length=10, unique=True)
    txId = models.CharField(max_length=66, default=None, null=True)