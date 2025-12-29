from django import template
from django.utils import timezone
from django.db import models
from posts.models import Post

register = template.Library()


@register.simple_tag
def get_priority_posts(limit=5):
    """Récupère les posts prioritaires actifs"""
    now = timezone.now()
    posts = Post.objects.filter(
        publique=True,
        prioritaire=True
    ).filter(
        models.Q(date_expiration__gte=now) | models.Q(date_expiration__isnull=True)
    ).order_by('-date_publication')[:limit]
    
    return posts
