from django.db import models

from django.db import models
from django.contrib.auth.models import User

class Property(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.IntegerField()
    zip_code = models.CharField(max_length=10)
    image = models.ImageField(upload_to="properties/", blank=True, null=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
