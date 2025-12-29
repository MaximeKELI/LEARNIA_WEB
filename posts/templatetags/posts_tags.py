from django import template
from django.utils import timezone
from posts.models import Post

register = template.Library()


@register.inclusion_tag('posts/priority_posts.html', takes_context=True)
def get_priority_posts(context, limit=5):
    """Récupère les posts prioritaires actifs"""
    posts = Post.objects.filter(
        publique=True,
        prioritaire=True
    ).filter(
        date_expiration__gte=timezone.now()
    ) | Post.objects.filter(
        publique=True,
        prioritaire=True,
        date_expiration__isnull=True
    )
    
    posts = posts.order_by('-date_publication')[:limit]
    return {'posts': posts}

