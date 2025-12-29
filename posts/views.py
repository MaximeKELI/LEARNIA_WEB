from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Post


def posts_list(request):
    """Affiche la liste des posts publics"""
    posts = Post.objects.filter(
        publique=True
    ).filter(
        date_expiration__gte=timezone.now()
    ) | Post.objects.filter(
        publique=True,
        date_expiration__isnull=True
    )
    
    posts = posts.order_by('-prioritaire', '-date_publication')
    return render(request, 'posts/list.html', {'posts': posts})


@login_required
def post_detail(request, post_id):
    """Détails d'un post"""
    from django.shortcuts import get_object_or_404
    post = get_object_or_404(Post, id=post_id, publique=True)
    
    # Vérifier que le post n'est pas expiré
    if not post.is_active():
        from django.http import Http404
        raise Http404("Ce post a expiré")
    
    return render(request, 'posts/detail.html', {'post': post})

