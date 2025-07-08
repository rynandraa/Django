from django.db import models
from django.urls import reverse
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    content =models.TextField()
    created_at =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse("post-detail", args=[str(self.id)])
    
    def update_created_at_time(self):
        self.created_at = timezone.now()