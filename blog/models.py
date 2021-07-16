from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from PIL import Image

TYPES = (
    ('Food', 'Food'),
    ('Fashion', 'Fashion'),
    ('Fitness', 'Fitness'),
    ('Finance', 'Finance'),
    ('Travel ', 'Travel '),
    ('Music', 'Music'),
    ('Lifestyle', 'Lifestyle'),
    ('Music', 'Music'),    
    ('Sports', 'Sports'),    
    ('Political', 'Political'),
    ('Gaming', 'Gaming'),    
)


class post(models.Model):
    title = models.CharField(max_length=100)
    type = models.CharField(max_length=20, blank=True, choices=TYPES)
    content = models.TextField()
    img = models.ImageField(upload_to='post_pics', blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='post_likes')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
