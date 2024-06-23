from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Documents(models.Model):
    objects = models.Manager()

    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)
