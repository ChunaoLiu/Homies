from django.db import models
from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=25, default="Bruh")
    email = models.EmailField(default="No_EMAIL")
    class meta():
        db_table = 'User'
        ordering = ['name']

    def __str__(self):
        return self.name