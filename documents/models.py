from django.db import models


# Create your models here.
class Documents(models.Model):
    objects = models.Manager()

    title = models.CharField(max_length=255)
    user = models.CharField(max_length=255)
    file = models.FileField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)
