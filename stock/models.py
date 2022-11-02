from django.db import models

from account.models import User


# Create your models here.
class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255, unique=True)
    quantity = models.PositiveIntegerField(default=0)
    price = models.FloatField()

    def __str__(self):
        return '{}'.format(self.name)

    def get_absolute_url(self):
        return f"product/{self.pk}/"



