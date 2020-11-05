from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Institution(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    TYPES = [
        (0, 'Fundacja'),
        (1, 'Organizacja pozarządowa'),
        (2, 'Zbiórka lokalna'),
    ]
    type = models.IntegerField(choices=TYPES, default=0)
    categories = models.ManyToManyField(Category, related_name='institutions')

    def __str__(self):
        return self.name


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category, related_name='donations')
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=150)
    phone_number = models.IntegerField()
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=6)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None, blank=True)

    def __str__(self):
        return f'Dar dla: {self.institution}, liczba worków: {self.quantity}, Odbiór: {self.pick_up_date} o {self.pick_up_time}'
